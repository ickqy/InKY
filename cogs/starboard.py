import discord
from discord.ext import commands
import json

class Starboard(commands.Cog):

    def __innit__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_reaction_add(self, client, reaction, user):
        if (
            reaction.emoji == "⭐"
            and not reaction.message.id in self.client.pins
            and reaction.count >= 5
        ):
            self.client.pins.append(reaction.message.id)

            embed = discord.Embed(
                title="**New Starred Message**",
                description=reaction.message.content,
                colour=discord.Colour(0xB92C36),
                url=reaction.message.jump_url,
                timestamp=reaction.message.created_at,
            )

            for attachement in reaction.message.attachments:
                if attachement.height:
                    embed.set_image(url=attachement.url)
            embed.set_author(
                name=str(reaction.message.author),
                icon_url=reaction.message.author.avatar_url_as(format="png"),
            )
            embed.set_footer(text=reaction.message.id)

            # embed.add_field(name="Stars", value=reaction.count)
            channel = self.client.get_channel(
                int(self.client.config[str(reaction.message.guild.id)]["pins_channel"])
            )
            await channel.send(embed=embed)

def setup(client):
    client.add_cog(Starboard(client))