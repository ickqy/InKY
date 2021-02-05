import discord
from random import choice, randint, random
from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["cc"])
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, amount=1):
        """`Deletes messages in bulck (Only People with [manage_messages = True] can use this command)`"""
        await ctx.channel.purge(limit=amount)
        await ctx.send("Messages Deleted", delete_after=5)

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        """`Kick a Member (Only People with [kick_members = True] can use this command)`"""
        await member.send(f"You Have been kicked from {ctx.guild.name} for {reason}!")
        await ctx.send(f'{member.mention} has been kicked from the server')
        await member.kick(reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        """`Ban a Member (Only People with [ban_members = True] can use this command)`"""
        
        nah_fam = {
            564610598248120320,
            783159643126890517,
        }

        if member.id in nah_fam:
            await ctx.send('Shut up boomer')
            return

        else:
            await member.send(f"You Have been Banned from {ctx.guild.name} for {reason}!")
            await ctx.send(f"{member.mention} {choice(['has been Banned from the server', 'has been brrred from the server', 'has beed bonked from the server'])}!")
            await member.ban(reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, *, member):
        """`Unban a Member (Only People with [ban_members = True] can use this command)`"""
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                await member.send(f"You Have been Unbanned from {ctx.guild.name}!")
                return

        @commands.command()
    async def emojilist(self, ctx):
        """List all emoji in the server."""
        emojis = " ".join([str(emoji) for emoji in ctx.guild.emojis])
        emoji_list = textwrap.wrap(emojis, 1024)

        page = 1
        total_page = len(emoji_list)
        embed_reactions = ["◀️", "▶️", "⏹️"]

        def check_reactions(reaction, user):
            if user == ctx.author and str(reaction.emoji) in embed_reactions:
                return str(reaction.emoji)
            else:
                return False

        def create_embed(ctx, page):
            e = discord.Embed(
                title="Emojis",
                description=emoji_list[page - 1],
                color=discord.Colour(0xFFFFF0),
                timestamp=ctx.message.created_at,
            )
            e.set_author(
                name=f"{ctx.guild.name} - {page}/{total_page}",
                icon_url=ctx.guild.icon_url,
            )
            e.set_footer(
                text=f"Requested by {ctx.message.author.name}#{ctx.message.author.discriminator}"
            )
            return e

        embed = create_embed(ctx, page)
        msg = await ctx.send(embed=embed)
        for emoji in embed_reactions:
            await msg.add_reaction(emoji)
        while True:
            try:
                reaction, user = await self.client.wait_for(
                    "reaction_add", check=check_reactions, timeout=60.0
                )
            except asyncio.TimeoutError:
                break
            else:
                emoji = check_reactions(reaction, user)
                try:
                    await msg.remove_reaction(reaction.emoji, user)
                except discord.Forbidden:
                    pass
                if emoji == "◀️" and page != 1:
                    page -= 1
                    embed = create_embed(ctx, page)
                    await msg.edit(embed=embed)
                if emoji == "▶️" and page != total_page:
                    page += 1
                    embed = create_embed(ctx, page)
                    await msg.edit(embed=embed)
                if emoji == "⏹️":
                    # await msg.clear_reactions()
                    break
        return

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def poll(self, ctx, title, *options):
        emojiLetters = [
            "\N{REGIONAL INDICATOR SYMBOL LETTER A}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER B}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER C}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER D}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER E}", 
            "\N{REGIONAL INDICATOR SYMBOL LETTER F}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER G}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER H}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER I}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER J}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER K}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER L}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER M}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER N}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER O}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER P}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Q}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER R}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER S}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER T}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER U}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER V}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER W}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER X}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Y}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Z}"
        ]
        
        options = list(options)
        for i in range(len(options)):
            options[i] = f"{emojiLetters[i]}  {options[i]}"
        embed = discord.Embed(title=title,
        description='\n'.join(options),
        color=0xff0000)
        message = await ctx.send(embed=embed)
        for i in range(len(options)):
            await message.add_reaction(emojiLetters[i])
        await ctx.send('@everyone')

    @commands.Cog.listener()
    async def on_message(self, msg):

        filtered_words = {"-poll"}

        if msg.author == self.client.user:
            return
        
        else:
            for word in filtered_words:
                if word in msg.content:
                    await msg.delete()

def setup(client):
    client.add_cog(Moderation(client))
