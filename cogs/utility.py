#cog by Number1#4325
import disnake as discord
from disnake.ext import commands
import random
import psutil
import os
import requests
import asyncio
import datetime, time
from replit import db

botbuild = "6.4.1" # major.sub.fix
pyver = "3.8.2"
dnver = "2.4.0"

waiquotes = ["Your cool", "Your pro", "I dont know who are you", "Your 228 iq", "Your The Le` Pro!", "Que pro", "You are the best!"]
reportblacklist = []
pollemojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"] #10 is the max 

if "afk" not in db:
  db["afk"] = {}

if "notes" not in db:
  db["notes"] = {}

if "reminders" not in db:
  db["reminders"] = {}

if "bot" not in db:
  db["bot"] = {}

if "bugcounter" not in db["bot"]:
  db["bot"]["bugcounter"] = 0

if "atr_log" not in db["bot"]:
  db["bot"]["atr_log"] = 0

async def suggest_note(inter, input):
  return [note for note in db['notes'][str(inter.author.id)].keys() if input.lower() in note.lower()][0:24]

async def suggest_user(inter, input):
  return [input] + [user.name for user in inter.bot.users if input.lower() in user.name.lower()][0:23] if input else [user.name for user in inter.bot.users if input.lower() in user.name.lower()][0:24]  

async def suggest_member(inter, input):
  return [input] + [member.name for member in inter.guild.members if input.lower() in member.name.lower() or input.lower() in member.display_name.lower()][0:23] if input else [member.name for member in inter.guild.members if input.lower() in member.name.lower() or input.lower() in member.display_name.lower()][0:24]

