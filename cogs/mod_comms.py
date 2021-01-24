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

def setup(client):
    client.add_cog(Moderation(client))
