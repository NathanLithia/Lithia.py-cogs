from discord.ext import tasks, commands
from itertools import cycle
import asyncio, discord, sys

class Status(commands.Cog):
    """Hidden Cog for cycling status displays for Lithia"""
    def __init__(self, client):
        self.client = client
        self.status = cycle([f'Python {sys.version_info.major}.{sys.version_info.minor}', f'{self.client.prefixes[0]}Commands', 'NathanLithia.tk'])

    @commands.Cog.listener()
    async def on_ready(self):
        self.status_task.start()

    def cog_unload(self):
        self.status_task.cancel()

    @tasks.loop(seconds=32.0)
    async def status_task(self):
        await self.client.change_presence(status=discord.Status.dnd, activity=discord.Game(next(self.status)))

    @status_task.before_loop
    async def before_status_task(self):
        await self.client.wait_until_ready()

def setup(client):
    client.add_cog(Status(client))