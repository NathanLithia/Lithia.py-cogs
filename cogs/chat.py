from discord.ext import commands
import discord
import random

class Chat(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(pass_context=True, aliases=['say'])
    async def Say(self, ctx, message: str = None):
        """| Repeats text."""
        try:
            await ctx.reply(str(ctx.message.content).split('say', 1)[1])
        except Exception as e: await ctx.send(f'{e}')


    @commands.command(pass_context=True, aliases=['roll'])
    async def Roll(self, ctx, dice : str):
        """| Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.reply('Format has to be in NdN!')
            return
        if limit >= 1000 or rolls >= 1000:
            await ctx.reply('Too much! try rolling less')
            return
        evaldata = ' + '.join(str(random.randint(1, limit)) for r in range(rolls))
        total = eval(evaldata)
        dicevalue = evaldata.replace(' + ', '+')
        if len(dicevalue) >= 1000:
            dicevalue = 'Dice data exceeds 1000 character limit for embed fields!'
        rollembed=discord.Embed()
        rollembed.set_thumbnail(url="https://emojipedia-us.s3.amazonaws.com/thumbs/120/emoji-one/104/game-die_1f3b2.png")
        rollembed.add_field(name='Dice Rolls', value=f"```{dicevalue}```", inline=True)
        rollembed.add_field(name='Data', value=f'``Total:`` {total}\n``Rolls:`` {rolls}\n``Sides:`` {limit}', inline=True)
        await ctx.reply(embed=rollembed)


    @commands.command(description='For when you wanna settle the score some other way', aliases=['choose'])
    async def Choose(self, ctx, *choices : str):
        """| Chooses between multiple choices."""
        await ctx.reply(random.choice(choices))


    @commands.command(pass_context=True, aliases=['invite'])
    async def Invite(self, ctx, client_id = 309600524125339659):
        """| Send invitation links"""
        await ctx.reply(f"Here's the invitation link.\n<https://discord.com/oauth2/authorize?client_id={client_id}&scope=bot>")


    @commands.command(pass_context=True, aliases=['ping'])
    async def Ping(self, ctx):
        """| Pong!"""
        await ctx.reply(f"{ctx.message.author.mention} Pong!")


    @commands.command(pass_context=True, hidden=True, aliases=['pong'])
    async def Pong(self, ctx):
        """| Ping!"""
        await ctx.reply(f"{ctx.message.author.mention} Ping!")


    @commands.command(pass_context=True, hidden=True, aliases=['commands'])
    async def command_redirect(self, ctx):
        """| Redirect message for people listening to client status"""
        await ctx.reply(f"You can view my commands with >help")



def setup(client):
    client.add_cog(Chat(client))