from discord.ext import commands
import asyncio
import discord
from geolite2 import geolite2

class GeoIP(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(pass_context=True, hidden=True, aliases=['ip'])
    @commands.is_owner()
    async def iptrack(self, ctx, ip = '1.1.1.1'):
        """ip (..IP..)"""
        print(f"!!!!{ip}")
        reader = geolite2.reader()
        match = reader.get(ip)
        if match is None:
            return geolite2.close()
        await ctx.send(f"""
                IP: {ip}
                Country: ``{match['country']['names']['en']}``
            """)
        return geolite2.close()


def setup(client):
    client.add_cog(GeoIP(client))
