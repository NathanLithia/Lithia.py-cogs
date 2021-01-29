from discord.ext import commands
import discord

class messages(commands.Cog):
    """Hidden Message Handle for Lithia"""
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_message(self, message): 
        pass


def setup(client):
    client.add_cog(messages(client))