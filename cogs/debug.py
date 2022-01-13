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
  async def on_slash_command_error(self, inter, error):
    if isinstance(error, commands.CommandNotFound):
      return
    if not isinstance(error, commands.CommandOnCooldown):
      if not "Command raised an exception:" in str(error):
        e = discord.Embed(title = "Error", description = f"```{str(error)}```", color = random.randint(0, 16777215))
      else:
        e = discord.Embed(title = "Error", description = f"```{str(error)[29:]}```", color = random.randint(0, 16777215))
    else:
      e = discord.Embed(title = "Error", description = f"{str(error)[:31]} <t:{int(time.time() + error.retry_after)}:R>", color = random.randint(0, 16777215))
    await inter.send(embed = e, ephemeral = True)

  #debug command
  @commands.slash_command(name = "debug", description = "bot owner only")
  @commands.is_owner()
  async def slashdebug(inter, text = None):
    if text != None:
      if str(inter.author.id) not in db["debug"]:
        db["debug"][str(inter.author.id)] = "True"
        e = discord.Embed(title = "Success", description = "Debug mode enabled", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)
      else:
        del db["debug"][str(inter.author.id)]
        e = discord.Embed(title = "Success", description = "Debug mode disabled", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)
    else:
      if str(inter.author.id) in db["debug"]:
        e = discord.Embed(title = "Debug info", description = "Debug mode is enabled", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)
      else:
        e = discord.Embed(title = "Debug info", description = "Debug mode is disabled", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)

def setup(bot):
  bot.add_cog(Debug(bot))