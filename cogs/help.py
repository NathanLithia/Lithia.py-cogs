from discord.ext import commands
import discord


#This custom help command is a perfect replacement for the default one on any Discord client written in Discord.py!
#However, you must put "client.remove_command('help')" in your client, and the command must be in a cog for it to work.
#Written by Jared Newsom (AKA Jared M.F.)!

#this cog is broken af --NathanLithia


class Helper(commands.Cog):
    """Help Commands for Lithia"""
    def __init__(self, client):
        self.client = client
        self.client.remove_command('help')


    @commands.command(pass_context=True, aliases=['Help'])
    @commands.has_permissions(add_reactions=True,embed_links=True)
    async def help(self,ctx,*cog):
        """Retrieves all Cogs and Cog Commands."""
        try:
            if not cog:
                """Cog listing.  What more?"""
                halp=discord.Embed(title='Cog Listing', description=f'Use `{self.client.prefixes[0]}help *cog*` to find out more about them!\n***(CASE SeNsAtIvE will be fixed soon!)***')
                cogs_desc = ''
                for x in self.client.cogs:
                    if str(self.client.cogs[x].__doc__).startswith('hidden') or str(self.client.cogs[x].__doc__).startswith('Hidden') == False:
                        cogs_desc += ('⚙️ ``{}`` {}'.format(x,self.client.cogs[x].__doc__)+'\n')
                halp.add_field(name='Cogs',value=f"{cogs_desc[0:len(cogs_desc)-1]}",inline=False)
                await ctx.message.add_reaction(emoji='✉')
                await ctx.message.author.send(embed=halp)
            else:
                """Helps me remind you if you pass too many args."""
                if len(cog) > 1:
                    halp = discord.Embed(title='Error!',description='That is way too many cogs!',color=discord.Color.red())
                    await ctx.message.author.send('',embed=halp)
                else:
                    """Command listing within a cog."""
                    found = False
                    for x in self.client.cogs:
                        for y in cog:
                            if x == y:
                                halp=discord.Embed(title=f'\⚙️  {cog[0]} Command Listing',description=self.client.cogs[cog[0]].__doc__)
                                for c in self.client.get_cog(y).get_commands():
                                    if not c.hidden:
                                        halp.add_field(name=c.name,value=f'```{c.help}```',inline=False)
                                found = True
                    if not found:
                        """Reminds you if that cog doesn't exist."""
                        halp = discord.Embed(title='Error!',description='How do you even use "'+cog[0]+'"?',color=discord.Color.red())
                    else:
                        await ctx.message.add_reaction(emoji='✉')
                    await ctx.message.author.send('',embed=halp)
        except Exception as e: await ctx.reply(f'{e}')


def setup(client):
    client.add_cog(Helper(client))