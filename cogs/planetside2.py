import random
from discord.ext import commands
import discord
import json
import aiohttp
import urllib.request
import datetime
import asyncio

#OFFLINE SERVER OUTPUT FOR https://ps2.fisu.pw/api/territory/?world=1&continent=6
#{"config":{"world":1,"continent":6,"time":1579102080,"timeend":1579102080},"result":[],"timing":{"start-ms":0,"query-ms":43,"process-ms":0,"total-ms":43}}

# world - World id (1 = Connery, 10 = Miller, 13 = Cobalt, 17 = Emerald, 19 = Jaeger, 25 = Briggs, 40 = SolTech).
# continent - Continent id (0 = All, 2 = Indar, 4 = Hossin, 6 = Amerish, 8 = Esamir).

planetside_servers = ['BRIGGS', '25', 'JAEGER', '19', 'CONNERY', '1', 'MILLER', '10', 'EMERALD', '17', 'COLBALT', '13', '40', 'SOLTECH']

planetside_help_cmd = """```diff
- Planetside help prompt
+ Planetside help
+ Planetside servers
- Player Online Status
+ Planetside status <USERNAME>
- Player Character Stats
+ Planetside character <USERNAME>
- Server Population
+ Planetside population <SERVER>
- Server alert status
+ Planetside alert <SERVER>
```"""
world = "http://ps2.fisu.pw/api/population/?world"

PS2Images = [
"https://cdn.discordapp.com/app-assets/309600524125339659/517514078227398677.png",
"https://cdn.discordapp.com/app-assets/309600524125339659/517514073433309194.png",
"https://cdn.discordapp.com/app-assets/309600524125339659/517514062985428993.png",
"https://cdn.discordapp.com/app-assets/309600524125339659/517514065401217036.png",
"https://cdn.discordapp.com/app-assets/309600524125339659/517514084455809034.png",
"https://cdn.discordapp.com/app-assets/309600524125339659/517514083352969216.png",
"https://cdn.discordapp.com/app-assets/309600524125339659/517514082136358916.png",
"https://cdn.discordapp.com/app-assets/309600524125339659/517514072778866688.png",
"https://cdn.discordapp.com/app-assets/309600524125339659/517514073055821825.png",
"https://cdn.discordapp.com/app-assets/309600524125339659/517514077812293643.png"
]

PS2ICON = "https://pbs.twimg.com/profile_images/883060220779532288/zViSqVuM_400x400.jpg"

PS2LoadEmbed=discord.Embed(color=0xc0c0c0)
PS2LoadEmbed.set_author(name="Planetside 2", icon_url=PS2ICON)
PS2LoadEmbed.set_thumbnail(url=f"{random.choice(PS2Images)}")
PS2LoadEmbed.add_field(name=f'Loading...', value=f'<:NC:528718336180092938> ...\n<:VS:528718387627687936> ...\n<:TR:528718372192649237> ...', inline=True)
PS2LoadEmbed.add_field(name='Statistics', value=f'POP: ...\nOP: ...', inline=True)
PS2LoadEmbed.set_footer(text=f"| Contacting PS2.FISU.PW |")

PS2BriggsEmbed=discord.Embed(color=0xa40000)
PS2BriggsEmbed.set_author(name="Planetside 2", icon_url=PS2ICON)
PS2BriggsEmbed.set_thumbnail(url=f"{random.choice(PS2Images)}")
PS2BriggsEmbed.add_field(name=f'Briggs', value=f'<:NC:528718336180092938> 12 : 1%\n<:VS:528718387627687936> 20 : 1%\n<:TR:528718372192649237> 500 : 99999%', inline=True)
PS2BriggsEmbed.add_field(name='Statistics', value=f'POP: 532\nOP: TR', inline=True)
PS2BriggsEmbed.set_footer(text=f"| LONG.LIVE.BRIGGS |")

