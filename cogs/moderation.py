#cog by Number1#4325
import disnake as discord
from disnake.ext import commands
import asyncio
import random
from replit import db

purgequotes = ["Stop spamming!", "Spamming is bad.", "Purge the chat! Haha!", "Purge after these silly young spammers...", "Is it just me, or is spamming more likely now than notime else?"]
modquotes = ["I hope they learned their lesson.", "Make them cry!", "Haha!", "Gotcha!", "They should've readed the rules.", "Why they didn't readed the rules...", "That's lesson for you to read rules!", "'no reason ban' they say... Right at your eyes broke rule number 1337!", "Oops!"]

if "prefix" not in db:
  db["prefix"] = {}

if "warns" not in db:
  db["warns"] = {}

if "serversetting" not in db:
  db["serversetting"] = {}
  db["serversetting"]["gpd"] = {}
  db["serversetting"]["antiscam"] = {}

class Moderation(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  #kick command
  @commands.slash_command(name = "kick", description = "Kick mentioned member")
  @commands.has_permissions(kick_members = True)
  @commands.bot_has_permissions(kick_members = True)
  async def slashkick(inter, member: discord.Member): 
    e = discord.Embed(title = "Pwned!", description = f"You were kicked from server {inter.guild.name}", color = random.randint(0, 16777215))
    e.set_thumbnail(url = str(inter.guild.icon))
    await member.send(embed = e)
    
    await member.kick()
    kquote = modquotes[random.randint(0, len(modquotes) - 1)]
    e = discord.Embed(title = "Success", description = f"Successfully kicked {member.mention}! {kquote}", color = random.randint(0, 16777215))
    await inter.send(embed = e)

  #ban command
  @commands.slash_command(name = "ban", description = "Ban mentioned people")
  @commands.has_permissions(ban_members = True)
  @commands.bot_has_permissions(ban_members = True)
  async def ban(inter, member: discord.Member, *, reason = None):
    e = discord.Embed(title = "Banned!", description = f"You were banned from server {inter.guild.name}", color = random.randint(0, 16777215))
    e.set_thumbnail(url = str(inter.guild.icon))
    await member.send(embed = e)

    await member.ban(reason = reason)
    bquote = modquotes[random.randint(0, len(modquotes) - 1)]
    e = discord.Embed(title = "Success", description = f"Successfully banned {member.mention}! {bquote}", color = random.randint(0, 16777215))
    await inter.send(embed = e)

  #timeout command
  @commands.slash_command(name = "timeout", description = "Mute/Timeout mentioned member")
  @commands.has_permissions(moderate_members = True)
  @commands.bot_has_permissions(moderate_members = True)
  async def slashtimeout(inter, member: discord.Member, duration = "1d"):
    if duration.endswith("d"):
      timeoutduration = 86400 * int(duration[:-1])
      await member.timeout(duration = timeoutduration)
      e = discord.Embed(title = f"{member.name} Got timeout", description = f"Duration {int(duration[:-1])} days", color = random.randint(0, 16777215))
      await inter.send(embed = e)
    elif duration.endswith("s"):
      timeoutduration = int(duration[:-1])
      await member.timeout(duration = timeoutduration)
      e = discord.Embed(title = f"{member.name} Got timeout", description = f"Duration: {int(duration[:-1])} seconds", color = random.randint(0, 16777215))
      await inter.send(embed = e)
    elif duration.endswith("h"):
      timeoutduration = 3600 * int(duration[:-1])
      await member.timeout(duration = timeoutduration)
      e = discord.Embed(title = f"{member.name} Got timeout", description = f"Duration: {int(duration[:-1])} hours", color = random.randint(0, 16777215))
      await inter.send(embed = e)
    elif duration.endswith("m"):
      timeoutduration = 60 * int(duration[:-1])
      await member.timeout(duration = timeoutduration)
      e = discord.Embed(title = f"{member.name} Got timeout", description = f"Duration: {int(duration[:-1])} minutes", color = random.randint(0, 16777215))
      await inter.send(embed = e)

  #unban command
  @commands.slash_command(name = "unban", description = "Unban peole")
  @commands.has_permissions(ban_members = True)
  @commands.bot_has_permissions(ban_members = True)
  async def unban(inter, member: discord.Member, *, reason = None):
    e = discord.Embed(title = "Unbanned!", description = f"You were unbanned from server {inter.guild.name}", color = random.randint(0, 16777215))
    e.set_thumbnail(url = str(inter.guild.icon))
    await member.send(embed = e)

    await member.unban(reason = reason)
    e = discord.Embed(title = "Success", description = f"Successfully unbanned {member.mention}!", color = random.randint(0, 16777215))
    await inter.send(embed = e)

  #purge command
  @commands.slash_command(name = "purge", description = "Purge messages")
  @commands.has_permissions(manage_channels = True)
  @commands.bot_has_permissions(manage_channels = True)
  async def slashpurge(inter, num1: int):
    if num1 > 0:
      if num1 <= 100:
        await inter.message.delete()
        await asyncio.sleep(1)
        await inter.channel.purge(limit = num1)
        pquote = purgequotes[random.randint(0, len(purgequotes) - 1)]
        e = discord.Embed(title = "Success", description = f"Purged the channel successfully! {pquote}", color =  random.randint(0, 16777215))
        await inter.send(embed = e, delete_after = 5)
        #await asyncio.sleep(5)
        #await m.delete()
      else:
        await inter.send("❌ Please insert a number under 100")
    else:
      await inter.send("❌ Please insert a number above 0")

  #pin command
  @commands.command(help = "Pin a message", description = "This is useless command don't use it\nUsage: Reply a message and type pb!pin\nUsage 2: pb!pin (message id)")
  @commands.has_permissions(manage_channels = True)
  @commands.bot_has_permissions(manage_channels = True)
  async def pin(self, ctx, message: discord.Message = None):
    if message == None and ctx.message.reference.resolved != None:
      await ctx.message.reference.resolved.pin()
    else:
      await message.pin()

  #prefix command
  @commands.slash_command(name = "prefix", description = "See current prefix or change it")
  async def slashprefix(inter, prefix = None):
    if inter.author.guild_permissions.administrator or inter.author.id == inter.bot.owner.id:
      if not prefix:
        e = discord.Embed(title = "Prefix", description = f"Current prefix is: `{db['prefix'][str(inter.guild.id)]}`", color = random.randint(0, 16777215))
        await inter.send(embed = e)
      else:
        if len(prefix) > 5:
          db["prefix"][str(inter.guild.id)] = prefix[:5]
          e = discord.Embed(title = "Prefix", description = f"Prefix got changed to: `{prefix[:5]}`", color = random.randint(0, 16777215))
          await inter.send(embed = e)
        else:
          db["prefix"][str(inter.guild.id)] = prefix
          e = discord.Embed(title = "Prefix", description = f"Prefix got changed to: `{prefix}`", color = random.randint(0, 16777215))
          await inter.send(embed = e)
    else:
      if not prefix:
        e = discord.Embed(title = "Prefix", description = f"Current prefix is: `{db['prefix'][str(inter.guild.id)]}`", color = random.randint(0, 16777215))
        await inter.send(embed = e)
      else:
        e = discord.Embed(title = "Prefix", description = f"You can't change bot's prefix: No admin perms\nCurrent prefix is: `{db['prefix'][str(inter.guild.id)]}`", color = random.randint(0, 16777215))
        await inter.send(embed = e)

  @commands.slash_command(name = "warn", description = "Warn people (BETA)")
  @commands.has_permissions(kick_members = True)
  @commands.bot_has_permissions(kick_members = True)
  async def slashwarn(inter, member: discord.Member, *, reason = "None"):
    if str(member.id) not in db["warns"]:
      db["warns"][str(member.id)] = []
      updatelist = db["warns"][str(member.id)]
      updatelist.append(reason)
      db["warns"][str(member.id)] = updatelist
      e = discord.Embed(title = "Success", description = f"Warned `{member.name}` for reason: `{reason}`", color = random.randint(0, 16777215))
      await inter.send(embed = e)
    else:
      updatelist = db["warns"][str(member.id)]
      updatelist.append(reason)
      db["warns"][str(member.id)] = updatelist
      e = discord.Embed(title = "Success", description = f"Warned `{member.name}` for reason: `{reason}`", color = random.randint(0, 16777215))
      await inter.send(embed = e)

  @commands.slash_command(name = "warns", description =  "See people's warns (BETA)")
  @commands.has_permissions(kick_members = True)
  @commands.bot_has_permissions(kick_members = True)
  async def slashwarns(inter, member: discord.Member):
    if str(member.id) in db["warns"] and db["warns"][str(member.id)] != []:
      list = db["warns"][str(member.id)]
      text = ""
      text += f"1. `{list[0]}`"
      for i in range(len(list) - 1):
        text += f"\n{i + 2}. `{list[i + 1]}`"
      e = discord.Embed(title = f"{member.name}'s Warns:", description = text, color = random.randint(0, 16777215))
      await inter.send(embed = e)
    else:
      e = discord.Embed(title = f"{member.name}'s Warns:", description = "They have no warns", color = random.randint(0, 16777215))
      await inter.send(embed = e)

  @commands.slash_command(name = "removewarn", description = "Remove people's warns (BETA)")
  @commands.has_permissions(kick_members = True)
  @commands.bot_has_permissions(kick_members = True)
  async def removewarn(inter, member: discord.Member, index: int):
    if str(member.id) in db["warns"] and db["warns"][str(member.id)] != []:
      updatelist = db["warns"][str(member.id)]
      try:
        if not len(updatelist) < index or not 0 > index:
          reason = updatelist.pop(int(index - 1))
          db["warns"][str(member.id)] = updatelist
          e = discord.Embed(title = "Success!", description = f"`{member.name}`'s warn: {index}: `{reason}` is deleted!", color = random.randint(0, 16777215))
          await inter.send(embed = e)
        else:
          e = discord.Embed(title = "Error", description = "This index doesn't exist!", color = random.randint(0, 16777215))
          await inter.send(embed = e)
      except IndexError:
        e = discord.Embed(title = "Error", description = "This index doesn't exist!", color = random.randint(0, 16777215))
        await inter.send(embed = e)
    else:
      e = discord.Embed(title = "Error", description = "They have no warns", color = random.randint(0, 16777215))
      await inter.send(embed = e)

  #setting group
  @commands.slash_command(name = "setting", description = "See current setting or change it. Available settings: gpd")
  async def slashsetting(inter, setting, switch):
    if switch != "info":
      if inter.author.guild_permissions.administrator or inter.author.id == inter.bot.owner.id:
        if setting == "gpd":
          if str(inter.guild.id) in db["serversetting"]["gpd"]:
            del db["serversetting"]["gpd"][str(inter.guild.id)]
            e = discord.Embed(title = "Success", description = "You disabled ghost ping detection for this server", color = random.randint(0, 16777215))
            await inter.send(embed = e)
          else:
            db["serversetting"]["gpd"][str(inter.guild.id)] = "True"
            e = discord.Embed(title = "Success", description = "You enabled ghost ping detection for this server", color = random.randint(0, 16777215))
            await inter.send(embed = e)
      else:
        if str(inter.guild.id) in db["serversetting"]["gpd"]:
          e = discord.Embed(title = "GPD Info:", description = "Your server has ghost ping detection enabled", color = random.randint(0, 16777215))
          await inter.send(embed = e)
        else:
          e = discord.Embed(title = "GPD Info:", description = "Your server has ghost ping detection disabled", color = random.randint(0, 16777215))
          await inter.send(embed = e)

def setup(bot):
  bot.add_cog(Moderation(bot))