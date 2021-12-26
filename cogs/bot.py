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

  #reset db command
  @commands.command(aliases = ["rdb", "r"], help = "Remove database/ database key", description = "bot owner only", hidden = True)
  @commands.is_owner()
  async def removedb(self, ctx, key = None):
    if key == None:
      await ctx.trigger_typing()
      global save
      save = {}
      for index in db.keys():
        save[index] = db[index]
        del db[index]
      e = discord.Embed(title = "Delete database: Success", description = "DB erased", color = random.randint(0, 16777215))
      await ctx.send(embed = e)
    else:
      try:
        del db[f"{key}"]
        e = discord.Embed(title = "Delete database key: Success", description = f"{key} Deleted", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
      except KeyError:
        e = discord.Embed(title = "Error", description = "Key doens't exist", color = random.randint(0, 16777215))
        await ctx.send(embed = e)

  #add db command
  @commands.command(aliases = ["adb", "a"], help = "Add database key", description = "bot owner only", hidden = True)
  @commands.is_owner()
  async def adddb(self, ctx, key = None, value = None):
    if key != None:
      db[f"{key}"] = value
      e = discord.Embed(title = "Add database key: Success", description = "Key added to the DB", color = random.randint(0, 16777215))
      await ctx.send(embed = e)

  #read db command
  @commands.command(aliases = ["redb", "re"], help = "Read database/database key", description = "bot owner only", hidden = True)
  @commands.is_owner()
  async def readdb(self, ctx, key = None):
    if key == None:
      keys = db.keys()
      e = discord.Embed(title = "Read database", description = f"{keys}", color = random.randint(0, 16777215))
      await ctx.send(embed = e)
    else:
      try:
        value = db[f"{key}"]
        e = discord.Embed(title = f"Read database: {key}", description = f"{db[key].value}", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
      except KeyError:
        value = "None"
        e = discord.Embed(title = f"Read database: {key} (doesn't exist)", description = f"{value}", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
  
  #set db command
  @commands.command(aliases = ["sdb"], help = "Set database key", description = "bot owner only", hidden = True)
  @commands.is_owner()
  async def setdb(self, ctx, key, value, type):
    try:
      if type == "int":
        test = db[f"{key}"]
        db[f"{key}"] = int(value)
        e = discord.Embed(title = "Set database key: Success", description = f"Set {key} to int({value})", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
      elif type == "str":
        test = db[f"{key}"]
        db[f"{key}"] = str(value)
        e = discord.Embed(title = "Set database key: Success", description = f"Set {key} to str({value})", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
    except KeyError:
      e = discord.Embed(title = "Error", description = "This key doesn't exist", color = random.randint(0, 16777215))
      await ctx.send(embed = e)
  
  #type db command
  @commands.command(aliases = ["tdb", "tydb"], help = "Set database key type", description = "bot owner only", hidden = True)
  @commands.is_owner()
  async def typedb(self, ctx, key, type):
    try:
      translate = db[f"{key}"]
      if type == "int":
        db[f"{key}"] = int(translate)
        e = discord.Embed(title = "Set database key type: Success", description = f"Set {key} type to {type}", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
      elif type == "str":
        db[f"{key}"] = str(translate)
        e = discord.Embed(title = "Set database key type: Success", description = f"Set {key} type to {type}", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
    except KeyError:
      e = discord.Embed(title = "Error", description = "This key doesn't exist", color = random.randint(0, 16777215))
      await ctx.send(embed = e)

  #undelete command
  @commands.command(aliases = ["undel", "undo"], help = "Undelete whole database or database key", description = "undelete whole database after accidental deletion", hidden = True)
  @commands.is_owner()
  async def undeldb(self, ctx, key = None):
    if key == None:
      await ctx.trigger_typing()
      for key in save:
        db[key] = save[key]
      e = discord.Embed(title = "Undelete database: Success", descirption = "Database deletion undone", color = random.randint(0, 16777215))
      await ctx.send(embed = e)
    else:
      db[key] = save[key]
      e = discord.Embed(title = "Undelete database key: Success", description = "Database key deletion undone", color = random.randint(0, 16777215))
      await ctx.send(embed = e)

  #shutdown command
  @commands.command(aliases = ["close", "shut", "down"], help = "Shutdown bot", hidden = True)
  @commands.is_owner()
  async def shutdown(self, ctx):
    e = discord.Embed(title = "Bot shutdown", description = "The owner shutdown the bot")
    await ctx.send(embed = e)
    quit()

  #exec command
  @commands.command(help = "Execute python code", description = "bot owner only", hidden = True)
  @commands.is_owner()
  async def exec(self, ctx, *, code):
    exec(code)
    print(f"{code} is executed")
    e = discord.Embed(title = "Success", description = f"`{code}` is executed!", color = random.randint(0, 16777215))
    await ctx.send(embed = e)

def setup(bot):
  bot.add_cog(Bot(bot))