class Planetside(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.NewCheckTime = 30

        self.BriggsTime   = None
        self.JaegerTime   = None
        self.ConneryTime  = None
        self.MillerTime   = None
        self.EmeraldTime  = None
        self.ColbaltTime  = None
        self.SolTechTime  = None

        self.BriggsData     = None
        self.JaegerData     = None
        self.ConneryData    = None
        self.MillerData     = None
        self.EmeraldData    = None
        self.ColbaltData    = None
        self.SolTechData    = None

# Cooldown
# @commands.cooldown(2, 1, commands.BucketType.default)

### TODO ###
# CONVERT URLLIB REQUESTS TO AIOHTTP
# ADD MORE FUNCTIONALITY
# CLEAN UP CODE

# AIOHTTP EXAMPLE
#   async with aiohttp.ClientSession() as cs:
#       async with cs.get('http://random.cat/meow') as r:
#           res = await r.json()
#           await client.send_message(channel, res['file'])

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
        ps2embed.set_author(name="Planetside 2", icon_url=PS2ICON)
        ps2embed.set_thumbnail(url=f"{random.choice(PS2Images)}")
        ps2embed.add_field(name=f'{ServerName}', value=f'<:NC:528718336180092938> {NC} : {NCPERC}%\n<:VS:528718387627687936> {VS} : {VSPERC}%\n<:TR:528718372192649237> {TR} : {TRPERC}%', inline=True)
        ps2embed.add_field(name='Statistics', value=f'POP: {total}\nOP: {OverPOP}', inline=True)
        ps2embed.set_footer(text=f"| PS2.FISU.PW | {datetime.datetime.utcnow()} |")
        return ps2embed


    #@commands.command(aliases=['briggs', 'BRIGGS', 'bruggs', 'breggs', 'broggs', 'braggs'])
    #async def Briggs(self, ctx):
    #    """PS2 Server Status."""
    #    if self.BriggsTime == None or (datetime.datetime.now()-self.BriggsTime).total_seconds() > self.NewCheckTime:
    #        self.BriggsTime = datetime.datetime.now()
    #        MSG = await ctx.send(f'``{ctx.message.author.name}``', embed=PS2LoadEmbed)
    #        self.BriggsData = self.PS2EmbedGen(self.PS2WorldGrab("25"), "Briggs")
    #        await MSG.edit(content=f'``{ctx.message.author.name}``', embed=self.BriggsData)
    #    else:
    #        MSG = await ctx.send(f'``{ctx.message.author.name}`` ``CACHED``', embed=self.BriggsData, delete_after=32)
    #    await self.timed_delete(MSG)
    #    await self.timed_delete(ctx.message)


    @commands.command(aliases=['briggs', 'BRIGGS', 'bruggs', 'breggs', 'broggs', 'braggs'])
    async def Briggs(self, ctx):
        """PS2 Server Status."""
        MSG = await ctx.send(f'``{ctx.message.author.name}``', embed=PS2BriggsEmbed)
        await self.timed_delete(MSG)
        await self.timed_delete(ctx.message)


    @commands.command(pass_context=True, aliases=['connery', 'CONNERY'])
    async def Connery(self, ctx):
        """PS2 Server Status."""
        if self.ConneryTime == None or (datetime.datetime.now()-self.ConneryTime).total_seconds() > self.NewCheckTime:
            self.ConneryTime = datetime.datetime.now()
            MSG = await ctx.send(f'``{ctx.message.author.name}``', embed=PS2LoadEmbed)
            self.ConneryData = self.PS2EmbedGen(self.PS2WorldGrab("1"), "Connery")
            await MSG.edit(content=f'``{ctx.message.author.name}``', embed=self.ConneryData)
        else:
            MSG = await ctx.send(f'``{ctx.message.author.name}`` ``CACHED``', embed=self.ConneryData, delete_after=32)
        await self.timed_delete(MSG)
        await self.timed_delete(ctx.message)


    @commands.command(pass_context=True, aliases=['miller', 'MILLER'])
    async def Miller(self, ctx):
        """PS2 Server Status."""
        if self.MillerTime == None or (datetime.datetime.now()-self.MillerTime).total_seconds() > self.NewCheckTime:
            self.MillerTime = datetime.datetime.now()
            MSG = await ctx.send(f'``{ctx.message.author.name}``', embed=PS2LoadEmbed)
            self.MillerData = self.PS2EmbedGen(self.PS2WorldGrab("10"), "Miller")
            await MSG.edit(content=f'``{ctx.message.author.name}``', embed=self.MillerData)
        else:
            MSG = await ctx.send(f'``{ctx.message.author.name}`` ``CACHED``', embed=self.MillerData, delete_after=32)
        await self.timed_delete(MSG)
        await self.timed_delete(ctx.message)


    @commands.command(pass_context=True, aliases=['emerald', 'EMERALD'])
    async def Emerald(self, ctx):
        """PS2 Server Status."""
        if self.EmeraldTime == None or (datetime.datetime.now()-self.EmeraldTime).total_seconds() > self.NewCheckTime:
            self.EmeraldTime = datetime.datetime.now()
            MSG = await ctx.send(f'``{ctx.message.author.name}``', embed=PS2LoadEmbed)
            self.EmeraldData = self.PS2EmbedGen(self.PS2WorldGrab("17"), "Emerald")
            await MSG.edit(content=f'``{ctx.message.author.name}``', embed=self.EmeraldData)
        else:
            MSG = await ctx.send(f'``{ctx.message.author.name}`` ``CACHED``', embed=self.EmeraldData, delete_after=32)
        await self.timed_delete(MSG)
        await self.timed_delete(ctx.message)


    @commands.command(pass_context=True, aliases=['cobalt', 'COBALT', 'colbalt', 'COLBALT', 'Colbalt'])
    async def Cobalt(self, ctx):
        """PS2 Server Status."""
        if self.ColbaltTime == None or (datetime.datetime.now()-self.ColbaltTime).total_seconds() > self.NewCheckTime:
            self.ColbaltTime = datetime.datetime.now()
            MSG = await ctx.send(f'``{ctx.message.author.name}``', embed=PS2LoadEmbed)
            self.ColbaltData = self.PS2EmbedGen(self.PS2WorldGrab("13"), "Colbalt")
            await MSG.edit(content=f'``{ctx.message.author.name}``', embed=self.ColbaltData)
        else:
            MSG = await ctx.send(f'``{ctx.message.author.name}`` ``CACHED``', embed=self.ColbaltData, delete_after=32)
        await self.timed_delete(MSG)
        await self.timed_delete(ctx.message)


    @commands.command(pass_context=True, aliases=['jaeger', 'JAEGER'])
    async def Jaeger(self, ctx):
        """PS2 Server Status."""
        if self.JaegerTime == None or (datetime.datetime.now()-self.JaegerTime).total_seconds() > self.NewCheckTime:
            self.JaegerTime = datetime.datetime.now()
            MSG = await ctx.send(f'``{ctx.message.author.name}``', embed=PS2LoadEmbed)
            self.JaegerData = self.PS2EmbedGen(self.PS2WorldGrab("19"), "Jaeger")
            await MSG.edit(content=f'``{ctx.message.author.name}``', embed=self.JaegerData)
        else:
            MSG = await ctx.send(f'``{ctx.message.author.name}`` ``CACHED``', embed=self.JaegerData, delete_after=32)
        await self.timed_delete(MSG)
        await self.timed_delete(ctx.message)


    @commands.command(pass_context=True, aliases=['soltech', 'SOLTECH'])
    async def Soltech(self, ctx):
        """PS2 Server Status."""
        if self.SolTechTime == None or (datetime.datetime.now()-self.SolTechTime).total_seconds() > self.NewCheckTime:
            self.SolTechTime = datetime.datetime.now()
            MSG = await ctx.send(f'``{ctx.message.author.name}``', embed=PS2LoadEmbed)
            self.SolTechData = self.PS2EmbedGen(self.PS2WorldGrab("40"), "SolTech")
            await MSG.edit(content=f'``{ctx.message.author.name}``', embed=self.SolTechData)
        else:
            MSG = await ctx.send(f'``{ctx.message.author.name}`` ``CACHED``', embed=self.SolTechData, delete_after=32)
        await self.timed_delete(MSG)
        await self.timed_delete(ctx.message)


def setup(client):
    client.add_cog(Planetside(client))
