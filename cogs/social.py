import asyncio
import disnake as discord
import random
import os
import datetime, time
from replit import db
from disnake.ext import commands

if "account" not in db:
  db["account"] = {}

if "subs" not in db:
  db["subs"] = {}

class Social(commands.Cog):
  def __init__(self, bot):
    self.bot = bot  

  #add account command
  @commands.command(aliases = ["addacc"], help = "BETA")
  async def addaccount(self, ctx):
    if str(ctx.author.id) not in db["account"]:
      db["account"][str(ctx.author.id)] = {}
      db["subs"][str(ctx.author.id)] = []
      e = discord.Embed(title = "Success", description = "Account created!", color = random.randint(0, 16777215))
      await ctx.send(embed = e)
    else:
      e = discord.Embed(title = "Error", description = "You already have an account!", color = random.randint(0, 16777215))
      await ctx.send(embed = e)

  #post command
  @commands.command(help = "BETA", description = "Has cooldown of 10 minutes")
  @commands.cooldown(rate = 1, per = 600, type = commands.BucketType.user)
  async def post(self, ctx, name = "Sample", *, text = "Sample text"):
    if str(ctx.author.id) in db["account"]:
      updatedict = db["account"][str(ctx.author.id)]
      updatedict.update({name: text})
      db["account"][str(ctx.author.id)] = updatedict
      e = discord.Embed(title = "Success", description = f"You posted: `{name}: {text}`", color = random.randint(0, 16777215))
      await ctx.send(embed = e)
    else:
      e = discord.Embed(title = "Error", description = "Make an account!", color = random.randint(0, 16777215))
      await ctx.send(embed = e)
      ctx.command.reset_cooldown(ctx)

  #remove post command
  @commands.command(aliases = ["rpost"], help = "BETA")
  async def removepost(self, ctx, *, name = None):
    if str(ctx.author.id) in db["account"]:
      if name != None or name not in db["account"][str(ctx.author.id)]:
        updatedict = db["account"][str(ctx.author.id)]
        e = discord.Embed(title = "Success", description = f"Post named `{name}` is deleted!", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
        updatedict.pop(name)
        db["account"][str(ctx.author.id)] = updatedict
      else:
        e = discord.Embed(title = "Error", description = f"Post named `{name}` doesn't exist!", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
    else:
      e = discord.Embed(title = "Error", description = "Make an account!", color = random.randint(0, 16777215))
      await ctx.send(embed = e)

  #overview command
  @commands.command(aliases = ["ov"], help = "BETA")
  async def overview(self, ctx, member: discord.Member = None):
    if member != None:
      if str(member.id) in db["account"]:
        if len(dict(db["account"][str(member.id)])) != 0:
          posts = dict(db["account"][str(member.id)])
          list1 = list(posts.keys())
          list2 = list(posts.values())
          names = ""
          names = list1[0]
          texts = ""
          texts = list2[0]
          e = discord.Embed(title = f"{member.name}'s posts:", description = "posts here", color = random.randint(0, 16777215))
          e.add_field(name = names, value = texts)
          for i in range(len(list1) - 1):
            names = f"{list1[i + 1]}"
            texts = f"{list2[i + 1]}"
            e.add_field(name = names, value = texts)
          e.set_thumbnail(url = member.avatar)
          await ctx.send(embed = e)
        else:
          e = discord.Embed(title = f"{member.name}'s posts:", description = "posts here", color = random.randint(0, 16777215))
          e.set_thumbnail(url = member.avatar)
          e.add_field(name = "No posts here", value = "Check later!")
          await ctx.send(embed = e)
      else:
        e = discord.Embed(title = "Error", description = "They have no account...", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
    else:
      if str(ctx.author.id) in db["account"]:
        if len(dict(db["account"][str(ctx.author.id)])) != 0:
          posts = dict(db["account"][str(ctx.author.id)])
          list1 = list(posts.keys())
          list2 = list(posts.values())
          names = ""
          names = list1[0]
          texts = ""
          texts = list2[0]
          e = discord.Embed(title = f"{ctx.author.name}'s posts:", description = "posts here", color = random.randint(0, 16777215))
          e.add_field(name = names, value = texts)
          for i in range(len(list1) - 1):
            names = f"{list1[i + 1]}"
            texts = f"{list2[i + 1]}"
            e.add_field(name = names, value = texts)
          e.set_thumbnail(url = ctx.author.avatar)
          await ctx.send(embed = e)
        else:
          e = discord.Embed(title = f"{ctx.author.name}'s posts:", description = "posts here", color = random.randint(0, 16777215))
          e.set_thumbnail(url = ctx.author.avatar)
          e.add_field(name = "No posts here", value = "Check later!")
          await ctx.send(embed = e)
      else:
        e = discord.Embed(title = "Error", description = "You have no account...", color = random.randint(0, 16777215))
        await ctx.send(embed = e)

def setup(bot):
  bot.add_cog(Social(bot))