#cog by maxy#2866
import disnake as discord
from disnake.ext import commands
import random
import psutil
import sys
import os
import requests
import asyncio
import datetime, time
from utils import dividers, db

botbuild = "10.8.0" # major.sub.minor/fix
pyver = ".".join(str(i) for i in list(sys.version_info)[0:3])
dnver = ".".join(str(i) for i in list(discord.version_info)[0:3])

reportblacklist = []
pollemojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"] #10 is the max

statusemotes = {
  "mobile": {
             "online": "<:mobonline:1073331669261623307>",
             "idle": "<:mobidle:1073331671371354252>",
             "dnd": "<:mobdnd:1073331651586830397>"
            },
  "desktop": {
              "online": "<:pconline:1073331654464127006>",
              "idle": "<:pcidle:1073331656322187364>",
              "dnd": "<:pcdnd:1073331659149164636>"
             },
  "web": {
          "online": "<:webonline:1073331661225332766>",
          "idle": "<:webidle:1073331664115216527>",
          "dnd": "<:webdnd:1073331666170429471>"
         }
}

if "notes" not in db:
  db["notes"] = {}

if "reminders" not in db:
  db["reminders"] = {}

def sbs(members):
  rval = {"offline": 0, "online": 0, "idle": 0, "dnd": 0}
  for m in members:
    if str(m.status) in rval:
      rval[str(m.status)] += 1
  return rval

async def suggest_note(inter, input):
  if str(inter.author.id) not in db["notes"]:
    db["notes"][str(inter.author.id)] = {}
  return [note for note in list(db['notes'][str(inter.author.id)].keys()) if input.lower() in note.lower()][0:24]

async def suggest_user(inter, input):
  return [input] + [user.name for user in inter.bot.users if input.lower() in user.name.lower()][0:23] if input else [user.name for user in inter.bot.users if input.lower() in user.name.lower()][0:24]  

async def suggest_member(inter, input):
  return [input] + [member.name for member in inter.guild.members if input.lower() in member.name.lower() or input.lower() in member.display_name.lower()][0:23] if input else [member.name for member in inter.guild.members if input.lower() in member.name.lower() or input.lower() in member.display_name.lower()][0:24]

async def suggest_bookmark(inter, input):
  if str(inter.author.id) not in db["bookmarks"]:
    db["bookmarks"][str(inter.author.id)] = {}
  return [bm for bm in list(db["bookmarks"][str(inter.author.id)].keys()) if input.lower() in bm.lower()][0:24] if db["bookmarks"][str(inter.author.id)] and [bm for bm in list(db["bookmarks"][str(inter.author.id)].keys()) if input.lower() in bm.lower()][0:24] else ["You have nothing! Go create a bookmark!"]

async def suggest_sbookmark(inter, input):
  if str(inter.author.id) not in db["bookmarks"]:
    db["bookmarks"][str(inter.author.id)] = {}
  return [input] + [bm for bm in list(db["bookmarks"][str(inter.author.id)].keys()) if input.lower() in bm.lower()][0:23] if db["bookmarks"][str(inter.author.id)] and [bm for bm in list(db["bookmarks"][str(inter.author.id)].keys()) if input.lower() in bm.lower()][0:24] else ["You have nothing! Go create a bookmark!"]