class Utility(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    bot.help_command.cog = self

  #context menu user info command
  @commands.user_command(name="User Info")  
  async def userinfo(self, inter, member: discord.Member):
      role_list = []

      for role in member.roles:
        if role.name != "@everyone":
          role_list.append(role.mention)
          
      role_list.reverse()
      b = ", ".join(role_list)
      e = discord.Embed(title = f"Member info: {member}", description = f"{member.mention}", color = random.randint(0, 16777215))
      if member.avatar != None:
        e.set_thumbnail(url = str(member.avatar))
      e.add_field(name = "Joined", value = f"<t:{str(time.mktime(member.joined_at.timetuple()))[:-2]}:R>", inline = True)
      e.add_field(name = "Registered", value = f"<t:{str(time.mktime(member.created_at.timetuple()))[:-2]}:R>", inline = True)
      if len(role_list) != 0:
        e.add_field(name = f"Roles ({len(role_list)}):", value = "".join([b]), inline = False)
      else:
        e.add_field(name = "Roles (0)", value = "None")
      if member.top_role != None:
        e.add_field(name = "Top role:", value = member.top_role.mention, inline = False)
      if member.guild_permissions.administrator:
        e.add_field(name = "Administrator?", value = "True", inline = False)
      else:
        e.add_field(name = "Administrator?", value = "False", inline = False)
      e.add_field(name = "Icon url:", value = f"[Link here]({str(member.avatar)[:-10]})", inline = False)
      e.set_footer(text = f"ID: {member.id}")
      await inter.send(embed = e)

  #context menu message info command
  @commands.message_command(name="Message Info") 
  async def msginfo(self, inter, message: discord.Message):
    e = discord.Embed(title = "Message info", description = f"Message ID: {message.id}\nChannel ID: {message.channel.id}\nServer ID: {message.guild.id}\n\nCreated at: <t:{str(time.mktime(message.created_at.timetuple()))[:-2]}:R>\nMessage author: {message.author.mention}\nMessage content: {message.content}\nLink: [Jump url]({message.jump_url})", color = random.randint(0, 16777215))
    await inter.response.send_message(embed = e, ephemeral = True)

  #ping command slash
  @commands.slash_command(name = "ping", description = "Shows bot's ping")
  async def slashping(inter):
    await inter.response.defer()
    try:
      url = "https://api.uptimerobot.com/v2/getMonitors"
      payload = "api_key=m789844302-2c9467e07ebf524406068312&format=json&custom_uptime_ratios=7-30"
      headers = {
      'content-type': "application/x-www-form-urlencoded",
      'cache-control': "no-cache"
      }
      response = requests.request("POST", url, data=payload, headers=headers)          
      resjson = response.json()
      customtimeratio = resjson['monitors'][0]['custom_uptime_ratio'].split('-')
      db["bot"]["atr_log"] = customtimeratio
    except:
      customtimeratio = db["bot"]["atr_log"]

    e = discord.Embed(title = "Pong!", description = f"Bot ping: {int(inter.bot.latency * 1000)}ms\nUp since: <t:{int(inter.bot.launch_time.timestamp())}:R>\nThis week's uptime ratio: `{customtimeratio[0]}%`\nThis month's uptime ratio: `{customtimeratio[1]}%`", color = random.randint(0, 16777215))
    if str(inter.author.id) in db["debug"]:
      e.add_field(name = "Debug", value = f"Variables value:\n{inter.bot.latency * 1000}, {inter.bot.launch_time.timestamp()}")
    await inter.edit_original_message(embed = e)

  #report bug command
  @commands.slash_command(name = "bugreport", description = "report bug")
  async def slashreport(inter, text):
    '''
    Report a bug to bot owner

    Parameters
    ----------
    text: Tell your bug here
    '''
    if str(inter.author.id) not in reportblacklist:
      with open("buglist.txt", "a") as report:
        db['bot']['bugcounter'] += 1
        report.write("\n")
        report.write(f"Bug #{db['bot']['bugcounter']}: {text} from {inter.author}")
        report.close()
      e = discord.Embed(title = "Success", description = f"Appended `Bug #{db['bot']['bugcounter']}: {text} from {inter.author}`", color = random.randint(0, 16777215))
      await inter.send(embed = e)
    else:
      e = discord.Embed(title = "Error", description = "Youre blacklisted", color = random.randint(0, 16777215))
      await inter.send(embed = e)

  """#remind command
  @commands.slash_command(name = "remind", description = "reminder")
  async def slashremind(inter, ctime = "1h", *, text):
    '''
    Make a reminder for yourself

    Parameters
    ----------
    ctime: Xh = X hours, Xd = X days, Xs = X seconds, Xm = X minutes | Default: 1h
    text: Your reminder here
    '''
    if ctime[:-1].isnumeric():
      if ctime[len(ctime) - 1] == "m":
        rtime = int(time.time()) + 60 * int(ctime[:-1])
      elif ctime[len(ctime) - 1] == "d":
        rtime = int(time.time()) + 86400 * int(ctime[:-1])
      elif ctime[len(ctime) - 1] == "s":
        rtime = int(time.time()) + int(ctime[:-1])
      elif ctime[len(ctime) - 1] == "h":
        rtime = int(time.time()) + 3600 * int(ctime[:-1])
    else:
      raise ValueError("Invalid argument: time")
    ruser = inter.author.id
    rtext = text
    db["reminders"][str(inter.author.id)] = {"rtext": rtext, "rid": ruser, "time": rtime}
    e = discord.Embed(title = "Success", description = f"Reminder done!\nWill remind you <t:{int(rtime)}:R>", color = random.randint(0, 16777215))
    if str(inter.author.id) in db["debug"]:
      e.add_field(name = "Debug", value = f"Variables value:\n{dict(db['reminders'][str(inter.author.id)])}")
    await inter.send(embed = e)"""
    
  #bot info command
  @commands.slash_command(name = "botinfo", description = "Shows bot's info")
  async def slashbotinfo(inter):
    await inter.response.defer()
    total_memory, used_memory, free_memory = map(
    int, os.popen('free -t -m').readlines()[-1].split()[1:])
    
    e = discord.Embed(title = "About Python Bot", description = f"Python Bot is a discord bot made by [Number1#4325](https://github.com/1randomguyspecial).",  color = random.randint(0, 16777215))
    e.add_field(name = "Bot", value = f"Total amount of commands: {len(tuple(command for command in inter.bot.commands if not command.hidden)) + len(inter.bot.slash_commands)}/{len(inter.bot.commands) + len(inter.bot.slash_commands)} ({len(inter.bot.commands) - len(tuple(command for command in inter.bot.commands if not command.hidden))} hidden) ({len(inter.bot.slash_commands)} slash)\nBot statistics:\n> Servers connected: `{len(inter.bot.guilds)}`\n> Users connected: `{len(inter.bot.users)}`\n> Channels connected: `{sum(len(i.channels) for i in inter.bot.guilds) - sum(len(i.categories) for i in inter.bot.guilds)}`")
    e.add_field(name = "Specs", value = f"CPU:\n> Cores: `{os.cpu_count()}`\n> Usage: `{psutil.getloadavg()[1]}%` (5 min avg)\n> Frequency: `{round(psutil.cpu_freq()[0])}Mhz`\nRAM:\n> Total: `1024MB`\n> Usage: `{psutil.virtual_memory()[2]}%` (virtual)\nOther:\n> Boot time: <t:{round(psutil.boot_time())}:R>", inline = False)
    e.add_field(name = "Links", value = "[Python Bot github page](https://github.com/1randomguyspecial/pythonbot)\n[Disnake github page](https://github.com/DisnakeDev/disnake)\n[Python official page](https://www.python.org)", inline = False)
    e.add_field(name = f"Versions", value = f"Bot: `{botbuild}`\nPython: `{pyver}`\nDisnake: `{dnver}`", inline = False)
    #e.add_field(name = f"Message from Number1", value = f"Leaving reality, see ya\n\*insert [almond cruise](https://www.youtube.com/watch?v=Cn6rCm01ru4) song here\*", inline = False)
    await inter.edit_original_message(embed = e)
  
  @commands.slash_command(name = "contributors", description = "Shows contributor list")
  async def credits(inter):
    e = discord.Embed(title = "Contributors list", description = "[icemay#6281](https://replit.com/@neonyt1) - Scripter, Helper, Tester\n[Bricked#7106](https://replit.com/@Bricked) - Scripter, Helper, Tester\n[Senjienji#8317](https://github.com/Senjienji) - Helper, Tester\n[Dark dot#5012](https://replit.com/@adthoughtsind) - Contributor, Tester\nflguynico#8706 - Contributor, Tester\nTjMat#0001 - Contributor\n[R3DZ3R#8150](https://github.com/R3DZ3R) - Contributor\nmillionxsam#4967 - Contributor\nRage#6456 - Tester", color = random.randint(0, 16777215))
    await inter.send(embed = e)

  #server info command
  @commands.slash_command(name = "serverinfo", description = "Shows server's info")
  async def serverinfo(inter):
    server_role_count = len(inter.guild.roles)
    list_of_bots = [bot.mention for bot in inter.guild.members if bot.bot]
    e = discord.Embed(title = f"Server info: {inter.guild.name}", description = f"Icon url: {str(inter.guild.icon)[:-10]}\nServer creation date: <t:{str(time.mktime(inter.guild.created_at.timetuple()))[:-2]}:R>", color = random.randint(0, 16777215))
    e.add_field(name = "Moderation", value = f"Server owner: {inter.guild.owner.name}\nVerification level: {str(inter.guild.verification_level)}\nNumber of roles: {server_role_count}")
    e.add_field(name = "Channels", value = f"Total: {len(inter.guild.channels) - len(inter.guild.categories)}\nText: {len(inter.guild.text_channels)}\nVoice: {len(inter.guild.voice_channels)}\nStage: {len(inter.guild.stage_channels)}")
    e.add_field(name = "Members", value = f"Total: {inter.guild.member_count}\nHumans: {inter.guild.member_count - len(list_of_bots)}\nBots: {len(list_of_bots)}")
    if inter.guild.icon != None:
      e.set_thumbnail(url = str(inter.guild.icon))
    e.set_footer(text = f"ID: {inter.guild.id}")
    await inter.send(embed = e)

  #suggest command
  @commands.slash_command(name = "suggest", description = "suggest")
  async def slashsuggest(inter, text):
    '''
    Suggest an improvement for server

    Parameters
    ----------
    text: Tell your suggestion here
    '''
    e = discord.Embed(title = f"Suggestion from: {inter.author}", description = f"{text}", color = random.randint(0, 16777215))
    e.set_thumbnail(url = str(inter.author.avatar))
    await inter.send(embed = e)
    msg = await inter.original_message()
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    await msg.add_reaction("❓")

  #invite command
  @commands.slash_command(name = "invite", description = "See invites  to bot support server and invite bot to your server")
  async def slashinvite(inter):
    e = discord.Embed(title = "Invites", description = "Click the buttons below!", color = random.randint(0, 16777215))
    view = discord.ui.View()
    style = discord.ButtonStyle.gray
    item = discord.ui.Button(style = style, label = "Invite bot to your server", url = "https://discord.com/api/oauth2/authorize?client_id=912745278187126795&permissions=1239702432855&scope=bot%20applications.commands")
    style1 = discord.ButtonStyle.gray
    item1 = discord.ui.Button(style = style1, label = "Invite to support server", url = "https://discord.gg/jRK82RNx73")
    view.add_item(item = item)
    view.add_item(item = item1)
    await inter.send(embed = e, view = view)
    
  #member info command
  @commands.slash_command(name = "whois", description = "Shows mentioned member's info")
  async def slashmemberinfo(inter, member: discord.Member = None):
    '''
    Shows mentioned member's info

    Parameters
    ----------
    member: Mention member
    '''
    if member != None:
      role_list = []

      for role in member.roles:
        if role.name != "@everyone":
          role_list.append(role.mention)
          
      role_list.reverse()
      b = ", ".join(role_list)
      e = discord.Embed(title = f"Member info: {member}", description = f"{member.mention}", color = random.randint(0, 16777215))
      if member.avatar != None:
        e.set_thumbnail(url = str(member.avatar))
      e.add_field(name = "Joined", value = f"<t:{str(time.mktime(member.joined_at.timetuple()))[:-2]}:R>", inline = True)
      e.add_field(name = "Registered", value = f"<t:{str(time.mktime(member.created_at.timetuple()))[:-2]}:R>", inline = True)
      if len(role_list) != 0:
        e.add_field(name = f"Roles ({len(role_list)}):", value = "".join([b]), inline = False)
      else:
        e.add_field(name = "Roles (0)", value = "None")
      if member.top_role != None:
        e.add_field(name = "Top role:", value = member.top_role.mention, inline = False)
      if member.guild_permissions.administrator:
        e.add_field(name = "Administrator?", value = "True", inline = False)
      else:
        e.add_field(name = "Administrator?", value = "False", inline = False)
      e.add_field(name = "Icon url:", value = f"[Link here]({str(member.avatar)[:-10]})", inline = False)
      e.set_footer(text = f"ID: {member.id}")
      await inter.send(embed = e)
    else:
      rgwai = waiquotes[random.randint(0, len(waiquotes) - 1)]
      role_list = []

      for role in inter.author.roles:
        if role.name != "@everyone":
          role_list.append(role.mention)

      role_list.reverse()
      b = ", ".join(role_list)
      e = discord.Embed(title = f"Member info: {inter.author}", description = f"{inter.author.mention}", color = random.randint(0, 16777215))
      if inter.author.avatar != None:
        e.set_thumbnail(url = str(inter.author.avatar))
      e.add_field(name = "Joined", value = f"<t:{str(time.mktime(inter.author.joined_at.timetuple()))[:-2]}:R>", inline = True)
      e.add_field(name = "Registered", value = f"<t:{str(time.mktime(inter.author.created_at.timetuple()))[:-2]}:R>", inline = True)
      if len(role_list) != 0:
        e.add_field(name = f"Roles ({len(role_list)}):", value = "".join([b]), inline = False)
      else:
        e.add_field(name = "Roles (0):", value = "None")
      if inter.author.top_role != None:
        e.add_field(name = "Top role:", value = inter.author.top_role.mention, inline = False)
      if inter.author.guild_permissions.administrator:
        e.add_field(name = "Administrator?", value = "True", inline = False)
      else:
        e.add_field(name = "Administrator?", value = "False", inline = False)
      e.add_field(name = "Icon url:", value = f"[Link here]({str(inter.author.avatar)[:-10]})", inline = False)
      e.add_field(name = "Quote:", value = f"{rgwai}")
      e.set_footer(text = f"ID: {inter.author.id}")
      await inter.send(embed = e)
       
  #emoji command
  @commands.slash_command(name = "emoji", description = "See emoji info")
  async def emoji(inter, emoji: discord.Emoji):
    '''
    See emoji info

    Parameters
    ----------
    emoji: Emoji here
    '''
    e = discord.Embed(title = f"Emoji info: {emoji.name}", description = f"Animated?: {'True' if emoji.animated else 'False'}\nCreated at: <t:{int(emoji.created_at.timestamp())}:F>\nFrom guild: {emoji.guild.name}\nLink: [Link here]({emoji.url})", color = random.randint(0, 16777215))
    e.set_image(url = emoji.url)
    e.set_footer(text = f"ID: {emoji.id}")
    await inter.send(embed = e)

  """#servers command
  @commands.slash_command(description = "See other servers' member counter")
  async def servers(inter):
    await inter.response.defer()
    counter = "\n".join(f"{index}. `{guild.name}` by `{guild.owner.name}`: {guild.member_count}" for index, guild in enumerate(sorted(inter.bot.guilds, key = lambda guild: guild.me.joined_at.timestamp()), start = 1))
    e = discord.Embed(title = "Servers' member counts:", description = f"Total: {len(inter.bot.users)}\n{counter}", color = random.randint(0, 16777215))
    await inter.send(embed = e)"""

  #afk command
  @commands.slash_command(name = "afk", description = "Set your afk and reason for it")
  async def slashafk(inter, reason = "None"):
      '''
      Set your afk and reason for it
  
      Parameters
      ----------
      reason: Reason for afk
      '''
      db["afk"][str(inter.author.id)] = {"reason": reason, "time": int(time.time())}
      e = discord.Embed(title = "AFK", description = f"Set your afk reason to `{reason}`", color = random.randint(0, 16777215))
      await inter.send(embed = e)

  #poll command
  @commands.slash_command(name = "poll", description = "Example: /poll Hello name! Hello option 1!, Hello option 2!, Hello option 3!")
  async def slashpoll(inter, name, options):
    '''
    Make a poll

    Parameters
    ----------
    name: Name of your poll
    options: Example: Hello option 1!, Hello option 2!, Hello option 3!
    '''  
    optionstuple = options.split(', ')[:10]
    e = discord.Embed(title = f"Poll from {inter.author.name}: {name}", description = '\n'.join(f'{pollemojis[i]} {optionstuple[i]}' for i in range(len(optionstuple))), color = random.randint(0, 16777215))
    #await inter.send("Successfully sent poll", ephemeral = True)
    await inter.send(embed = e)
    msg = await inter.original_message()
    for i in range(len(optionstuple)):
      await msg.add_reaction(pollemojis[i])

  #group smh
  @commands.slash_command(description = "Make notes with the bot (BETA)")
  async def note(self, inter):
    if str(inter.author.id) not in db["notes"]:
      db["notes"][str(inter.author.id)] = {}
  
  @note.sub_command(description = "Shows list of notes you have")
  async def list(self, inter):
    if str(inter.author.id) in db["notes"] and db["notes"][str(inter.author.id)] != {}:
      notes = "\n".join(f"{index}. `{name}`" for index, (name) in enumerate(db["notes"][str(inter.author.id)].keys(), start = 1))
      e = discord.Embed(title = f"{inter.author}'s notes:", description = notes, color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
    else:
      e = discord.Embed(title = f"Notes: {inter.author}", description = "You have nothing right now", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
  
  @note.sub_command(description = "Creates note")
  async def create(self, inter, name, text):
    '''
    Creates note

    Parameters
    ----------
    name: Note's name here
    text: Note's text here
    '''
    if str(inter.author.id) in db["notes"]:
      if name not in db["notes"][str(inter.author.id)]:
        if text != None:
          updatenotes = db["notes"][str(inter.author.id)]
          updatenotes[name] = text
          db["notes"][str(inter.author.id)] = updatenotes
          e = discord.Embed(title = "Success", description = f"Note named `{name}` is created!", color = random.randint(0, 16777215))
          await inter.send(embed = e, ephemeral = True)
        else:
          updatenotes = db["notes"][str(inter.author.id)]
          updatenotes[name] = "New note"
          db["notes"][str(inter.author.id)] = updatenotes
          e = discord.Embed(title = "Success", description = f"Note named `{name}` is created!", color = random.randint(0, 16777215))
          await inter.send(embed = e, ephemeral = True)
      else:
        e = discord.Embed(title = "Error", description = "This name is used!", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)
    else:
      if text != None:
        db["notes"][str(inter.author.id)] = {}
        updatenotes = db["notes"][str(inter.author.id)]
        updatenotes[name] = text
        db["notes"][str(inter.author.id)] = updatenotes
        e = discord.Embed(title = "Success", description = f"Note named `{name}` is created!", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)
      else:
        db["notes"][str(inter.author.id)] = {}
        updatenotes = db["notes"][str(inter.author.id)]
        updatenotes[name] = "New note"
        db["notes"][str(inter.author.id)] = updatenotes
        e = discord.Embed(title = "Success", description = f"Note named `{name}` is created!", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)
  
  @note.sub_command(description =  "Replaces whole note text")
  async def overwrite(inter, *, name: str = commands.Param(autocomplete = suggest_note), text):
    '''
    Replaces whole note text

    Parameters
    ----------
    name: Note's name here
    text: Note's text here, // to newline
    '''
    try:
      updatenotes = db["notes"][str(inter.author.id)]
      updatenotes[name] = text.replace("//", "\n")
      db["notes"][str(inter.author.id)] = updatenotes
      e = discord.Embed(title = "Success", description = f"Changed `{name}`'s text", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
    except KeyError:
      e = discord.Embed(title = f"Error", description = f"Note `{name}` doesn't exist", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

  @note.sub_command(description = "Inserts text at the end")
  async def add(self, inter, *, name: str = commands.Param(autocomplete = suggest_note), text):
    '''
    Inserts text at the end

    Parameters
    ----------
    name: Note's name here
    text: Note's text here
    '''
    try:
      updatenotes = db["notes"][str(inter.author.id)]
      updatenotes[name] += f" {text}"
      db["notes"][str(inter.author.id)] = updatenotes
      e = discord.Embed(title = "Success", description = f"Changed `{name}`'s text", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
    except KeyError:
      e = discord.Embed(title = f"Error", description = f"Note `{name}` doesn't exist", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

  @note.sub_command(description = "Inserts text at the end on new line")
  async def newline(self, inter, *, name: str = commands.Param(autocomplete = suggest_note), text):
    '''
    Inserts text at the end on new line

    Parameters
    ----------
    name: Note's name here
    text: Note's text here
    '''
    try:
      updatenotes = db["notes"][str(inter.author.id)]
      updatenotes[name] += f"\n{text}"
      db["notes"][str(inter.author.id)] = updatenotes
      e = discord.Embed(title = "Success", description = f"Changed `{name}`'s text", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
    except KeyError:
      e = discord.Embed(title = f"Error", description = f"Note `{name}` doesn't exist", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
  
  @note.sub_command(description = "Reads selected note")
  async def read(self, inter, *, name: str = commands.Param(autocomplete = suggest_note)):
    '''
    Reads selected note

    Parameters
    ----------
    name: Note's name here
    '''
    if name in db["notes"][str(inter.author.id)]:
      e = discord.Embed(title = f"Notes: {name}", description = f"{db['notes'][str(inter.author.id)].get(name)}", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
    else:
      e = discord.Embed(title = f"Error", description = f"Note `{name}` doesn't exist", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

  @note.sub_command(description = "Deletes selected note")
  async def delete(self, inter, *, name: str = commands.Param(autocomplete = suggest_note)):
    '''
    Deletes selected note

    Parameters
    ----------
    name: Note's name here
    '''
    if str(inter.author.id) in db["notes"]:
      if name != None:
        if name in db["notes"][str(inter.author.id)]:
          updatenotes = db["notes"][str(inter.author.id)]
          e = discord.Embed(title = "Success", description = f"Note named `{name}` is deleted!", color = random.randint(0, 16777215))
          await inter.send(embed = e, ephemeral = True)
          updatenotes.pop(name)
          db["notes"][str(inter.author.id)] = updatenotes
        else:
          e = discord.Embed(title = f"Error", description = f"Note `{name}` doesn't exist!", color = random.randint(0, 16777215))
          await inter.send(embed = e, ephemeral = True)
      else:
        e = discord.Embed(title = f"Error", description = "You can't delete nothing!", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)
    else:
      e = discord.Embed(title = f"Error", description = "You have no notes!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

  @note.sub_command(description = "Reads selected note but escapes markdown")
  async def read_raw(self, inter, *, name: str = commands.Param(autocomplete = suggest_note)):
    '''
    Reads selected note but escapes markdown

    Parameters
    ----------
    name: Note's name here
    '''
    if str(inter.author.id) in db["notes"]:
      if name in db["notes"][str(inter.author.id)]:
        text = db['notes'][str(inter.author.id)].get(name)
        rtext = text.replace('_', '\_').replace('*', '\*').replace('`', '\`').replace('~', '\~')
        e = discord.Embed(title = f"Notes: {name}", description = "`" + text.replace("\n", "//") + "`\n\n" + rtext, color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)
      else:
        e = discord.Embed(title = f"Error", description = f"Note `{name}` doesn't exist!", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)
    else:
      e = discord.Embed(title = f"Error", description = "You have no notes!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

  #exec command
  @commands.slash_command(name = "exec", description = "bot owner only")
  @commands.is_owner()
  async def slashexec(inter, code):
    '''
    bot owner only

    Parameters
    ----------
    code: Code here
    '''
    exec(code)
    print(f"{code} is executed")
    e = discord.Embed(title = "Success", description = f"`{code}` is executed!", color = random.randint(0, 16777215))
    await inter.send(embed = e, ephemeral = True)

  #quote command
  @commands.slash_command(name = "quote")
  async def quote(inter, text):
    '''
    Quote command or whatever idk

    Parameters
    ----------
    text: Your text here
    '''
    e = discord.Embed(title = "Quote", description = f"{text}", color = random.randint(0, 16777215))
    e.set_footer(text = f"{inter.author}", icon_url = str(inter.author.avatar))
    await inter.send(embed = e)

  #find command
  @commands.slash_command()
  async def find(self, inter):
    pass

  #find command
  @find.sub_command()
  async def user(self, inter, user: str = commands.Param(autocomplete = suggest_user)):
    '''
    Find a user i guess
    
    Parameters
    ----------
    user: User here
    '''
    result = []
    for member in inter.bot.users:
      if user.lower() in member.name.lower():
        name = member.name
        i = name.lower().find(user.lower())
        found = name.replace(name[i:len(user) + i], f"**__{name[i:len(user) + i]}__**")
        result.append(f"{found}\#{member.discriminator}{' `[BOT]`' if member.bot else ''}{' :beginner:' if member in inter.guild.members else ''}")
  
    fields, fi, mul = [[]], 0, 1
    for i, m in enumerate(result):
      if i == 20 * mul:
        fields.append([])
        fi += 1
        mul += 1
      else:
        fields[fi].append(m)
        
    e = discord.Embed(title = f"Searching for \"{user}\"", description = "This may be inaccurate\n🔰 = User is in this server", color = random.randint(0, 16777215))
    if result:
      for i, field in enumerate(fields, start = 1):
        e.add_field(name = f"Part {i}", value = "\n".join(field), inline = True)
    else:
      e.add_field(name = "No results found", value = "_ _")
    await inter.send(embed = e, ephemeral = True)

  @find.sub_command()
  async def member(self, inter, qmember: str = commands.Param(autocomplete = suggest_member)):
    '''
    Find a member in current server i guess
    
    Parameters
    ----------
    qmember: Member here
    '''
    result = []
    for member in inter.guild.members:
      if qmember.lower() in member.name.lower():
        name = member.name
        i = name.lower().find(qmember.lower())
        found = name.replace(name[i:len(qmember) + i], f"**__{name[i:len(qmember) + i]}__**")
        result.append(f"{found}\#{member.discriminator}{' `[BOT]`' if member.bot else ''}{' 🟢' if member.status == discord.Status.online else ''}{' 🟡' if member.status == discord.Status.idle else ''}{' 🔴' if member.status == discord.Status.dnd else ''}{' ⚫' if member.status == discord.Status.offline else ''}")
  
    fields, fi, mul = [[]], 0, 1
    for i, m in enumerate(result):
      if i == 20 * mul:
        fields.append([])
        fi += 1
        mul += 1
      else:
        fields[fi].append(m)
        
    e = discord.Embed(title = f"Searching for \"{qmember}\" in this server", description = "This may be inaccurate", color = random.randint(0, 16777215))
    if result:
      for i, field in enumerate(fields, start = 1):
        e.add_field(name = f"Part {i}", value = "\n".join(field), inline = True)
    else:
      e.add_field(name = "No results found", value = "_ _")
    await inter.send(embed = e, ephemeral = True)

def setup(bot):
  bot.add_cog(Utility(bot))