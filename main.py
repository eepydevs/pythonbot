import asyncio
import disnake as discord
import random
import sys
import os
import datetime, time
from utils import PopcatAPI, Upload, db
from disnake.ext import commands, tasks
from dotenv import load_dotenv
from pp_calc import calc as pp
import topgg
import subprocess
load_dotenv()

bot = commands.InteractionBot(intents=discord.Intents.all()) #, test_guilds = [1037736545211400313, 910131051320475648, 1008480558692712589, 1027278026154705046, 908099219401883670, 823959191894491206, 866689038731313193, 916407122474979398, 926443840632676412, 858300189358293037, 900579811544670218, 902248677891010641, 968171159776559174, 902970942173626378, 995060155848851537, 843562496543817778, 1004796648641273856, 1030182066052145283, 809722018953166858, 1030182066052145283, 1005108434779250779]
bot.topgg = topgg.DBLClient(bot, os.environ["TOPGG"])

pyver = ".".join(str(i) for i in list(sys.version_info)[0:3])

if "afk" not in db:
  db["afk"] = {}

#on message event thing
@bot.event
async def on_message(message):
  if message.author.bot:
    return
  try:
    if str(message.author.id) in db["afk"]:
      if not "[afk]" in message.content.lower():
        if "serverid" in db["afk"][str(message.author.id)] and db["afk"][str(message.author.id)]["serverid"] != message.guild.id:
          if bot.get_guild(db["afk"][str(message.author.id)]["serverid"]).me.guild_permissions.manage_nicknames and bot.get_guild(db["afk"][str(message.author.id)]["serverid"]).me.top_role > message.author.top_role and message.author.roles[1:]:
            await bot.get_guild(db["afk"][str(message.author.id)]["serverid"]).get_member(message.author.id).edit(nick = db["afk"][str(message.author.id)]["bname"])
        else:
          if message.guild.me.guild_permissions.manage_nicknames and message.guild.me.top_role > message.author.top_role and message.author.roles[1:]:
            await message.author.edit(nick = db["afk"][str(message.author.id)]["bname"])
        await message.channel.send(f"Welcome back, {message.author.mention}", delete_after = 3)
        del db["afk"][str(message.author.id)]
    for member in message.mentions:
      if str(member.id) in db["afk"] and str(member.id) != str(message.author.id):
        e = discord.Embed(title = f"{member.name} is AFK", description = f"Reason: `{db['afk'][str(member.id)]['reason']}`\nSince: <t:{db['afk'][str(member.id)]['time']}:R>", color = random.randint(0, 16777215))
        await message.channel.send(embed = e)
      return
  except Exception:
    pass

@bot.event
async def on_message_delete(message):
  try:
    if str(message.guild.id) in db["serversetting"]["gpd"]:
      if message.mentions:
        if not message.author.bot:
          e = discord.Embed(title = "Ghost ping detected!", description = f"{message.content}", color = random.randint(0, 16777215))
          e.set_footer(text = f"Message from: {message.author}")
          await message.channel.send(embed = e)
  except Exception: pass

#when connected event lol
@bot.event
async def on_connection():
  bot.launch_time = datetime.datetime(1970, 1, 1)

#when bot is online event
@bot.event
async def on_ready():
  print("bot connected")
  await bot.change_presence(status = discord.Status.online, activity = discord.Game("Restarted"))
  bot.TP = list(bot.get_guild(910131051320475648).get_role(1098971358509154374).members)
  bot.DEV = list(bot.get_guild(910131051320475648).get_role(932937400706007060).members)
  bot.CONTRIB = list(bot.get_guild(910131051320475648).get_role(910131898376937502).members)
  try:
    db["ping"] = int(bot.latency * 1000)
  except Exception as e:
    print(f"{e.__class__.__name__}: {e}")
  bot.launch_time = datetime.datetime.utcnow()
  await asyncio.sleep(3)
  await bot.change_presence(status = discord.Status.online, activity = discord.Game(f"/ | Made in Python {pyver}!"))

@tasks.loop(seconds = 30)
async def update_reminders():
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

@tasks.loop(minutes = 30)
async def update_rolelists():
  try:
    bot.TP = list(bot.get_guild(910131051320475648).get_role(1098971358509154374).members)
    bot.DEV = list(bot.get_guild(910131051320475648).get_role(932937400706007060).members)
    bot.CONTRIB = list(bot.get_guild(910131051320475648).get_role(910131898376937502).members)
  except Exception as e:
    print(f"{e.__class__.__name__}: {e}")

@tasks.loop(minutes = 30)
async def top_gg_updstats():
  try:
    await bot.topgg.post_guild_count()
    print(f"Successfully updated guild count: {len(bot.guilds)}")
  except Exception as e:
    print(f"{e.__class__.__name__}: {e}")

@tasks.loop(seconds = 30)
async def update_ping():
  try:
    db["ping"] = int(bot.latency * 1000)
  except Exception as e:
    print(f"{e.__class__.__name__}: {e}")
    
#load cogs
for filename in os.listdir('./cogs'):
  if filename.endswith('.py') and filename not in []:
    bot.load_extension(f'cogs.{filename[:-3]}')

update_reminders.start()
if os.environ["TEST"] != "y":
  top_gg_updstats.start()
update_rolelists.start()
update_ping.start()
bot.run(os.environ["DISCORD_TOKEN"])
