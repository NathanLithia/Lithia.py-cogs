import discord
from discord.ext import commands
import datetime
import ast
import subprocess

class Developers(commands.Cog):
    """Hidden Unboxed "Developers" Module for Lithia"""
    def __init__(self, client):
        self.client = client


    def insert_returns(self, body):
        if isinstance(body[-1], ast.Expr):
            body[-1] = ast.Return(body[-1].value)
            ast.fix_missing_locations(body[-1])
        if isinstance(body[-1], ast.If):
            self.insert_returns(body[-1].body)
            self.insert_returns(body[-1].orelse)
        if isinstance(body[-1], ast.With):
            self.insert_returns(body[-1].body)


    @commands.command(hidden=True, aliases=['eval', 'Eval', 'Eval_fn', 'sandbox'])
    @commands.is_owner()
    async def eval_fn(self, ctx, *, cmd):
        """Multi line Evaluation Tool"""
        fn_name = "_eval_expr"
        cmd = cmd.strip("` ")
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
        body = f"async def {fn_name}():\n{cmd}"
        parsed = ast.parse(body)
        body = parsed.body[0].body
        self.insert_returns(body)
        env = {
            'client': self.client,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__
        }
        try:
            exec(compile(parsed, filename="<ast>", mode="exec"), env)
            result = (await eval(f"{fn_name}()", env))
        except Exception as e:
            await ctx.reply(f'`🔴{type(e).__name__}` - {e}')
        if result == None:
            return
        else:
            await ctx.reply(result)


    @commands.command(hidden=True)
    @commands.is_owner()
    async def cmdOLD(self, ctx, *, inputs):
        """OLD Remote Terminal Access Tool"""
        result = subprocess.check_output(inputs.split())
        await ctx.reply(f'``{inputs.split()}``')
        trace = result.decode('utf-8')
        for chunk in [trace[i:i+1500] for i in range(0, len(trace), 1500)]: await ctx.reply(f"```{chunk}```")


    @commands.command(hidden=True, aliases=['CMD', 'term', 'terminal'])
    @commands.is_owner()
    async def cmd(self, ctx, *, inputs):
        """Remote Terminal Access Tool"""
        try:
            result = subprocess.check_output(inputs.split())
        except Exception as e:
            await ctx.reply(f'`🔴{type(e).__name__}` - {e}')
            return
        trace = result.decode('utf-8')
        self.Terminal_Embed=discord.Embed(color=0xc0c0c0)
        self.Terminal_Embed.set_footer(text=f"{inputs.split()}")
        fields = 0
        while fields <= 25:
            for chunk in [trace[i:i+2048] for i in range(0, len(trace), 2048)]:
                self.Terminal_Embed.add_field(name=f'Terminal Field: ``{fields}``', value=f'```{chunk}```')
                fields += 1
            break
        await ctx.reply(embed=self.Terminal_Embed)


def setup(client):
    client.add_cog(Developers(client))