class rbbuttons(discord.ui.View):
  def __init__(self, inter: discord.Interaction, color, lb, rolename):
    super().__init__(timeout = 60)
    self.inter = inter
    self.page = 0
    self.color = color
    self.leaderboard = lb
    self.rn = rolename
    
  async def interaction_check(self, inter: discord.MessageInteraction):
    if inter.author != self.inter.author:
      await inter.send("Those buttons are not for you", ephemeral = True)
      return False
    return True

  @discord.ui.button(label = "", custom_id = "-10", emoji = "⬅️")
  async def arrowleft(self, button: discord.ui.Button, interaction = discord.MessageInteraction):
    self.page += int(interaction.data.custom_id)
    self.page = min(max(self.page, 0), len(self.leaderboard) // 10 * 10)
    e = discord.Embed(
      title = f"Role board: {self.rn}",
      description = "\n".join(self.leaderboard[self.page:self.page + 10]),
      color = self.color
    )
    if str(interaction.author.id) in db["debug"]:
      e.add_field(name = "Debug", value = f"Variables value:\n{self.page}")
    await interaction.response.edit_message(embed = e)

  @discord.ui.button(label = "", custom_id = "10", emoji = "➡️")
  async def arrowright(self, button: discord.ui.Button, interaction = discord.MessageInteraction):
    self.page += int(interaction.data.custom_id)
    self.page = min(max(self.page, 0), len(self.leaderboard) // 10 * 10)
    e = discord.Embed(
      title = f"Role board: {self.rn}"  ,
      description = "\n".join(self.leaderboard[self.page:self.page + 10]),
      color = self.color
    )
    if str(interaction.author.id) in db["debug"]:
      e.add_field(name = "Debug", value = f"Variables value:\n{self.page}")
    await interaction.response.edit_message(embed = e)

class Utility(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  #x reaction
  @commands.Cog.listener()
  async def on_reaction_add(self, reaction, user):
    if reaction.message.author == self.bot.user and reaction.emoji == "❌" and (user.guild_permissions.manage_messages or user.id == 439788095483936768):
      await reaction.message.delete()

  #context menu message info command
  @commands.message_command(name="Message Info") 
  async def msginfo(self, inter, message: discord.Message):
    e = discord.Embed(title = "Message info", description = f"Message ID: {message.id}\nChannel ID: {message.channel.id}\nServer ID: {message.guild.id}\n\nCreated at: <t:{str(time.mktime(message.created_at.timetuple()))[:-2]}:R>\nMessage author: {message.author.mention}\nMessage content: {message.content}\nLink: [Jump url]({message.jump_url})", color = random.randint(0, 16777215))
    await inter.response.send_message(embed = e, ephemeral = True)

  @commands.message_command(name="Add bookmark") 
  async def addbm(self, inter, msgid: discord.Message):
    await inter.response.defer(ephemeral = True)
    if str(inter.author.id) not in db["bookmarks"]:
      db["bookmarks"][str(inter.author.id)] = {}

    if str(msgid.id) in db["bookmarks"][str(inter.author.id)]:
      e = discord.Embed(title = "Error", description = "A bookmark with name already exists", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return

    msg = await inter.bot.get_channel(msgid.channel.id).fetch_message(msgid.id)
    db["bookmarks"][str(inter.author.id)].update({str(msgid.id): {"items": {"content": msg.content, "jumpurl": msg.jump_url}}})
    e = discord.Embed(title = "Success", description = f"Added `{msgid.id}`", color = random.randint(0, 16777215))
    await inter.edit_original_response(embed = e)

  @commands.slash_command()
  async def bookmarks(self, inter):
    if str(inter.author.id) not in db["bookmarks"]:
      db["bookmarks"][str(inter.author.id)] = {}
    
  @bookmarks.sub_command()
  async def add(self, inter, *, bmname = None, msgid: discord.Message):
    '''
    Add a message to your bookmarks (private pins)
    
    Parameters
    ----------
    bmname: Name of bookmark
    msgid: Message id to pin
    '''
    if bmname is None:
      bmname = str(msgid.id)
    if bmname in db["bookmarks"][str(inter.author.id)]:
      e = discord.Embed(title = "Error", description = "A bookmark with name already exists", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return

    msg = await inter.bot.get_channel(msgid.channel.id).fetch_message(msgid.id)
    db["bookmarks"][str(inter.author.id)].update({bmname: {"items": {"content": msg.content, "jumpurl": msg.jump_url}}})
    e = discord.Embed(title = "Success", description = f"Added `{msgid.id}` as `{bmname}`", color = random.randint(0, 16777215))
    await inter.send(embed = e, ephemeral = True)

  @bookmarks.sub_command()
  async def remove(self, inter, bmname: str = commands.Param(autocomplete = suggest_bookmark)):
    '''
    Remove a pinned message in your bookmarks (private pins)
    
    Parameters
    ----------
    bmname: Name of bookmark
    '''
    if bmname not in db["bookmarks"][str(inter.author.id)]:
      e = discord.Embed(title = "Error", description = "Invalid bookmark name: Bookmark doesn't exist", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return

    upd = db["bookmarks"]
    del upd[str(inter.author.id)][bmname]
    db["bookmarks"] = upd
    e = discord.Embed(title = "Success", description = f"Removed `{bmname}`", color = random.randint(0, 16777215))
    await inter.send(embed = e, ephemeral = True)

  @bookmarks.sub_command()
  async def show(self, inter, bmname: str = commands.Param(autocomplete = suggest_bookmark)):
    '''
    See a pinned message in your bookmarks (private pins)
    
    Parameters
    ----------
    bmname: Name of bookmark
    '''
    if bmname not in db["bookmarks"][str(inter.author.id)]:
      e = discord.Embed(title = "Error", description = "Invalid bookmark name: Bookmark doesn't exist", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    e = discord.Embed(title = f"Bookmark: {bmname}", description = db["bookmarks"][str(inter.author.id)][bmname]["items"]["content"], color = random.randint(0, 16777215), url = db["bookmarks"][str(inter.author.id)][bmname]["items"]["jumpurl"])
    await inter.send(embed = e, ephemeral = True)

  #remind command
  @commands.slash_command()
  async def remind(self, inter):
    pass

  @remind.sub_command()
  async def add(self, inter, days: int = 0, hours: int = 0, minutes: int = 0, *, text):
    '''
    Make a reminder for yourself
    
    Parameters
    ----------
    days: Amount of days to wait | Default: 0
    hours: Amount of hours to wait | Default: 1
    minutes: Amount of minutes to wait | Default: 0
    text: Your reminder here
    '''
    if not any([days, hours, minutes]): hours = 1
    rtime = int(time.time()) + 86400 * days + 3600 * hours + 60 * minutes
    ruser = inter.author.id
    rtext = text
    db["reminders"][str(inter.author.id)] = {"rtext": rtext, "rid": ruser, "time": rtime}
    e = discord.Embed(title = "Success", description = f"Reminder done!\nWill remind you <t:{int(rtime)}:R>", color = random.randint(0, 16777215))
    if str(inter.author.id) in db["debug"]:
      e.add_field(name = "Debug", value = f"Variables value:\n{dict(db['reminders'][str(inter.author.id)])}")
    await inter.send(embed = e)


  @remind.sub_command()
  async def remove(self, inter):
    '''
    Remove the reminder you made
    '''
    e = discord.Embed(title = "Error", description = f"Reminder deleted", color = random.randint(0, 16777215))
    if str(inter.author.id) in db["reminders"]:
      del db["reminders"][str(inter.author.id)]
      e = discord.Embed(title = "Success", description = f"Reminder deleted", color = random.randint(0, 16777215))
      await inter.send(embed = e)
      return
    e = discord.Embed(title = "Error", description = f"Reminder is not found", color = random.randint(0, 16777215))
    await inter.send(embed = e, ephemeral = True)

  #afk command
  @commands.slash_command(name = "afk", description = "Set your afk and reason for it")
  async def slashafk(inter, reason = "None"):
      '''
      Set your afk and reason for it
  
      Parameters
      ----------
      reason: Reason for afk
      '''
      cond = False
      if "[AFK]" not in inter.author.nick or str(inter.author.id) not in db["afk"]:
        cond = True
      db["afk"][str(inter.author.id)] = {"reason": reason[0:127], "time": int(time.time())}
      if inter.guild.me.guild_permissions.manage_nicknames and inter.guild.me.top_role > inter.author.top_role and inter.author.roles[1:]:
        if cond:
          db["afk"][str(inter.author.id)].update({"bname": (str(inter.author.nick) if inter.author.nick else str(inter.author.name)), "serverid": inter.guild.id})
          await inter.author.edit(nick = f"[AFK] {str(inter.author.nick) if inter.author.nick else str(inter.author.name)}"[0:31])
      e = discord.Embed(title = "AFK", description = f"Set your afk reason to `{reason[0:127]}`" + ("\n> Warning: You can use only 128 characters as AFK reason" if len(reason) > 128 else "") + "\n> Tip: Add a `[afk]` anywhere in your message to stay afk but still write", color = random.randint(0, 16777215))
      await inter.send(embed = e)

  #bot group
  @commands.slash_command()
  async def bot(self, inter):
    pass
  
  #bot info command
  @bot.sub_command(name = "info", description = "Shows bot's info")
  async def slashbotinfo(self, inter):
    await inter.response.defer()
    
    e = discord.Embed(title = "About Python Bot", description = f"Python Bot is a discord bot made by [maxy#2866](https://github.com/1randomguyspecial).",  color = random.randint(0, 16777215))
    e.add_field(name = "Bot", value = f"Total amount of commands: {len(inter.bot.slash_commands)}\nBot statistics:\n> Servers connected: `{len(inter.bot.guilds)}`\n> Users connected: `{len(inter.bot.users)}`\n> Channels connected: `{sum(len(i.channels) for i in inter.bot.guilds) - sum(len(i.categories) for i in inter.bot.guilds)}`")
    e.add_field(name = "Specs", value = f"Host: `{'Local (PC)' if os.environ['HOSTTYPE'] == '0' else 'Railway.app' if os.environ['HOSTTYPE'] == '1' else 'Daki.cc'}`\nCPU:\n> Cores: `{os.cpu_count()}`\n> Usage: `{'%.1f'%([x / psutil.cpu_count() * 100 for x in psutil.getloadavg()][1])}%` (5 min avg)\n> Frequency: `{round(psutil.cpu_freq()[0])}Mhz`\nRAM:\n> Virtual:\n> - Total: `{round(psutil.virtual_memory()[0] / 1024 / 1024)}MB`\n> - Usage: `{round(psutil.virtual_memory()[3] / 1024 / 1024)}MB / {'%.1f'%(psutil.virtual_memory()[2])}%`\n> - Free: `{round(psutil.virtual_memory()[1] / 1024 / 1024)}MB / {'%.1f'%(100 - psutil.virtual_memory()[2])}%`" + (f"\n> Swap: \n> - Total: `{round(psutil.swap_memory()[0] / 1024 / 1024)}MB`\n> - Usage: `{round(psutil.swap_memory()[1] / 1024 / 1024)}MB / {'%.1f'%(psutil.swap_memory()[3])}%`\n> - Free: `{round(psutil.swap_memory()[2] / 1024 / 1024)}MB / {'%.1f'%(100 - psutil.swap_memory()[3])}%`" if round(psutil.swap_memory()[0] / 1024 / 1024) else "") + f"\nOther:\n> Boot time: <t:{round(psutil.boot_time())}:R>", inline = False)
    e.add_field(name = "Links", value = "[⚡ Support me on Boosty!](https://boosty.to/number1)\n[⚡ Support me on DonationAlerts!](https://www.donationalerts.com/r/maxy1)\n[🖥️ Python Bot Github page](https://github.com/1randomguyspecial/pythonbot)\n[📄 Python Bot To-Do board](https://github.com/users/1randomguyspecial/projects/2)\n[🧰 Disnake Github page](https://github.com/DisnakeDev/disnake)\n[🐍 Python official page](https://www.python.org)", inline = False)
    e.add_field(name = f"Versions", value = f"Bot: `{botbuild}`\nPython: `{pyver}`\nDisnake: `{dnver}`", inline = False)
    #e.add_field(name = f"Message from Number1", value = f"Leaving reality, see ya\n\*insert [almond cruise](https://www.youtube.com/watch?v=Cn6rCm01ru4) song here\*", inline = False)
    await inter.edit_original_message(embed = e)

  #bot ping command
  @bot.sub_command(name = "ping", description = "Shows bot's ping")
  async def slashping(self, inter):
    s4dutilping = -1
    fshping = -1
    await inter.response.defer()
    if inter.guild.id == 866689038731313193 and not inter.guild.get_member(1030156986140074054).status == discord.Status.offline:
      try:
        await inter.guild.get_channel(1077214640754405417).send(f"Requested by: `{inter.author.name}#{inter.author.discriminator}`")
        await inter.guild.get_channel(1077214640754405417).send(f"s4d!check")
        message = await inter.bot.wait_for("message", check = lambda message: message.author.id == 1030156986140074054 and message.channel.id == 1077214640754405417 and not message.embeds, timeout = 3)
        s4dutilping = message.content
      except asyncio.TimeoutError:
        s4dutilping = -1
    fshexist = inter.guild.get_member(1068572316986003466)
    if fshexist and not fshexist.status == discord.Status.offline:
      fshping = int(requests.get("https://fsh-bot.frostzzone.repl.co/api/ping?plain=1").json())
    e = discord.Embed(title = "Pong!", description = f"Bot ping: `{int(inter.bot.latency * 1000)}ms`" + (f"\n> `{abs(int(s4dutilping) - int(inter.bot.latency * 1000))}ms` {'more' if int(s4dutilping) < int(inter.bot.latency * 1000) else 'less'} than S4D Utilities" if int(s4dutilping) >= 0 else "\n> `S4D Utilities` Unavailable..." if inter.guild.id == 866689038731313193 else "") + (f"\n> `{abs(fshping - int(inter.bot.latency * 1000))}ms` {'more' if fshping < int(inter.bot.latency * 1000) else 'less'} than Fsh" if fshping >= 0 else "\n> `Fsh` Unavailable..." if fshexist else "") + f"\nUp since: <t:{int(inter.bot.launch_time.timestamp())}:R>", color = random.randint(0, 16777215))
    await inter.send(embed = e)

  #bot credits command
  @bot.sub_command(name = "credits", description = "Shows contributor list")
  async def credits(self, inter):
    e = discord.Embed(title = "Contributors/credits list", description = "[Bricked#7106](https://replit.com/@Bricked) - Scripter, Helper, Tester\n[Senjienji#8317](https://github.com/Senjienji) - Helper, Tester\n[Dark dot#5012](https://replit.com/@adthoughtsind) - Contributor, Tester\nflguynico#8706 - Contributor, Tester\n[R3DZ3R#8150](https://github.com/R3DZ3R) - Contributor\nmillionxsam#4967 - Contributor\n\nfsh for being fsh still fshing and continuing to fsh\n**Devs of fsh:**\n> `frostzzone#4486`\n> `inventionpro#6814`\n> `LarsIsHere#3320`", color = random.randint(0, 16777215))
    await inter.send(embed = e)

  @bot.sub_command(description = "Shows side projects im working on")
  async def sideprojects(self, inter):
    e = discord.Embed(title = "Side projects im working on", description = "Some of projects may not be mine", color = random.randint(0, 16777215))
    e.add_field(name = "Telicards [BOT] (by Telcaum#9774)", value = "> PVP Card game\nIm a `Dev` and `Designer`\n[Invite it to your server](https://discord.com/api/oauth2/authorize?client_id=1069308287239077898&permissions=277025769536&scope=applications.commands%20bot)\n[Support server](https://discord.gg/6X7hGMMPAv)", inline = False)
    e.add_field(name = "Fsh [BOT] (by frostzzone#4486, inventionpro#6814)", value = "> Fsh this bot!! Its Fshing Fsh!!!\nIm `Inspiration` and a `Helper`\n[Invite it to your server](https://discord.com/api/oauth2/authorize?client_id=1068572316986003466&permissions=8&scope=applications.commands%20bot)\nNo support server", inline = False)
    await inter.send(embed = e)
    
  @commands.slash_command()
  async def server(self, inter):
    pass

  #server info command
  @server.sub_command(name = "info", description = "Shows server's info")
  async def serverinfo(self, inter):
    server_role_count = len(inter.guild.roles)
    list_of_bots = [bot.mention for bot in inter.guild.members if bot.bot]
    ms = sbs(inter.guild.members)
    e = discord.Embed(title = f"Server info: {inter.guild.name}", description = f"Icon url: {str(inter.guild.icon)[:-10]}\nServer creation date: <t:{str(time.mktime(inter.guild.created_at.timetuple()))[:-2]}:R>", color = random.randint(0, 16777215))
    e.add_field(name = "Moderation", value = f"Server owner: {inter.guild.owner.mention}\nVerification level: {str(inter.guild.verification_level)}\nNumber of roles: {server_role_count}")
    e.add_field(name = "Channels", value = f"Total: {len(inter.guild.channels) - len(inter.guild.categories)}\nText: {len(inter.guild.text_channels)}\nVoice: {len(inter.guild.voice_channels)}\nStage: {len(inter.guild.stage_channels)}")
    e.add_field(name = "Members", value = f"Total: {inter.guild.member_count}\n> ⚫ {ms['offline']}\n> 🟢 {ms['online']}\n> 🟡 {ms['idle']}\n> 🔴 {ms['dnd']}\nPeople: {inter.guild.member_count - len(list_of_bots)}\nBots: {len(list_of_bots)}")
    if inter.guild.icon != None:
      e.set_thumbnail(url = str(inter.guild.icon))
    e.set_footer(text = f"ID: {inter.guild.id}")
    await inter.send(embed = e)

  #role info command
  @server.sub_command(name = "roleinfo", description = "Shows role's info")
  async def roleinfo(self, inter, role: discord.Role):
    e = discord.Embed(title = f"Role info: {role.name}", description = f"{role.mention}\n\nRole position: {-role.position + len(inter.guild.roles)}\nRole creation date: <t:{str(time.mktime(role.created_at.timetuple()))[:-2]}:R>\nCan be mentioned by other users?: {role.mentionable}\nIs separated from other roles?: {role.hoist}\n{('Icon link: ' + role.icon.url) if role.icon != None else ''}", color = role.color)
    if len(role.members) != 0:
      rm = '\n'.join([f"{m}" for m in role.members[0:9]])
      e.add_field(name = f"{len(role.members) if len(role.members) < 10 else f'More than 10 ({len(role.members)})'} People have this role:", value = rm)
    if role.icon != None:
      e.set_thumbnail(url = role.icon.url)
    e.set_footer(text = f"ID: {role.id}")
    await inter.send(embed = e)

  #hasrole command
  @server.sub_command()
  async def hasrole(self, inter, role: discord.Role):
    '''
    Shows how much people has the selected role
    
    Parameters
    ----------
    role: Role here
    '''
    board = tuple(f"{index}. `{member}`" for index, member in enumerate(role.members, start = 1))
    color = role.color
    e = discord.Embed(title = f"Role board: {role.name}", description = "\n".join(board[0:9]), color = color)
    await inter.send(embed = e, view = rbbuttons(inter, color, board, role.name))

  #suggest command
  @server.sub_command(name = "suggest")
  async def slashsuggest(self, inter, text):
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

  #member info command
  @server.sub_command(name = "whois", description = "Shows mentioned member's info")
  async def slashmemberinfo(self, inter, member: discord.Member = None):
    '''
    Shows mentioned member's info
    Parameters
    ----------
    member: Mention member
    '''
    if member == None:
      member = inter.author
      
    role_list = []

    for role in member.roles:
      if role.name != "@everyone":
        role_list.append(role.mention)
          
    role_list.reverse()
    b = ", ".join(role_list)
    e = discord.Embed(title = f"Member info: {member} ({dividers([statusemotes['desktop'].get(str(member.desktop_status).lower(), '') if str(member.desktop_status) != 'offline' else None, statusemotes['mobile'].get(str(member.mobile_status).lower(), '') if str(member.mobile_status) != 'offline' else None, statusemotes['web'].get(str(member.web_status).lower(), '') if str(member.web_status) != 'offline' else None])}{'⚫' if member.status == discord.Status.offline else ''})", description = f"{member.mention}", color = random.randint(0, 16777215))
    if member.avatar != None:
      e.set_thumbnail(url = str(member.avatar))
    e.add_field(name = "Joined", value = f"<t:{str(time.mktime(member.joined_at.timetuple()))[:-2]}:R>", inline = True)
    e.add_field(name = "Registered", value = f"<t:{str(time.mktime(member.created_at.timetuple()))[:-2]}:R>", inline = True)
    if member.activity != None:
      e.add_field(name = "Activity", value = f"{member.activity.type[0].capitalize()} **{member.activity.name}**", inline = False)
    if len(role_list) != 0:
      e.add_field(name = f"Roles ({len(role_list)}):", value = "".join([b]) if len("".join([b])) < 1024 else "Too many roles to show", inline = False)
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
       
  #emoji command
  @server.sub_command(name = "emoji", description = "See emoji info")
  async def emoji(self, inter, emoji: discord.Emoji):
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
    
  #poll command
  @server.sub_command(name = "poll", description = "Example: /poll Hello name! Hello option 1!, Hello option 2!, Hello option 3!")
  async def slashpoll(self, inter, name, options):
    '''
    Make a poll
    Parameters
    ----------
    name: Name of your poll
    options: Example: Hello option 1!, Hello option 2!, Hello option 3!
    '''  
    optionstuple = options.split(',')[:10]
    e = discord.Embed(title = f"Poll from {inter.author.name}: {name}", description = '\n'.join(f'{pollemojis[i]} {optionstuple[i].strip()}' for i in range(len(optionstuple))), color = random.randint(0, 16777215))
    #await inter.send("Successfully sent poll", ephemeral = True)
    await inter.send(embed = e)
    msg = await inter.original_message()
    for i in range(len(optionstuple)):
      await msg.add_reaction(pollemojis[i])

  #invite command
  @commands.slash_command(name = "invite", description = "See invites  to bot support server and invite bot to your server")
  async def slashinvite(inter):
    e = discord.Embed(title = "Invites", description = "Click the buttons below!", color = random.randint(0, 16777215))
    view = discord.ui.View()
    style = discord.ButtonStyle.gray
    item = discord.ui.Button(style = style, label = "Invite bot to your server", url = "https://discord.com/api/oauth2/authorize?client_id=912745278187126795&permissions=1239836650583&scope=bot%20applications.commands")
    item1 = discord.ui.Button(style = style, label = "Invite to support server", url = "https://discord.gg/jRK82RNx73")
    item2 = discord.ui.Button(style = style, label = "Invite to Guilded support server", url = "https://www.guilded.gg/i/keNWeOPp?cid=bec0dc7b-4b97-41c7-aaa4-513d3e53f5e7&intent=chat")
    view.add_item(item = item)
    view.add_item(item = item1)
    view.add_item(item = item2)
    await inter.send(embed = e, view = view)

  """#servers command
  @commands.slash_command(description = "See other servers' member counter")
  async def servers(inter):
    await inter.response.defer()
    counter = "\n".join(f"{index}. `{guild.name}` by `{guild.owner.name}`: {guild.member_count}" for index, guild in enumerate(sorted(inter.bot.guilds, key = lambda guild: guild.me.joined_at.timestamp()), start = 1))
    e = discord.Embed(title = "Servers' member counts:", description = f"Total: {len(inter.bot.users)}\n{counter}", color = random.randint(0, 16777215))
    await inter.send(embed = e)"""

  #group smh
  @commands.slash_command(description = "Make notes with the bot")
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
  @commands.is_owner()
  async def user(self, inter, user: str = commands.Param(autocomplete = suggest_user)):
    '''
    Find a user i guess (owner only)
    
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
        result.append(f"{found}\#{member.discriminator}{' `[BOT]`' if member.bot else ''} {dividers([statusemotes['desktop'].get(str(member.desktop_status).lower(), '') if str(member.desktop_status) != 'offline' else None, statusemotes['mobile'].get(str(member.mobile_status).lower(), '') if str(member.mobile_status) != 'offline' else None, statusemotes['web'].get(str(member.web_status).lower(), '') if str(member.web_status) != 'offline' else None], ', ')}{'⚫' if member.status == discord.Status.offline else ''}")
  
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