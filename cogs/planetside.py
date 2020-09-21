import random
from discord.ext import commands
import discord
import json
import aiohttp
import urllib.request
import datetime
import asyncio
import sqlite3 as sql
import os

class Planetside(commands.Cog):
    def __init__(self, client):
        self.client = client

        #Default Variables
        self.PS2Images = ["https://cdn.discordapp.com/app-assets/309600524125339659/517514078227398677.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514073433309194.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514062985428993.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514065401217036.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514084455809034.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514083352969216.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514082136358916.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514072778866688.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514073055821825.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514077812293643.png"]
        self.server_num = {'briggs':25, "jaeger":19, 'connery':1,'miller':10,'emerald':17,'colbalt':13,'soltech':40}
        self.servers = ['briggs', "jaeger", 'connery','miller','emerald','colbalt','soltech']
        self.ps2icon = "https://pbs.twimg.com/profile_images/883060220779532288/zViSqVuM_400x400.jpg"
        self.icons = {'nc':'<:NC:528718336180092938>','vs':'<:VS:528718387627687936>','tr':'<:TR:528718372192649237>','NS':'<:NS:740268320988725381>'}
        self.colors = {'nc':0x0080ff,'vs':0x740084,'tr':0xa40000}
        self.NewCheckTime = 300

        #Default Embed for loading
        self.PS2_Loading_Embed=discord.Embed(color=0xc0c0c0)
        self.PS2_Loading_Embed.set_author(name="Planetside 2", icon_url=self.ps2icon)
        self.PS2_Loading_Embed.set_thumbnail(url=f"{random.choice(self.PS2Images)}")
        self.PS2_Loading_Embed.add_field(name=f'Loading...', value=f'``🔵`` ...\n``🟣`` ...\n``🔴`` ...', inline=True)
        self.PS2_Loading_Embed.add_field(name='Statistics', value=f'``POP :`` ...\n``OP  :`` ...\n``WIN :`` ...', inline=True)
        self.PS2_Loading_Embed.set_footer(text=f"| PS2.FISU.PW RT-API | {datetime.datetime.utcnow()} |")

        self.briggsTime   = None
        self.jaegerTime   = None
        self.conneryTime  = None
        self.millerTime   = None
        self.emeraldTime  = None
        self.colbaltTime  = None
        self.soltechTime  = None

        self.briggsData     = None
        self.jaegerData     = None
        self.conneryData    = None
        self.millerData     = None
        self.emeraldData    = None
        self.colbaltData    = None
        self.soltechData    = None

    async def msgdel(self, message, delay = 30):
        """deletes message after an delay"""
        await asyncio.sleep(delay)
        await message.delete()


    async def timed_delete(self, message, delay = 30):
        """Task Spawner for Deleting messages over time"""
        self.client.loop.create_task(self.msgdel(message, delay))


    async def timed_message(self, message, delay = 30):
        """Messages and deletes message after a delay"""
        msg2delete = await message.channel.send(message)
        await self.timed_delete(msg2delete, delay)
        return 

    def JsonGrab(self, URL, seconds = 15):
        try:
            data = json.loads(urllib.request.urlopen(URL, timeout=seconds).read().decode("utf8"))
        except urllib.error.URLError:
            return 'URLERROR'
        else:
            return data

    def PS2WorldGrab(self, WorldID):
        return self.JsonGrab(f"http://ps2.fisu.pw/api/population/?world={WorldID}")

    def PS2EmbedGen(self, JData, ServerName = "Server_Name"):
        NC = JData['result'][0]['nc']
        VS = JData['result'][0]['vs']
        TR = JData['result'][0]['tr']
        total = NC+VS+TR
        if NC is not 0:
            NCPERC = round(NC/total*100)
        else:
            NCPERC = NC
        if VS is not 0:
            VSPERC = round(VS/total*100)
        else:
            VSPERC = VS
        if TR is not 0:
            TRPERC = round(TR/total*100)
        else:
            TRPERC = TR
        if max(TR, NC, VS) == 0:
            embedcolor = 0xc0c0c0
            OverPOP = "NS"
        elif TR == max(TR, NC, VS):
            embedcolor = 0xa40000
            OverPOP = "TR"
        elif NC == max(TR, NC, VS):
            embedcolor = 0x0080ff
            OverPOP = "NC"
        elif VS == max(TR, NC, VS):
            embedcolor = 0x740084
            OverPOP = "VS"
        ps2embed=discord.Embed(color=embedcolor)
        ps2embed.set_author(name=f"Planetside 2", icon_url=self.ps2icon)
        ps2embed.set_thumbnail(url=f"{random.choice(self.PS2Images)}")
        ps2embed.add_field(name=f'{ServerName.capitalize()}', value=f'``🔵`` ``{NC} : {NCPERC}%``\n``🟣`` ``{VS} : {VSPERC}%``\n``🔴`` ``{TR} : {TRPERC}%``', inline=True)
        ps2embed.add_field(name='Statistics', value=f'``POP :`` ``{total}``\n``OP  :`` ``{OverPOP}``\n``WIN :`` ``WIP``', inline=True)
        ps2embed.set_footer(text=f"| PS2.FISU.PW RT-API | {datetime.datetime.utcnow()} |")
        return ps2embed

    @commands.command(pass_context=True, aliases=['briggs', 'Briggs', 'jaeger', 'Jaeger', 'connery', 'Connery', 'miller', 'Miller', 'emerald', 'Emerald', 'colbalt', 'Colbalt', 'soltech', 'Soltech'])
    async def Planetside(self, ctx):
        """Get Stats from a Planetside Server, Commands {self.client.prefixes[0]+self.servers[0]}"""
        server = ctx.message.content.split()[0][1:].lower()
        if server in self.servers:
            if eval(f"self.{server}Time == None") or eval(f'(datetime.datetime.now()-self.{server}Time).total_seconds() > self.NewCheckTime'):
                exec(f'self.{server}Time = datetime.datetime.now()')
                MSG = await ctx.send(f'{ctx.message.author.mention}', embed=self.PS2_Loading_Embed)
                exec(f'self.{server}Data = self.PS2EmbedGen(self.PS2WorldGrab("1"), "{server}")')
                await eval(f'MSG.edit(content="{ctx.message.author.mention}", embed=self.{server}Data)')
            else:
                MSG = await eval(f'ctx.send("{ctx.message.author.mention} ``CACHED``", embed=self.{server}Data)')


def setup(client):
    client.add_cog(Planetside(client))