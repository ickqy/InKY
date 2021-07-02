import discord
import os
import asyncio
import random
import re
import wavelink
import config

import typing as t
import datetime as dt


from discord.ext import commands

from enum import Enum


URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
OPTIONS = {
    "1️⃣": 0,
    "2⃣": 1,
    "3⃣": 2,
    "4⃣": 3,
    "5⃣": 4,
}


class AlreadyConnectedToChannel(commands.CommandError):
    pass


class NoVoiceChannel(commands.CommandError):
    pass


class QueueIsEmpty(commands.CommandError):
    pass


class NoTracksFound(commands.CommandError):
    pass


class PlayerIsAlreadyPaused(commands.CommandError):
    pass


class NoMoreTracks(commands.CommandError):
    pass


class NoPreviousTracks(commands.CommandError):
    pass


class InvalidRepeatMode(commands.CommandError):
    pass


class RepeatMode(Enum):
    NONE = 0
    ONE = 1
    ALL = 2


class Queue:
    def __init__(self):
        self._queue = []
        self.position = 0
        self.repeat_mode = RepeatMode.NONE

    @property
    def is_empty(self):
        return not self._queue

    @property
    def current_track(self):
        if not self._queue:
            raise QueueIsEmpty

        if self.position <= len(self._queue) - 1:
            return self._queue[self.position]

    @property
    def upcoming(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[self.position + 1:]

    @property
    def history(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[:self.position]

    @property
    def length(self):
        return len(self._queue)

    def add(self, *args):
        self._queue.extend(args)

    def get_next_track(self):
        if not self._queue:
            raise QueueIsEmpty

        self.position += 1

        if self.position < 0:
            return None
        elif self.position > len(self._queue) - 1:
            if self.repeat_mode == RepeatMode.ALL:
                self.position = 0
            else:
                return None

        return self._queue[self.position]

    def shuffle(self):
        if not self._queue:
            raise QueueIsEmpty

        upcoming = self.upcoming
        random.shuffle(upcoming)
        self._queue = self._queue[:self.position + 1]
        self._queue.extend(upcoming)

    def set_repeat_mode(self, mode):
        if mode == "none":
            self.repeat_mode = RepeatMode.NONE
        elif mode == "1":
            self.repeat_mode = RepeatMode.ONE
        elif mode == "all":
            self.repeat_mode = RepeatMode.ALL

    def empty(self):
        self._queue.clear()
        self.position = 0


class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()

    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnectedToChannel

        if (channel := getattr(ctx.author.voice, "channel", channel)) is None:
            raise NoVoiceChannel

        await super().connect(channel.id)
        return channel

    async def teardown(self):
        try:
            await self.destroy()
        except KeyError:
            pass

    async def add_tracks(self, ctx, tracks):
        if not tracks:
            raise NoTracksFound

        if isinstance(tracks, wavelink.TrackPlaylist):
            self.queue.add(*tracks.tracks)
        elif len(tracks) == 1:
            self.queue.add(tracks[0])
            await ctx.reply(f"Added {tracks[0].title} to the queue.")
        else:
            if (track := await self.choose_track(ctx, tracks)) is not None:
                self.queue.add(track)
                await ctx.reply(f"Added {track.title} to the queue.")

        if not self.is_playing and not self.queue.is_empty:
            await self.start_playback()

    async def choose_track(self, ctx, tracks):
        def _check(r, u):
            return (
                r.emoji in OPTIONS.keys()
                and u == ctx.author
                and r.message.id == msg.id
            )

        embed = discord.Embed(
            title="Choose a song",
            description=(
                "\n".join(
                    f"**{i+1}.** {t.title} ({t.length//60000}:{str(t.length%60).zfill(2)})"
                    for i, t in enumerate(tracks[:5])
                )
            ),
            colour=discord.Colour(0x000000),
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Query Results")
        embed.set_footer(text=f"Invoked by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        msg = await ctx.reply(embed=embed)
        for emoji in list(OPTIONS.keys())[:min(len(tracks), len(OPTIONS))]:
            await msg.add_reaction(emoji)

        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=_check)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
        else:
            await msg.delete()
            return tracks[OPTIONS[reaction.emoji]]

    async def start_playback(self):
        await self.play(self.queue.current_track)

    async def advance(self):
        try:
            if (track := self.queue.get_next_track()) is not None:
                await self.play(track)
        except QueueIsEmpty:
            pass

    async def repeat_track(self):
        await self.play(self.queue.current_track)


class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.bot = bot
        self.wavelink = wavelink.Client(bot=bot)
        self.bot.loop.create_task(self.start_nodes())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                await self.get_player(member.guild).teardown()

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node):
        print(f" Wavelink node `{node.identifier}` ready.")

    @wavelink.WavelinkMixin.listener("on_track_stuck")
    @wavelink.WavelinkMixin.listener("on_track_end")
    @wavelink.WavelinkMixin.listener("on_track_exception")
    async def on_player_stop(self, node, payload):
        if payload.player.queue.repeat_mode == RepeatMode.ONE:
            await payload.player.repeat_track()
        else:
            await payload.player.advance()

    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Music commands are not available in DMs.")
            return False

        return True

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        nodes = {
            "MAIN": {
                "host": "127.0.0.1",
                "port": 2333,
                "rest_uri": "http://127.0.0.1:2333",
                "password": "youshallnotpass",
                "identifier": "MAIN",
                "region": "europe",
            }
        }

        for node in nodes.values():
            await self.wavelink.initiate_node(**node)

    def get_player(self, obj):
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)

    @commands.command(name="connect", aliases=["join", "hello"])
    async def connect_command(self, ctx, *, channel: t.Optional[discord.VoiceChannel]):
        """`Connect the bot to your/a voice channel`"""
        player = self.get_player(ctx)
        channel = await player.connect(ctx, channel)
        await ctx.reply(f"Connected to {channel.name}.")

    @connect_command.error
    async def connect_command_error(self, ctx, exc):
        if isinstance(exc, AlreadyConnectedToChannel):
            await ctx.reply("Already connected to a voice channel.")
        elif isinstance(exc, NoVoiceChannel):
            await ctx.reply("No suitable voice channel was provided.")

    @commands.command(name="disconnect", aliases=["leave", "bye"])
    async def disconnect_command(self, ctx):
        """`Disconnect the bot from the voice channel`"""
        player = self.get_player(ctx)
        await player.teardown()
        await ctx.send("Disconnected.")

    @commands.command(name="clear", aliases=["c"])
    async def clear_command(self, ctx):
        """`Clear the queue`"""
        player = self.get_player(ctx)
        if player.queue.is_empty:
            raise QueueIsEmpty

        else:
            player.queue.empty()
            await player.set_pause(True)
            await ctx.reply("The queue has been cleared.")

    @clear_command.error
    async def clear_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.reply("No songs to clear as the queue is empty.")
        elif isinstance(exc, NoVoiceChannel):
            await ctx.reply("You are not in a voice channel, therefore there's no queue to clear.")

    @commands.command(name="nowplaying", aliases=["np"])
    async def nowplaying_command(self, ctx):
        """`Shows what song is currentlly playing`"""
        player = self.get_player(ctx)
        if player.is_paused:
            raise PlayerIsAlreadyPaused

        if player.queue.is_empty:
            raise QueueIsEmpty

        else:
            embed = discord.Embed(
                title="Now Playing",
                description=f"**{player.queue.current_track}**",
                colour=discord.Colour(0x000000),
                )
            embed.add_field(
                name="Time Stamp",
                value=f"{round(player.position/1000)//60:02}:{round(player.position/1000)%60:02}/"
                + f"{round(player.queue.current_track.length/1000)//60:02}:{round(player.queue.current_track.length/1000)%60:02}",
                inline=False
                )
            await ctx.reply(embed=embed)

    @nowplaying_command.error
    async def nowplaying_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.reply("No songs are currently playing")
        elif isinstance(exc, QueueIsEmpty):
            await ctx.reply("There are no songs in the queue")

    @nowplaying_command.error
    async def now_playing_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.reply("No songs are currentlly playing")
        if isinstance(exc, QueueIsEmpty):
            await ctx.reply("There are no songs in the queue.")

    @commands.command(name="play", aliases=["p"])
    async def play_command(self, ctx, *, query: t.Optional[str]):
        """`Add a song to the queue or resume the song`"""
        player = self.get_player(ctx)

        if not player.is_connected:
            await player.connect(ctx)

        if query is None:
            if player.queue.is_empty:
                raise QueueIsEmpty

            await player.set_pause(False)
            await ctx.reply("Playback resumed.")

        else:
            query = query.strip("<>")
            if not re.match(URL_REGEX, query):
                query = f"ytsearch:{query}"

            await player.add_tracks(ctx, await self.wavelink.get_tracks(query))

    @play_command.error
    async def play_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.reply("No songs to play as the queue is empty.")
        elif isinstance(exc, NoVoiceChannel):
            await ctx.reply("No suitable voice channel was provided.")

    @commands.command(name="pause")
    async def pause_command(self, ctx):
        """`Pause the song`"""
        player = self.get_player(ctx)

        if player.is_paused:
            raise PlayerIsAlreadyPaused

        await player.set_pause(True)
        await ctx.reply("Playback paused.")

    @pause_command.error
    async def pause_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.reply("Already paused.")

    @commands.command(name="stop")
    async def stop_command(self, ctx):
        """`Stop the queue from playing`"""
        player = self.get_player(ctx)
        player.queue.empty()
        await player.stop()
        await ctx.reply("Playback stopped.")

    @commands.command(name="next", aliases=["skip"])
    async def next_command(self, ctx):
        """`Play the next song in queue`"""
        player = self.get_player(ctx)

        if not player.queue.upcoming:
            raise NoMoreTracks

        await player.stop()
        await ctx.reply("Playing next track in queue.")

    @next_command.error
    async def next_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.reply("This could not be executed as the queue is currently empty.")
        elif isinstance(exc, NoMoreTracks):
            await ctx.reply("There are no more tracks in the queue.")

    @commands.command(name="previous")
    async def previous_command(self, ctx):
        """`Go to the previous song in the queue`"""
        player = self.get_player(ctx)

        if not player.queue.history:
            raise NoPreviousTracks

        player.queue.position -= 2
        await player.stop()
        await ctx.reply("Playing previous track in queue.")

    @previous_command.error
    async def previous_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.reply("This could not be executed as the queue is currently empty.")
        elif isinstance(exc, NoPreviousTracks):
            await ctx.reply("There are no previous tracks in the queue.")

    @commands.command(name="shuffle")
    async def shuffle_command(self, ctx):
        """`Shuffle the songs in the queue`"""
        player = self.get_player(ctx)
        player.queue.shuffle()
        await ctx.reply("Queue shuffled.")

    @shuffle_command.error
    async def shuffle_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.reply("The queue could not be shuffled as it is currently empty.")

    @commands.command(name="repeat")
    async def repeat_command(self, ctx, mode: str):
        """`Reapeat songs, arguments are none, 1 and all`"""
        if mode not in ("none", "1", "all"):
            raise InvalidRepeatMode

        player = self.get_player(ctx)
        player.queue.set_repeat_mode(mode)
        await ctx.reply(f"The repeat mode has been set to {mode}.")

    @commands.command(name="queue", aliases=["q"])
    async def queue_command(self, ctx, show: t.Optional[int] = 10):
        """`Check what songs are in the queue`"""
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        embed = discord.Embed(
            title="Queue",
            description=f"Showing up to next {show} tracks",
            colour=discord.Colour(0x000000),
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Query Results")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.add_field(
            name="Currently playing",
            value=getattr(player.queue.current_track, "title", "No tracks currently playing."),
            inline=False
        )
        if upcoming := player.queue.upcoming:
            embed.add_field(
                name="Next up",
                value="\n".join(t.title for t in upcoming[:show]),
                inline=False
            )

        await ctx.reply(embed=embed)

    @queue_command.error
    async def queue_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.reply("The queue is currently empty.")

    @commands.command(name="soundeffect", aliases=['se'])
    async def soundeffect_command(self, ctx, arg=None):
        """`Play a sound effect`"""
        player = self.get_player(ctx)
        embed_reaction = ["🔁"]
        response = ["✅", "❎"]

        def check_reaction(reaction, user):
            if user == ctx.author and str(reaction.emoji) in embed_reaction:
                return str(reaction.emoji)
            else:
                return False

        def check_response(reaction, user):
            if user == ctx.author and str(reaction.emoji) in response:
                return str(reaction.emoji)
            else:
                return False

        if not player.is_connected:
            await player.connect(ctx)

        if not player.queue.is_empty:
            warn = await ctx.reply("Playing a sound effect will stop the song and will clear the queue. Would you like to continue?")
            for emoji in response:
                await warn.add_reaction(emoji)
            while True:
                try:
                    reaction, user = await self.bot.wait_for(
                        "reaction_add", check=check_response, timeout=20.0
                    )
                except asyncio.TimeoutError:
                    await warn.edit(content="Times out, stopped command.")
                    await warn.clear_reactions()
                    break
                else:
                    emoji = check_response(reaction, user)
                    try:
                        await warn.remove_reaction(reaction.emoji, user)
                    except discord.Forbidden:
                        pass
                    if emoji == "❎":
                        await warn.edit(content="Stopped Sound effect")
                        await warn.clear_reactions()
                        return
                    if emoji == "✅":
                        await warn.delete()
                        await player.set_pause(True)
                        player.queue.empty()
                        break

        if player.is_connected:
            if arg is None:
                await ctx.reply("No sound effect was provided. To see the list of sound effects, do `-lse` to see the list of sound effects.")
                return

            source = await self.wavelink.get_tracks(config.path+f"{arg}.mp4")

            if source is None:
                await ctx.reply("You did not provide a valid sound effect, do `-lse` to view all the available sound effects.")
                return

            await player.play(source[0])

            msg = await ctx.reply("Dispatching sound...")
            for emoji in embed_reaction:
                await msg.add_reaction(emoji)
            while True:
                try:
                    reaction, user = await self.bot.wait_for(
                        "reaction_add", check=check_reaction, timeout=60.0
                    )
                except asyncio.TimeoutError:
                    await msg.clear_reactions()
                    break
                else:
                    emoji = check_reaction(reaction, user)
                    try:
                        await msg.remove_reaction(reaction.emoji, user)
                    except discord.Forbidden:
                        pass
                    if emoji == "🔁":
                        await player.play(source[0])

    @soundeffect_command.error
    async def soundeffect_command_error(self, ctx, exc):
        if isinstance(exc, NoVoiceChannel):
            await ctx.reply("No suitable voice channel was provided.")

    @commands.command(name="selist", aliases=["lse"])
    async def selist_command(self, ctx):
        """`Shows a list of sound effects you can play`"""
        path = config.path

        files = os.listdir(path)

        sounds = []
        for f in files:
            sounds.append(f)
        embed = discord.Embed(
            title="List of Sound Effects",
            description="**" + "\n".join([sound.rstrip(".mp4") for sound in files]) + "**",
            color=0x000000,
            )
        embed.add_field(
            name="-se <sound effect name> to play sound effect",
            value="This is the list of sound effects you can use, remember to type it exactly like it's written.",
            inline=False
            )
        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Music(bot))
