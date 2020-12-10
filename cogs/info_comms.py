import discord
import random
import time
from discord.ext import commands

class Information(commands.Cog):

    def __innit__(self, client):
        self.client = client
    
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is Online!')
    
    # Commands
    @commands.command()
    async def ping(self, ctx, arg=None):
        """- Check Bots Ping"""
        if arg == "pong":
            return await ctx.send("Congratulation, you just ponged yourself lol")

        else:
            start = time.perf_counter()
            message = await ctx.send("Ping...")
            end = time.perf_counter()
            duration = (end - start) * 1000
            await message.edit(content='Pong! {:.2f}ms'.format(duration))

    @commands.command(aliases=["bi", "about", "info",])
    async def botinfo(self, ctx):
        """- Show bot information."""
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

    @commands.command()
    async def userinfo(self, ctx, user: discord.Member = None):
        """Get information about a user"""
        # await ctx.send(f"```py\n{dump(user)}```")

        if not user:
            user = ctx.message.author

        output = ""
        for i in user.roles:
            output += i.mention + " "

        if user.color.value == 0:
            color = 16777210
        else:
            color = user.color

        if user.is_avatar_animated():
            profilePic = user.avatar_url_as(format="gif")
        else:
            profilePic = user.avatar_url_as(format="png")

        embed = discord.Embed(
            title=user.name,
            description=user.mention,
            color=color,
            timestamp=ctx.message.created_at,
        )
        if user.premium_since:
            embed.add_field(name="Boosting since", value=user.premium_since.date())
        # embed.set_thumbnail(url="attachment://temp.webp")
        embed.set_thumbnail(url=profilePic)
        embed.add_field(name="Nickname", value=user.display_name, inline=False)
        embed.add_field(name="Joined on", value=user.joined_at.date(), inline=True)
        embed.add_field(name="Status", value=user.status, inline=True)
        embed.add_field(
            name="Created account on", value=user.created_at.date(), inline=True
        )
        embed.add_field(name="Roles", value=output, inline=True)
        embed.set_footer(text=f"ID: {user.id}")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Information(client))