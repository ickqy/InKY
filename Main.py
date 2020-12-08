import discord
import os
import config
from discord.ext import commands

client = commands.Bot(command_prefix = '-')

@client.command()
async def reload(ctx, extension):
    """- Unload and Load <extension> cogs"""
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send('Successfully Reloaded Extension! <:greenTick:767209095090274325>')

@client.command()
async def unload(ctx, extension):
    """- Unload <extension> cogs"""
    client.unload_extension(f'cogs.{extension}')
    await ctx.send('Successfully Unloaded Extension! <:greenTick:767209095090274325>')

@client.command()
async def load(ctx, extension):
    """- Load <extension> cogs"""
    client.load_extension(f'cogs.{extension}')
    await ctx.send('Successfully Loaded Extension! <:greenTick:767209095090274325>')

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Activity(type=discord.ActivityType.watching, name=('Over your Server')))

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(config.token)
