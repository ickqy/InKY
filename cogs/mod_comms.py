import discord
import random
from discord.ext import commands

class Moderation(commands.Cog):

    def __innit__(self, client):
        self.client = client

    @commands.command(aliases=["cc"])
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, amount=1):
        """- Delete messages in bulck"""
        await ctx.channel.purge(limit=amount)
        await ctx.send("Messages Deleted", delete_after=5)

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        """- Kick a Member"""
        await member.send(f"You Have been kicked from {ctx.guild.name} for {reason}!")
        await ctx.send(f'{member.mention} has been kicked from the server')
        await member.kick(reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        """- Ban a Member"""
        await member.send(f"You Have been Banned from {ctx.guild.name} for {reason}!")
        await ctx.send(f'{member.mention} has been Banned from the server')
        await member.ban(reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, *, member):
        """- Unban a Member"""
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
