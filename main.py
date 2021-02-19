import discord
import os
import keep_alive
import config
from discord.ext import commands

client = commands.Bot(command_prefix = ['-', 'e', '!', '.'], intents=discord.Intents.all())

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Activity(type=discord.ActivityType.watching, name=('Over your Server')))

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

keep_alive.keep_alive()
client.run(config.token)