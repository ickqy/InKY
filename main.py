import discord
import os
import config
from discord.ext import commands

client = commands.Bot(command_prefix = ['-'], intents=discord.Intents.all())

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Activity(type=discord.ActivityType.watching, name=('the chicken cross the road')))

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(config.token)