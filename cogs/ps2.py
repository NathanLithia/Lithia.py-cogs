import random
from discord.ext import commands
import discord
import json
import aiohttp
import urllib.request
import datetime
import asyncio
import time

class PS2(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.ps2thumbs = ["517514078227398677.png","517514073433309194.png","517514062985428993.png","517514065401217036.png","517514084455809034.png","517514083352969216.png","517514082136358916.png","517514072778866688.png","517514073055821825.png","517514077812293643.png"]
        self.assetpath = "https://cdn.discordapp.com/app-assets/309600524125339659/"
        self.servernum = {
            'briggs':'25',
            'jaeger':'19',
            'connery':'1',
            'miller':'10',
            'emerald':'17',
            'cobalt':'13',
            'soltech':'40',
            'apex':'24',
            '25':'briggs',
            '19':'jaeger',
            '1':'connery',
            '10':'miller',
            '17':'emerald',
            '13':'cobalt',
            '40':'soltech',
            '24':'apex'
            }
        self.servers = [
        'briggs',
        'jaeger',
        'connery',
        'miller',
        'emerald',
        'cobalt',
        'soltech',
        'apex'
        ]

    def share(self, NS, NC, TR, VS):
        # PS2 Servers tend to favor VS over all factions when drawing with another faction in an alert, Re-arrage based on that data. my predictions are VS>TR>NC
        while NS >= 1:
            NS = NS - 1
            if VS == min(NC,TR,VS):
                VS = VS + 1
            elif TR == min(NC,TR,VS):
                TR = TR + 1
            elif NC == min(NC,TR,VS):
                NC = NC + 1
        return [NC,TR,VS]

    def CreatePS2Embed(self, server):
        #load Population data from Fisu api
        try:
            JsonData = json.loads(urllib.request.urlopen(f"http://ps2.fisu.pw/api/population/?world={self.servernum[server]}", timeout=15).read().decode("utf8"))
        except urllib.error.URLError:
            ps2embed=discord.Embed(color=0xa40000)
            ps2embed.add_field(name=f'{server.upper()}-{self.servernum[server]}', value=f'``Could not contact Fisu api``')
            return ps2embed

        # Force fail if server does not exist.
        if JsonData['result'] == False:
            ps2embed=discord.Embed(color=0xa40000)
            ps2embed.add_field(name=f'{server.upper()}-{self.servernum[server]}', value=f'``Planetside Server could not be found.``')
            return ps2embed

        #Assign JSON values to factions.
        NC = JsonData['result'][0]['nc']
        VS = JsonData['result'][0]['vs']
        TR = JsonData['result'][0]['tr']
        NS = JsonData['result'][0]['ns']

        #Calculating population percentages, theres probably a better way to do this.
        Total = NC+VS+TR+NS
        if NC != 0: NCPERC = round(NC/Total*100)
        else: NCPERC = NC
        if VS != 0: VSPERC = round(VS/Total*100)
        else: VSPERC = VS
        if TR != 0: TRPERC = round(TR/Total*100)
        else: TRPERC = TR

        #Calculate the embed color for OP faction, Theres probably a better way to do this.
        if max(TR, NC, VS) == 0:
            embedcolor = 0xc0c0c0
        elif TR == max(TR, NC, VS):
            embedcolor = 0xa40000
        elif NC == max(TR, NC, VS):
            embedcolor = 0x0080ff
        elif VS == max(TR, NC, VS):
            embedcolor = 0x740084

        Balance = self.share(NS, NC, TR, VS)
        BalNC = Balance[0]
        BalTR = Balance[1]
        BalVS = Balance[2]
        if BalNC != 0: BalNCPERC = round(BalNC/Total*100)
        else: BalNCPERC = BalNC
        if BalVS != 0: BalVSPERC = round(BalVS/Total*100)
        else: BalVSPERC = BalVS
        if BalTR != 0: BalTRPERC = round(BalTR/Total*100)
        else: BalTRPERC = BalTR

        #Create an Embed
        ps2embed=discord.Embed(color=embedcolor)
        ps2embed.set_thumbnail(url=f"{self.assetpath+random.choice(self.ps2thumbs)}")
        ps2embed.add_field(name=f'{server.upper()}-{self.servernum[server]}', value=f'``🔵`` ``{NCPERC}% : {NC}``\n``🟣`` ``{VSPERC}% : {VS}``\n``🔴`` ``{TRPERC}% : {TR}``\n``⚪`` ``NSO : {NS}``', inline=True)
        ps2embed.add_field(name=f'Balance Est', value=f'``🔵`` ``{BalNCPERC}% : {BalNC}``\n``🟣`` ``{BalVSPERC}% : {BalVS}``\n``🔴`` ``{BalTRPERC}% : {BalTR}``\n``TOTAL : {Total}``', inline=True)
        return ps2embed


    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(pass_context=True)
    async def psc(self, ctx, server):
        if server.lower() in self.servers:
            try:
                await ctx.reply(embed=self.CreatePS2Embed(server))
            except Exception as e:
                await ctx.reply(str(e))

def setup(client):
    client.add_cog(PS2(client))