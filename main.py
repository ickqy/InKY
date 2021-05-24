import discord
import os
import config
from discord.ext import commands

client = commands.Bot(command_prefix = ['-'], intents=discord.Intents.all())

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Streaming(name="The Full Orchestra Concert", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(config.token)