from discord.ext import commands
import discord
from mcstatus import MinecraftServer
import json



class Minecraft(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.newline = "\n"


    @commands.command(pass_context=True)
    async def minecraft(self, ctx, ip = 'emb.ovh:20001', modifier = None):
        """Retrieve Minecraft MOTD's"""
        try:
            response = json.loads(str(MinecraftServer.lookup(f"{ip}").query().raw).replace("\'", "\""))
            mc=discord.Embed(color=0x0080ff)
            mc.set_author(name=f"Minecraft Server: ({ip.upper()})", icon_url="https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/31/Enchanting_Table.gif")
            mc.add_field(name='MOTD', value=f"``{response['hostname']}``", inline=False)
            mc.add_field(name='Statistics', value=f"Players: ``{response['numplayers']+'/'+response['maxplayers']}``\nMap: ``{response['map'].capitalize()}``", inline=True)
            mc.add_field(name='Address', value=f"IP: ``{response['hostip']}``\nPORT: ``{response['hostport']}``", inline=True)
            if modifier != None: mc.add_field(name='Software', value=f"```diff\n- {str(response['plugins']).replace('; ', self.newline+'+ ').replace(': ', ':'+self.newline+'+ ')}```", inline=False)
            await ctx.reply(embed=mc)
        except Exception as e: await ctx.send(f'{e}')


def setup(client):
    client.add_cog(Minecraft(client))