import asyncio
import disnake as discord
import random
import sys
import os
import datetime, time
from utils import RedisManager, PopcatAPI, Upload
from disnake.ext import commands
from dotenv import load_dotenv
from pp_calc import calc as pp
import subprocess
load_dotenv()

bot = commands.InteractionBot(intents=discord.Intents.all(), test_guilds = [1037736545211400313, 910131051320475648, 1008480558692712589, 1027278026154705046, 908099219401883670, 823959191894491206, 866689038731313193, 916407122474979398, 926443840632676412, 858300189358293037, 900579811544670218, 902248677891010641, 968171159776559174, 902970942173626378, 995060155848851537, 843562496543817778, 1004796648641273856, 1030182066052145283, 809722018953166858, 1030182066052145283, 1005108434779250779]) #, test_guilds = [1037736545211400313, 910131051320475648, 1008480558692712589, 1027278026154705046, 908099219401883670, 823959191894491206, 866689038731313193, 916407122474979398, 926443840632676412, 858300189358293037, 900579811544670218, 902248677891010641, 968171159776559174, 902970942173626378, 995060155848851537, 843562496543817778, 1004796648641273856, 1030182066052145283, 809722018953166858, 1030182066052145283, 1005108434779250779]

pyver = ".".join(str(i) for i in list(sys.version_info)[0:3])

with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
  if "afk" not in db:
    db["afk"] = {}

#on message event thing
@bot.event
async def on_message(message):
  if message.author.bot:
    return
  try:
    with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
      if str(message.author.id) in db["afk"]:
        if "serverid" in db["afk"][str(message.author.id)] and db["afk"][str(message.author.id)]["serverid"] != message.guild.id:
          if bot.get_guild(db["afk"][str(message.author.id)]["serverid"]).me.guild_permissions.manage_nicknames and bot.get_guild(db["afk"][str(message.author.id)]["serverid"]).me.top_role > message.author.top_role:
            await bot.get_guild(db["afk"][str(message.author.id)]["serverid"]).get_member(message.author.id).edit(nick = db["afk"][str(message.author.id)]["bname"])
        else:
          if message.guild.me.guild_permissions.manage_nicknames and message.guild.me.top_role > message.author.top_role:
            await message.author.edit(nick = db["afk"][str(message.author.id)]["bname"])
        del db["afk"][str(message.author.id)]
        await message.channel.send(f"Welcome back, {message.author.mention}", delete_after = 5)
      for member in message.mentions:
        if str(member.id) in db["afk"]: 
          e = discord.Embed(title = f"{member.name} is AFK", description = f"Reason: {db['afk'][str(member.id)]['reason']}\nSince: <t:{db['afk'][str(member.id)]['time']}:R>", color = random.randint(0, 16777215))
          await message.channel.send(embed = e)
        return
  except:
    pass

@bot.event
async def on_message_delete(message):
  try:
    with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:  
      if str(message.guild.id) in db["serversetting"]["gpd"]:
        if message.mentions:
          if not message.author.bot:
            e = discord.Embed(title = "Ghost ping detected!", description = f"{message.content}", color = random.randint(0, 16777215))
            e.set_footer(text = f"Message from: {message.author}")
            await message.channel.send(embed = e)
  except: pass

#when connected event lol
@bot.event
async def on_connection():
  bot.launch_time = datetime.datetime(1970, 1, 1)

#when bot is online event
@bot.event
async def on_ready():
  print("bot connected")
  await bot.change_presence(status = discord.Status.online, activity = discord.Game("Restarted"))
  bot.launch_time = datetime.datetime.utcnow()
  await asyncio.sleep(3)
  await bot.change_presence(status = discord.Status.online, activity = discord.Game(f"/ | Made in Python {pyver}!"))
  while True:
    with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
      if len(db["reminders"]) < 1:
        check = 1
      else:
        check = 0
      for i in range(len(db["reminders"]) - check):
        if int(time.time()) >= db["reminders"][list(db["reminders"].keys())[i]]["time"]:
          ruser = db["reminders"][list(db["reminders"].keys())[i]]["rid"]
          rtext = db["reminders"][list(db["reminders"].keys())[i]]["rtext"]
          e = discord.Embed(title = "Reminder", description = f"{rtext}", color = random.randint(0, 16777215))
          await bot.get_user(ruser).send(embed = e)
          del db["reminders"][list(db["reminders"].keys())[i]]
      await asyncio.sleep(10)

#load cogs
for filename in os.listdir('./cogs'):
  if filename.endswith('.py') and filename not in []:
    bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(os.environ["DISCORD_TOKEN"])