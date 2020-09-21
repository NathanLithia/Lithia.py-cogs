from discord.ext import commands
import discord
from datetime import datetime
from time import time

class info(commands.Cog):
    def __init__(self, client):
        self.client = client


    def status_symbol(self, status):
        status = str(status)
        if status == 'online': return '🟢'
        elif status == 'offline': return '🟢'
        elif status == 'idle': return '🟡'
        elif status == 'dnd': return '🔴'
        elif status == 'do_not_disturb': return '🔴'
        elif status == 'invisible': return '⚪'
        else: return f'{status}'


    @commands.command(pass_context=True, aliases=['user','uinfo'])
    async def User(self, ctx, member: discord.Member = None):
        """Display Users Statistics."""
        if ctx.message.guild.id == 254821113563971584:
            return await ctx.send('This command is Disabled on this Guild.')
        if member is None: member = ctx.author
        userembed=discord.Embed(title=f'``{self.status_symbol(member.status)}`` ``{member.name}#{member.discriminator}`` ``{member.id}``')
        userembed.set_thumbnail(url=f"{member.avatar_url}")
        userembed.add_field(name='User Data', value=f"``Joined`` {member.joined_at}\n``Created`` {member.created_at}\n``Nick`` {member.nick}\n``Premium_since`` {member.premium_since}\n``Colour`` {member.colour}\n``Activity`` {member.activity}\n``top_role`` {member.top_role}\n``guild_permissions`` {member.guild_permissions}", inline=True)
        await ctx.send(embed=userembed)


    @commands.command(pass_context=True, aliases=['pfp', 'upic'])
    async def PFP(self, ctx, member: discord.Member = None):
        """Displays user images."""
        if member is None: member = ctx.message.author
        pfpembed=discord.Embed(title=f'``{member.name}``')
        pfpembed.set_image(url=member.avatar_url)
        await ctx.send(embed=pfpembed)


    @commands.command(pass_context=True, aliases=['spic'])
    async def SPic(self, ctx):
        """Prints server display image"""
        srvembed=discord.Embed(title=ctx.server.name)
        srvembed.set_image(url=ctx.server.icon_url)
        await ctx.send(ctx.message.channel, embed=srvembed)


    @commands.command(pass_context=True, aliases=['sinfo'])
    async def SInfo(self, ctx):
        """Prints server info"""
        stats = f"""
        Name: {ctx.message.server.name}
        Owner: {ctx.message.server.owner}
        Member_count: {ctx.message.server.member_count}
        Created_at: {ctx.message.server.created_at}
        ID: {ctx.message.server.id}
        Region: {ctx.message.server.region}
        Default_channel: {ctx.message.server.default_channel}
        Afk_channel: {ctx.message.server.afk_channel}
        Afk_timeout: {ctx.message.server.afk_timeout}
        """
        srvembed=discord.Embed(title='Server Information')
        srvembed.set_thumbnail(url=ctx.message.server.icon_url)
        srvembed.add_field(name='SERVER STATS', value=stats, inline=True)
        await ctx.send(ctx.message.channel, embed=srvembed)


def setup(client):
    client.add_cog(info(client))