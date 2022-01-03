#cog by Number1#4325
import asyncio
import disnake as discord
import random
import os
import datetime, time
from replit import db
from disnake.ext import commands

if "debug" not in db:
  db["debug"] = {}

class Debug(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  #when error event
  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.CommandNotFound):
      return
    e = discord.Embed(title = "Error", description = f"Triggered by: `{ctx.message.content}` from {ctx.author}\n```{error}```", color = random.randint(0, 16777215))
    await ctx.send(embed = e)

  #debug command
  @commands.command(help = "Shows debug info", description = "bot owner only", hidden = True)
  @commands.is_owner()
  async def debug(self, ctx, text = None):
    if text != None:
      if str(ctx.author.id) not in db["debug"]:
        db["debug"][str(ctx.author.id)] = "True"
        e = discord.Embed(title = "Success", description = "Debug mode enabled", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
      else:
        del db["debug"][str(ctx.author.id)]
        e = discord.Embed(title = "Success", description = "Debug mode disabled", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
    else:
      if str(ctx.author.id) in db["debug"]:
        e = discord.Embed(title = "Debug info", description = "Debug mode is enabled", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
      else:
        e = discord.Embed(title = "Debug info", description = "Debug mode is disabled", color = random.randint(0, 16777215))
        await ctx.send(embed = e)

def setup(bot):
  bot.add_cog(Debug(bot))