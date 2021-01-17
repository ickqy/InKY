import discord
from discord.ext import commands
import numexpr as ne

class Math(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def math(self, ctx, *, arg):
        try:
            result = eval(arg)
            await ctx.send(int(result))
        except:
            await ctx.send("That is not a math statement. Here is an example of a math statement: 1 + 2 - 3 * 4")

def setup(client):
    client.add_cog(Math(client))