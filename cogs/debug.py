#cog by @maxy_dev (maxy#2866)
import asyncio
import sys
import disnake as discord
import random
import os
from main import bot
from enum import Enum
import datetime, time
from disnake.ext import commands
from utils import db

if "debug" not in db:
  db["debug"] = {}

class Required1(str, Enum):
  true = "True"
  false = ""

class Debug(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  #when slash error
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
    await inter.send(embed = e)

  #debug group
  @commands.slash_command()
  async def debug(self, inter):
    pass

  @debug.sub_command()
  @commands.is_owner()
  async def toggle(self, inter, toggler: Required1 = Required1.true):
    '''
    debug,,

    Parameters
    ----------
    text: None
    '''
    if str(inter.author.id) not in db["debug"] and toggler:
      db["debug"][str(inter.author.id)] = "True"
      e = discord.Embed(title = "Success", description = "Debug mode enabled", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    if str(inter.author.id) in db["debug"] and not toggler:
      del db["debug"][str(inter.author.id)]
      e = discord.Embed(title = "Success", description = "Debug mode disabled", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

        
  #load extension command
  @debug.sub_command()
  @commands.is_owner()
  async def load(self, inter, extension):
    '''
    Loads an extension

    Parameters
    ----------
    extension: Cog name
    '''
    bot.load_extension(f"cogs.{extension}")
    await inter.send(f"cogs.{extension} is loaded", ephemeral = True)
    
  #reload extension command
  @debug.sub_command()
  @commands.is_owner()
  async def reload(self, inter, extension):
    '''
    Loads an extension

    Parameters
    ----------
    extension: Cog name
    '''
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    await inter.send(f"cogs.{extension} is reloaded", ephemeral = True)
  
  #unload extension command
  @debug.sub_command()
  @commands.is_owner()
  async def unload(self, inter, extension):
    '''
    Loads an extension

    Parameters
    ----------
    extension: Cog name
    '''
    bot.unload_extension(f"cogs.{extension}")
    await inter.send(f"cogs.{extension} is unloaded", ephemeral = True)
    
  #restart bot
  # @debug.sub_command()
  # @commands.is_owner()
  # async def restart(self, inter):
  #   '''
  #   Restarts the bot
  #   '''
  #   await inter.send("Restarting", ephemeral = True)
  #   before = time.perf_counter()
  #   await bot.close()
  #   await bot.login(os.environ["DISCORD_TOKEN"])
  #   after = time.perf_counter()
  #   await inter.edit_original_message(f"Restarted, took `{round((after - before) * 1000)}`ms")
    
  @debug.sub_command()
  @commands.is_owner()
  async def shutdown(self, inter):
    '''
    Shutdowns the bot
    '''
    await inter.send("Shutdown", ephemeral = True)
    try:
      await bot.close()
    except Exception:
      print("something went wrong")
    sys.exit()
    
def setup(bot):
  bot.add_cog(Debug(bot))