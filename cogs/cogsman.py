import discord
from discord.ext import commands

class cogman(commands.Cog):
    """COG Management COG for Lithia"""
    def __init__(self, client):
        self.client = client


    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def cogload(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        try:
            self.client.load_extension(cog)
        except Exception as e:
            await ctx.send(f'`🔴{type(e).__name__}` - {e}')
        else:
            await ctx.send(f'`🔼Loaded_Cog:` {cog}')


    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def cogunload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        try:
            self.client.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'`🔴{type(e).__name__}` - {e}')
        else:
            await ctx.send(f'`🔽Unloaded_Cog:` {cog}')


    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def cogreload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        try:
            self.client.unload_extension(cog)
            self.client.load_extension(cog)
        except Exception as e:
            await ctx.send(f'`🔴{type(e).__name__}` - {e}')
        else:
            await ctx.send(f'`🔁Reloaded_Cog:` {cog}')


def setup(client):
    client.add_cog(cogman(client))