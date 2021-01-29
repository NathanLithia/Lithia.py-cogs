import discord
from discord.ext import commands

class Versions(commands.Cog):
    """Hidden Development COG for Lithia"""
    def __init__(self, client):
        self.client = client
    
    def versioncheck(package):
        pass

def setup(client):
    client.add_cog(Versions(client))