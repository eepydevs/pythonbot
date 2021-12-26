#cog by Number1#4325
import disnake as discord
from disnake.ext import commands
import random
import asyncio
import math

class Text(commands.Cog):
  def __init__(self, bot):
    self.bot = bot  

  #lowcase command
  @commands.command(aliases = ["lcase"], help = "Low case your inputted text!", description = "Usage: pb!lowcase 'Hello World!'\nOutput: hello world!")
  async def lowcase(self, ctx, *, text):
    modtext = text.lower()
    await ctx.send(modtext)

  #highcase command
  @commands.command(aliases = ["hcase"], help = "High case your inputted text!", description = "Usage: pb!highcase 'hello world!'\nOutput: HELLO WORLD!")
  async def highcase(self, ctx, *, text):
    modtext = text.upper()
    await ctx.send(modtext)

  #spacecase command
  @commands.command(aliases = ["scase"], help = "Space case your inputted text!", description = "Usage: pb!spacecase 'hello world!'\nOutput: h e l l o  w o r l d !")
  async def spacecase(self, ctx, *, text):
    modtext = " ".join(text)
    await ctx.send(modtext)
  
  #titlecase command
  @commands.command(aliases = ["tcase"], help = "Title case your inputted text!", description = "Usage: pb!titlecase 'hello world!'\nOutput: Hello World!")
  async def titlecase(self, ctx, *, text):
    modtext = text.title()
    await ctx.send(modtext)

  #swapcase command
  @commands.command(aliases = ["spacec"], help = "Swap case your inputted text!", description = "Usage: pb!swapcase 'Hello World!'\nOutput: hELLO wORLD!")
  async def swapcase(self, ctx, *, text):
    modtext = text.swapcase()
    await ctx.send(modtext)

  #capitaizecase command
  @commands.command(aliases = ["capitalcase", "ccase"], help = "Capitalize your inputted text!", description = "Usage: pb!capitalcase 'hello world!'\nOutput: Hello world!")
  async def capitalizecase(self, ctx, *, text):
    modtext = text.capitalize()
    await ctx.send(modtext)

  #flip command
  @commands.command(help = "Flip your inputted text!", description = "Usage: pb!flipcase 'hello world!'\nOutput: world! hello")
  async def flipcase(self, ctx, *, text):
    textlist = text.split()
    textlist.reverse()
    textstring = " ".join(textlist)
    await ctx.send(textstring)
  
  #reverse command
  @commands.command(aliases = ["reverse", "rev"], help = "Reverse your inputted text!", description = "Usage: pb!reversecase 'hello world!'\nOutput: !dlrow olleh")
  async def reversecase(self, ctx, *, text):
    modtext = text[::-1]
    await ctx.send(modtext)

  #mixcase command
  @commands.command(aliases = ["mixc", "shufflecase"], help = "Mix your inputted text!", description = "Usage: pb!mixcase 'hello world'\nOutput: hleoe wrold!")
  async def mixcase(self, ctx, *, text):
    modtext = " ".join(str().join(random.sample(i, len(i))) for i in text.split())
    await ctx.send(modtext)

def setup(bot):
  bot.add_cog(Text(bot))