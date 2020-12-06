import discord
import random
from discord.ext import commands

class Status_Commands(commands.Cog):

    def __innit__(self, client):
        self.client = client
    
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is Online!')
    
    # Commands
    @commands.command()
    async def ping(self, ctx):
        """- Check if the bot is online"""
        await ctx.send('Pong!')

    @commands.command(aliases=["bi", "about", "info",])
    async def botinfo(self, ctx):
        """Show bot information."""
        bot_ver = "1.0.0"
        embed = discord.Embed(
            title="About InKY Bot",
            colour=discord.Colour(0xFFFFF0),
            timestamp=ctx.message.created_at,
        )
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/783159643126890517/06e9f5496357fc24b6037dc92c159971.webp?size=1024')
        embed.add_field(name="Author", value="IKY#5948")
        embed.add_field(
            name="discord.py",
            value=f"[{discord.__version__}-modified](https://github.com/xIKYx/InKY-Bot)",
        )
        embed.add_field(
            name="About",
            value="**InKY Bot** is an open source bot, "
            + "a fork of [mcbeDiscordBot](https://github.com/AnInternetTroll/mcbeDiscordBot) "
            + "(Steve the Bot) created by [AnInternetTroll](https://github.com/AnInternetTroll), "
            + "and from [ZiRO-Bot](https://github.com/ZiRO-Bot/ziBot) (ziBot) created by "
            + "[null2264](https://github.com/null2264), "
            + f"but rewritten a bit.\n\n**Bot Version**: {bot_ver}",
            inline=False,
        )
        embed.set_footer(
            text=f"Requested by {ctx.message.author.name}#{ctx.message.author.discriminator}"
        )
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Status_Commands(client))