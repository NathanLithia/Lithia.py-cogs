from discord.ext import commands
import psutil

class sensors(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(pass_context=True, hidden=True)
    @commands.is_owner()
    async def battery(self, ctx):
        """| Outputs system temperatures"""
        await ctx.send(str(psutil.sensors_battery()))


    @commands.command(pass_context=True, hidden=True)
    @commands.is_owner()
    async def temps(self, ctx):
        """| Outputs system temperatures"""
        await ctx.send(str(psutil.sensors_temperatures().get('cpu-thermal')))


def setup(client):
    client.add_cog(sensors(client))
