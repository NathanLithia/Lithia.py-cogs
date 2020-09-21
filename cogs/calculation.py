import discord
from discord.ext import commands
import base64
import hashlib
#from tabulate import tabulate # pip install tabulate

HASH_TYPES = ['SHA1', 'SHA256', 'MD5']
FORMAT_TYPES = ['TABLE']
ENCODE_TYPES = ['BASE85', 'BASE64', 'BASE32', 'BASE16']
DECODE_TYPES = [] + ENCODE_TYPES

#https://stackoverflow.com/questions/17166074/most-efficient-way-of-making-an-if-elif-elif-else-statement-when-the-else-is-don

class Calculation(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(pass_context=True, aliases=['form', 'format'])
    async def Format(self, ctx, TYPE: str = None, *, INPUT: str = None):
        if TYPE == "TABLE":
            await ctx.send(f"{INPUT}")
            print(tabulate(INPUT))
            await ctx.send(f"{type(INPUT)}")
        else:
            await ctx.send(f"the method '{TYPE}' is not available, see {self.client.prefix}Format types") 


    @commands.command(pass_context=True, aliases=['encrypt'])
    async def Encrypt(self, ctx, key: str = None, *, data: str = "Hello World"):
        enc = []
        for i in range(len(data)):
            key_c = key[i % len(key)]
            enc_c = chr((ord(data[i]) + ord(key_c)) % 256)
            enc.append(enc_c)
        await ctx.send(base64.urlsafe_b64encode("".join(enc).encode()).decode("utf8"))

    @commands.command(pass_context=True, aliases=['decrypt'])
    async def Decrypt(self, ctx, key: str = None, *, enc: str = None):
        dec = []
        enc = base64.urlsafe_b64decode(enc).decode("utf8")
        for i in range(len(enc)):
            key_c = key[i % len(key)]
            dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        await ctx.send("".join(dec))

    @commands.command(pass_context=True, description='Base Encoder, Usage: ', aliases=['be', 'baseencode', 'encode'])
    async def Encode(self, ctx, TYPE: str = None, *, INPUT: str = None):
        """| Encodes inputs into a variety of formats """
        if TYPE == "BASE85":
            await ctx.send(str(base64.b85encode(bytes(INPUT, 'utf-8')))[2:-1])
        elif TYPE == "BASE64":
            await ctx.send(str(base64.b64encode(bytes(INPUT, 'utf-8')))[2:-1])
        elif TYPE == "BASE32":
            await ctx.send(str(base64.b32encode(bytes(INPUT, 'utf-8')))[2:-1])
        elif TYPE == "BASE16":
            await ctx.send(str(base64.b16encode(bytes(INPUT, 'utf-8')))[2:-1])
        elif TYPE == "types":
            await ctx.send(f"Encoding types: {ENCODE_TYPES}")
        else:
            await ctx.send(f"the method '{TYPE}' is not available, see {self.client.prefix}Encode types") 


    @commands.command(pass_context=True, description='Base Decoder, Usage: ', aliases=['bd', 'basedecode', 'decode'])
    async def Decode(self, ctx, TYPE: str = None, *, INPUT: str = None):
        """| Decodes a variety of inputs"""
        if TYPE == "BASE85":
            await ctx.send(str(base64.b85decode(bytes(INPUT, 'utf-8')))[2:-1])
        elif TYPE == "BASE64":
            await ctx.send(str(base64.b64decode(bytes(INPUT, 'utf-8')))[2:-1])
        elif TYPE == "BASE32":
            await ctx.send(str(base64.b32decode(bytes(INPUT, 'utf-8')))[2:-1])
        elif TYPE == "BASE16":
            await ctx.send(str(base64.b16decode(bytes(INPUT, 'utf-8')))[2:-1])
        elif TYPE == "types":
            await ctx.send(f"Decoding types: {DECODE_TYPES}")
        else:
            await ctx.send(f"the method '{TYPE}' is not available, see {self.client.prefix}Decode types")


    @commands.command(pass_context=True, no_pm=False, description='Base Hasher, Usage: ', aliases=['hash', 'hsh'])
    async def Hash(self, ctx, TYPE: str = None, *, INPUT: str = None):
        """| Hashes inputs into a variety of formats """
        if TYPE == "MD5":
            await ctx.send(str(hashlib.md5(bytes(INPUT, 'utf-8')).hexdigest()))
        elif TYPE == "SHA256":
            await ctx.send(str(hashlib.sha256(bytes(INPUT, 'utf-8')).hexdigest()))
        elif TYPE == "SHA1":
            await ctx.send(str(hashlib.sha1(bytes(INPUT, 'utf-8')).hexdigest()))
        elif TYPE == "types":
            await ctx.send(f"Hashing types: {HASH_TYPES}")
        else:
            await ctx.send(f"the method '{TYPE}' is not available, see {self.client.prefix}Hash types")


    @commands.command(pass_context=True, no_pm=False, description='Embedded Calculator, try >calculate 5*5 bop', aliases=['calculate', 'compute', 'calc', 'math'])
    async def Calculate(self, ctx, *, message: str = None):
        """| Commit mathematical calculations."""
        mathswhitelist=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ')', '(', '-', '=', '+', '/', '<', '>', '*', '.', ' ', '^', '!', '~', '&', '|', '%', ','] # https://stackoverflow.com/a/46799212
        if message == None:
            return await ctx.send(f"{self.client.prefix}calc 13.411/4.267```diff\n- 13.411/4.267\n+ 3.14295758143895```")
        if any(x not in mathswhitelist for x in message):
            return await ctx.send("Error. illegal expression.")
        else:
            try:
                calculation = str('```diff\n- '+str(message)+'\n+ '+str(eval(message))+'```')
            except OverflowError:
                return await ctx.send("Error. overflow error.")
            except SyntaxError:
                return await ctx.send("Error. syntax error.")
            except ZeroDivisionError:
                return await ctx.send("Error. cannot divide by zero.")
            except TypeError:
                return await ctx.send("Error, TypeError")
            if len(calculation) > 2000:
                return await ctx.send("Error, calculation exceeds 2000 characters.")
            else:
                await ctx.send(calculation)


def setup(client):
    client.add_cog(Calculation(client))