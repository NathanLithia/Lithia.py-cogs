import discord
from discord.ext import commands
import datetime
import hashlib
import ast


class DevTools(commands.Cog):
    """Development COG for Lithia"""
    def __init__(self, client):
        self.client = client


    @commands.command(hidden=True)
    @commands.is_owner()
    async def reboot(self, ctx):
        """| Reboots the client."""
        await ctx.send("```SubUnit\nRebooting <"+self.client.user.name+"> : "+str(datetime.datetime.now())+"z```")
        await self.client.close()


    @commands.command(hidden=True)
    @commands.is_owner()
    async def cinvite(self, ctx, channel):
        """| Creates an invite."""
        server_channel = self.client.get_channel(channel)
        invitelinknew = await self.client.create_invite(server_channel, xkcd = True, max_uses = 1)
        await ctx.send(invitelinknew)


    @commands.command(hidden=True)
    async def probe(self, ctx, data):
        "| Probes Destination"
        output = ""
        guild = self.client.get_guild(data)
        for channel in guild.channels:
            output = output+f"``{channel.id}`` ``{channel.name}``\n"
        await ctx.send(output)


    @commands.command(hidden=True)
    @commands.is_owner()
    async def leaveserver(self, ctx, data):
        "leaves server"
        server = self.client.get_guild(data)
        await self.client.leave_guild(server)


    @commands.command(hidden=True)
    async def servers(self, ctx):
        """Prints servers"""
        output = ""
        for guild in self.client.guilds:
            output = output+f"``{guild.id}`` ``{guild.name}``\n"
        await ctx.send(output)


    @commands.command(hidden=True)
    @commands.is_owner()
    async def unban(self, ctx, guild, member: None):
        """| Reloads an extension."""
        if member is None:
            member = ctx.message.author
        guilds = self.client.get_guild(guild)
        await self.client.unban(guilds, ctx.message.author)


    @commands.command(hidden=True)
    @commands.is_owner()
    async def kick(self, ctx, userName: discord.User):
        """| Kicks user."""
        if userName != None:
            return await self.client.kick(userName)
        else:
            return


    @commands.command(hidden=True)
    @commands.is_owner()
    async def clean(self, ctx, xlines: int): #purge_from(channel, *, limit=100, check=None, before=None, after=None, around=None)
        """| Cleans chat."""
        print(xlines)
        self.client.purge_from(ctx.message.channel, limit=xlines)
        return


    @commands.command(hidden=True)
    @commands.is_owner()
    async def appen(self, ctx, member, message: str = None, ):
        """Debug."""
        if member == None:
            member = ctx.message.author
        role = discord.utils.get(ctx.message.guild.roles, name=message)
        return await member.add_roles(member, role)


    @commands.command(hidden=True)
    @commands.is_owner()
    async def remov(self, ctx, message: str = None):
        """Debug."""
        role = discord.utils.get(ctx.message.guild.roles, name=message)
        return await self.client.remove_roles(ctx.message.author, role)


    @commands.command(hidden=True)
    @commands.is_owner()
    async def nick(self, ctx, *, message: str = "Lithia"):
        """nickname."""
        await self.client.change_nickname(ctx.message.server.me, f"{message}")


def setup(client):
    client.add_cog(DevTools(client))