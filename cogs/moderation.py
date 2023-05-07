#cog by maxy#2866
import disnake as discord
from disnake.ext import commands
import asyncio
from enum import Enum
import random
import os
from utils import db, LinkChannel

purgequotes = ["Stop spamming!", "Spamming is bad.", "Purge the chat! Haha!", "Purge after these silly young spammers...", "Is it just me, or is spamming more likely now than notime else?"]
modquotes = ["I hope they learned their lesson.", "Make them cry!", "Haha!", "Gotcha!", "They should've readed the rules.", "Why they didn't readed the rules...", "That's lesson for you to read rules!", "'no reason ban' they say... Right at your eyes broke rule number 1337!", "Oops!"]

if "warns" not in db:
  db["warns"] = {}

if "serversetting" not in db:
  db["serversetting"] = {}
  db["serversetting"]["gpd"] = {}
  db["serversetting"]["nqn"] = {}

if "channelsetting" not in db:
  db["channelsetting"] = {}
  db["channelsetting"]["imageonly"] = {}

class Requiredc(str, Enum):
  Text_Channel = "text"
  Voice_Channel = "voice"
  Stage_Channel = "stage"

class Requiredtoggler(str, Enum):
  true = "True"
  false = ""
  
class Moderation(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.slash_command()
  async def channel(self, inter):
    pass

  @channel.sub_command_group()
  async def settings(self, inter):
    pass

  @settings.sub_command()
  @commands.has_permissions(manage_channels = True)
  @commands.bot_has_permissions(manage_channels = True, manage_messages = True)
  async def imageonly(self, inter, id: int = None, *, toggler: Requiredtoggler = Requiredtoggler.false):
    if id is None:
      id = inter.channel.id
    if not inter.bot.get_channel(id):
      e = discord.Embed(title = "Error", description = "Invalid channel id", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

    if toggler == Requiredtoggler.true:
      if str(id) not in db["channelsetting"]["imageonly"]:
        db["channelsetting"]["imageonly"].update({str(id): True})
        e = discord.Embed(title="Success", description=f"Set `{id}` to image only", color=random.randint(0, 16777215))
        await inter.send(embed=e, ephemeral=True)
        return
      else:
        e = discord.Embed(title="Error", description="This channel is already image only", color=random.randint(0, 16777215))
        await inter.send(embed=e, ephemeral=True)
    else:
      if str(id) in db["channelsetting"]["imageonly"]:
        del db["channelsetting"]["imageonly"][str(id)]
        e = discord.Embed(title="Success", description=f"Set `{id}` to text only", color=random.randint(0, 16777215))
        await inter.send(embed=e, ephemeral=True)
        return
      else:
        e = discord.Embed(title="Error", description="This channel is not image only", color=random.randint(0, 16777215))
        await inter.send(embed=e, ephemeral=True)


  @channel.sub_command()
  @commands.is_owner()
  async def link(self, inter, id):
    '''
    Creates a link with current channelink and mentioned channel (ID)

    Parameters
    ----------
    id: Channel ID
    '''
    await inter.send(embed = LinkChannel(inter).link(id)[0], ephemeral = True)  

  @channel.sub_command()
  @commands.is_owner()
  async def unlink(self, inter, id):
    '''
    Unlinks current channel and mentioned channel (ID)

    Parameters
    ----------
    id: Channel ID
    '''
    await inter.send(embed = LinkChannel(inter).unlink(id)[0], ephemeral = True)

  @channel.sub_command(name = "create", description = "Create a channel")
  @commands.has_permissions(manage_channels = True)
  @commands.bot_has_permissions(manage_channels = True)
  async def createchannel(inter, *, name, channeltype: Requiredc = Requiredc.Text_Channel, topic = "", nsfw: Requiredtoggler = Requiredtoggler.false):
    '''
    Create a channel

    Parameters
    ----------
    name: Name of new channel
    channeltype: Existing types: text, voice, stage
    topic: Description of new channel
    nsfw: false or true
    '''
    if nsfw == Requiredtoggler.true:
      nsfw = True
    else:
      nsfw = False

    if channeltype == "text":
      await inter.guild.create_text_channel(name = name.replace(" ", "-"), category = inter.channel.category, topic = topic, nsfw = nsfw)
      e = discord.Embed(title = "Success", description = f"Text channel {name} is created!", color = random.randint(0, 16777215))
      await inter.send(embed = e)
    elif channeltype == "voice":
      await inter.guild.create_voice_channel(name = name, category = inter.channel.category)
      e = discord.Embed(title = "Success", description = f"Voice channel {name} is created!", color = random.randint(0, 16777215))
      await inter.send(embed = e)
    elif channeltype == "stage":
      await inter.guild.create_stage_channel(name = name.replace(" ", "-"), category = inter.channel.category, topic = topic)
      e = discord.Embed(title = "Success", description = f"Stage channel {name} is created!", color = random.randint(0, 16777215))
      await inter.send(embed = e)
    else:
      e = discord.Embed(title = "Error", description = "Unknown type!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

  #kick command
  @commands.slash_command(name = "kick", description = "Kick mentioned member")
  @commands.has_permissions(kick_members = True)
  @commands.bot_has_permissions(kick_members = True)
  async def slashkick(inter, member: discord.Member):
    '''
    Kick people

    Parameters
    ----------
    member: Mention member
    '''
    if not inter.author.top_role < member.top_role:
      e = discord.Embed(title = "Kicked!", description = f"You were kicked from server {inter.guild.name}", color = random.randint(0, 16777215))
      e.set_thumbnail(url = str(inter.guild.icon))
      await member.send(embed = e)
      
      await member.kick()
      kquote = modquotes[random.randint(0, len(modquotes) - 1)]
      e = discord.Embed(title = "Success", description = f"Successfully kicked {member.mention}! {kquote}", color = random.randint(0, 16777215))
      await inter.send(embed = e)
    else:
      e = discord.Embed(title = "Error", description = "You can't kick a person higher than you", color = random.randint(0, 16777215))
      await inter.send(embed = e)

  #ban command
  @commands.slash_command(name = "ban", description = "Ban mentioned people")
  @commands.has_permissions(ban_members = True)
  @commands.bot_has_permissions(ban_members = True)
  async def ban(inter, member: discord.Member, reason = None):
    '''
    Ban people

    Parameters
    ----------
    member: Mention member
    reason: Reason for the ban, will show up in audit log
    '''
    if not inter.author.top_role < member.top_role:
        e = discord.Embed(title = "Banned!", description = f"You were banned from server {inter.guild.name}", color = random.randint(0, 16777215))
        e.set_thumbnail(url = str(inter.guild.icon))
        await member.send(embed = e)
    
        await member.ban(reason = reason)
        bquote = modquotes[random.randint(0, len(modquotes) - 1)]
        e = discord.Embed(title = "Success", description = f"Successfully banned {member.mention}! {bquote}", color = random.randint(0, 16777215))
        await inter.send(embed = e)
    else:
      e = discord.Embed(title = "Error", description = "You can't ban a person higher than you", color = random.randint(0, 16777215))
      await inter.send(embed = e)
  

  '''#timeout command
  @commands.slash_command(name = "timeout", description = "timeout people")
  @commands.has_permissions(moderate_members = True)
  @commands.bot_has_permissions(moderate_members = True)
  async def slashtimeout(inter, member: discord.Member, duration = "1d"):
    
    Timeout (mute) mentioned member

    Parameters
    ----------
    member: Mention member
    duration: Xh = X hours, Xd = X days, Xs = X seconds, Xm = X minutes | Default: 1d
        
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
      await inter.send(embed = e)'''

  #unban command
  @commands.slash_command(name = "unban", description = "Unban people")
  @commands.has_permissions(ban_members = True)
  @commands.bot_has_permissions(ban_members = True)
  async def unban(inter, member: discord.User, reason = "None"):
    '''
    Unban people

    Parameters
    ----------
    member: Mention member
    reason: Reason for the unban, will show up in audit log
    '''
    if not inter.author.top_role < member.top_role:
        e = discord.Embed(title = "Error", description = "You can't warn a person higher than you", color = random.randint(0, 16777215))
        await inter.send(embed = e)
        e = discord.Embed(title = "Unbanned!", description = f"You were unbanned from server {inter.guild.name}", color = random.randint(0, 16777215))
        e.set_thumbnail(url = str(inter.guild.icon))
        await member.send(embed = e)
    
        await member.unban(reason = reason)
        e = discord.Embed(title = "Success", description = f"Successfully unbanned {member.mention}!", color = random.randint(0, 16777215))
        await inter.send(embed = e)
    else:
      e = discord.Embed(title = "Error", description = "You can't nnban a person higher than you", color = random.randint(0, 16777215))
      await inter.send(embed = e)

  #purge command
  @commands.slash_command(name = "purge", description = "Purge messages")
  @commands.has_permissions(manage_channels = True)
  @commands.bot_has_permissions(manage_channels = True)
  async def slashpurge(inter, number: int):
    '''
    Purge messages
    
    Parameters
    ----------
    number: Number used for purging, min=0, max=100
    '''
    if number <= 0: number = 1
    if number >= 100: number = 100
    await inter.channel.purge(limit = number)
    pquote = random.choice(purgequotes)
    e = discord.Embed(title = "Success", description = f"Purged the channel successfully! {pquote}", color = random.randint(0, 16777215))
    await inter.send(embed = e, delete_after = 5)
  #pin command
  @commands.slash_command()
  @commands.has_permissions(manage_channels = True)
  @commands.bot_has_permissions(manage_channels = True)
  async def pin(inter, message: discord.Message):
    '''
    Pin a message, This is useless command don't use it
    
    Parameters
    ----------
    message: Message id
    '''
    await message.pin()
    await inter.send(f"[Message]({message.jump_url}) pinned successfully")
    
  @commands.slash_command()
  async def warns(self, inter):
    pass

  @warns.sub_command(name = "add")
  @commands.has_permissions(kick_members = True)
  @commands.bot_has_permissions(kick_members = True)
  async def slashwarn(self, inter, member: discord.Member, reason = "None"):
    '''
    Warn people

    Parameters
    ----------
    member: Mention member
    reason: Reason for the warn, will be shown in /warns show member: @mention
    '''
    if not inter.author.top_role < member.top_role:
      if str(inter.guild.id) not in db["warns"]:
        db["warns"][str(inter.guild.id)] = {}
      if str(member.id) not in db["warns"][str(inter.guild.id)]:
        db["warns"][str(inter.guild.id)][str(member.id)] = []
        updatelist = db["warns"][str(inter.guild.id)][str(member.id)]
        updatelist.append(reason)
        db["warns"][str(inter.guild.id)][str(member.id)] = updatelist
        e = discord.Embed(title = "Success", description = f"Warned `{member.name}` for reason: `{reason}`", color = random.randint(0, 16777215))
        await inter.send(embed = e)
      else:
        updatelist = db["warns"][str(inter.guild.id)][str(member.id)]
        updatelist.append(reason)
        db["warns"][str(inter.guild.id)][str(member.id)] = updatelist
        e = discord.Embed(title = "Success", description = f"Warned `{member.name}` for reason: `{reason}`", color = random.randint(0, 16777215))
        await inter.send(embed = e)
    else:
      e = discord.Embed(title = "Error", description = "You can't warn a person higher than you", color = random.randint(0, 16777215))
      await inter.send(embed = e)

  @warns.sub_command(name = "show")
  @commands.has_permissions(kick_members = True)
  @commands.bot_has_permissions(kick_members = True)
  async def slashwarns(self, inter, member: discord.Member):
    '''
    See people's warns

    Parameters
    ----------
    member: Mention member
    '''
    if not inter.author.top_role < member.top_role:
      if str(inter.guild.id) not in db["warns"]:
        db["warns"][str(inter.guild.id)] = {}
      if str(member.id) in db["warns"][str(inter.guild.id)] and db["warns"][str(inter.guild.id)][str(member.id)] != []:
        list = db["warns"][str(inter.guild.id)][str(member.id)]
        text = ""
        text += f"1. `{list[0]}`"
        for i in range(len(list) - 1):
          text += f"\n{i + 2}. `{list[i + 1]}`"
        e = discord.Embed(title = f"{member.name}'s Warns:", description = text, color = random.randint(0, 16777215))
        await inter.send(embed = e)
      else:
        e = discord.Embed(title = f"{member.name}'s Warns:", description = "They have no warns", color = random.randint(0, 16777215))
        await inter.send(embed = e)
    else:
      e = discord.Embed(title = "Error", description = "You can't see warns of a person higher than you", color = random.randint(0, 16777215))
      await inter.send(embed = e)

  @warns.sub_command(name = "remove")
  @commands.has_permissions(kick_members = True)
  @commands.bot_has_permissions(kick_members = True)
  async def removewarn(self, inter, member: discord.Member, index: int):
    '''
    Remove people's warns

    Parameters
    ----------
    member: Mention member
    index: index of the warn, shown in /warns member: @mention
    '''
    if not inter.author.top_role < member.top_role:
      if str(inter.guild.id) not in db["warns"]:
        db["warns"][str(inter.guild.id)] = {}
      if str(member.id) in db["warns"][str(inter.guild.id)] and db["warns"][str(inter.guild.id)][str(member.id)] != []:
        updatelist = db["warns"][str(inter.guild.id)][str(member.id)]
        try:
          if not len(updatelist) < index or not 0 > index:
            reason = updatelist.pop(int(index - 1))
            db["warns"][str(inter.guild.id)][str(member.id)] = updatelist
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
    else:
      e = discord.Embed(title = "Error", description = "You can't remove warns from a person higher than you", color = random.randint(0, 16777215))
      await inter.send(embed = e)


  #setting group
  @commands.slash_command(name = "setting", description = "See current setting or change it. Available settings: gpd")
  async def slashsetting(inter, setting, switch = "info"):
    '''
    Switch settings

    Parameters
    ----------
    setting: Available settings: gpd, nqn
    switch: basically anything
    '''
    if switch != "info":
      if inter.author.guild_permissions.administrator or inter.author.id == inter.bot.owner.id:
        if setting == "gpd":
          if str(inter.guild.id) in db["serversetting"]["gpd"] and db["serversetting"]["gpd"][str(inter.guild.id)]:
            db["serversetting"]["gpd"][str(inter.guild.id)] = None
            e = discord.Embed(title = "Success", description = "You disabled ghost ping detection for this server", color = random.randint(0, 16777215))
            await inter.send(embed = e)
          else:
            db["serversetting"]["gpd"][str(inter.guild.id)] = "True"
            e = discord.Embed(title = "Success", description = "You enabled ghost ping detection for this server", color = random.randint(0, 16777215))
            await inter.send(embed = e)
        if setting == "nqn":
          if str(inter.guild.id) in db["serversetting"]["nqn"] and db["serversetting"]["nqn"][str(inter.guild.id)]:
            db["serversetting"]["nqn"][str(inter.guild.id)] = None
            e = discord.Embed(title = "Success", description = "You disabled NQN feature for this server", color = random.randint(0, 16777215))
            await inter.send(embed = e)
          else:
            db["serversetting"]["nqn"][str(inter.guild.id)] = "True"
            e = discord.Embed(title = "Success", description = "You enabled NQN feature for this server", color = random.randint(0, 16777215))
            await inter.send(embed = e)
      else:
        if setting == "gpd":
          if str(inter.guild.id) in db["serversetting"]["gpd"]:
            e = discord.Embed(title = "GPD Info:", description = "Your server has ghost ping detection enabled", color = random.randint(0, 16777215))
            await inter.send(embed = e)
          else:
            e = discord.Embed(title = "GPD Info:", description = "Your server has ghost ping detection disabled", color = random.randint(0, 16777215))
            await inter.send(embed = e)
        if setting == "nqn":
          if str(inter.guild.id) in db["serversetting"]["nqn"]:
            e = discord.Embed(title = "NQN Info:", description = "Your server has NQN feature enabled", color = random.randint(0, 16777215))
            await inter.send(embed = e)
          else:
            e = discord.Embed(title = "NQN Info:", description = "Your server has NQN feature disabled", color = random.randint(0, 16777215))
            await inter.send(embed = e)

def setup(bot):
  bot.add_cog(Moderation(bot))