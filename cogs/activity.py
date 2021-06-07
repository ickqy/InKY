import discord
import os


from discord.ext import commands


class Activity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.async_init())

    async def async_init(self):
        activity = discord.Activity(
            name=f"my owner be bad at coding", type=discord.ActivityType.watching
        )
        await self.bot.change_presence(activity=activity)

def setup(bot):
    bot.add_cog(Activity(bot))