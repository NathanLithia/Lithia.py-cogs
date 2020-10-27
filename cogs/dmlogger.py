from discord.ext import commands
import asyncio
import discord
import datetime
import os

class dmlogger(commands.Cog):
    def __init__(self, client):
        self.client = client


    def quickwrite(self, path, data):
        filename = path
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "a", encoding="utf-8") as f:
            f.write(data)


    def dmlog(self, message):
        if message.guild == None:
            self.quickwrite(f"./cogs/dmlogger/dm/{message.author.id}.log", f"\n[{datetime.datetime.utcnow()}][{message.author.name}]: {message.content}.")
        else:
            #self.quickwrite(f"./cogs/dmlogger/guild/{message.author.guild.id}/{message.channel.id}.log", f"\n[{datetime.datetime.utcnow()}][{message.author.name}]: {message.content}.")
            pass
        return


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == False:
            self.dmlog(message)


def setup(client):
    client.add_cog(dmlogger(client))
