import disnake as discord
from disnake.ext import commands
import asyncio
import random
from replit import db

purgequotes = ["Stop spamming!", "Spamming is bad.", "Purge the chat! Haha!", "Purge after these silly young spammers..."]
modquotes = ["I hope they learned their lesson.", "Make them cry!", "Haha!", "Gotcha!", "They should've readed the rules.", "Why they didn't readed the rules...", "That's lesson for you to read rules!", "'no reason ban' they say... Right at your eyes broke rule number 1337!", "Oops!"]

if "prefix" not in db:
  db["prefix"] = {}

if "warns" not in db:
  db["warns"] = {}


class Moderation(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  #kick command
  @commands.command(help = "Kick mentioned member", description = "This command is for admins only\nYou can kick members with this command\nUsage: pb!kick (@mention)")
  @commands.has_permissions(kick_members = True)
  async def kick(self, ctx, member: discord.Member): 
    e = discord.Embed(title = "Pwned!", description = f"You were kicked from server {ctx.guild.name}", color = random.randint(0, 16777215))
    e.set_thumbnail(url = str(ctx.guild.icon))
    await member.send(embed = e)
    
    await member.kick()
    kquote = modquotes[random.randint(0, len(modquotes) - 1)]
    e = discord.Embed(title = "Success", description = f"Successfully kicked {member.mention}! {kquote}", color = random.randint(0, 16777215))
    await ctx.send(embed = e)

  #ban command
  @commands.command(help = "Ban mentioned member", description = "This command is for admins only\nYou can ban members with this command\nUsage: pb!ban (@mention) [reason]")
  @commands.has_permissions(ban_members = True)
  async def ban(self, ctx, member: discord.Member, *, reason = None):
    e = discord.Embed(title = "Banned!", description = f"You were banned from server {ctx.guild.name}", color = random.randint(0, 16777215))
    e.set_thumbnail(url = str(ctx.guild.icon))
    await member.send(embed = e)

    await member.ban(reason = reason)
    bquote = modquotes[random.randint(0, len(modquotes) - 1)]
    e = discord.Embed(title = "Success", description = f"Successfully banned {member.mention}! {bquote}", color = random.randint(0, 16777215))
    await ctx.send(embed = e)

  #timeout command
  @commands.command(aliases = ["mute"], help = "Mute/Timeout mentioned member", description = "This command is for admins only\nYou can mute/timeout members with this command\nUsage: pb!timeout (user) (duration)")
  @commands.has_permissions(kick_members = True)
  async def timeout(self, ctx, member: discord.Member = None, duration = "1d"):
    if member != None:
      if duration.endswith("d"):
        timeoutduration = 86400 * int(duration[:-1])
        await member.timeout(duration = timeoutduration)
      elif duration.endswith("s"):
        timeoutduration = int(duration[:-1])
        await member.timeout(duration = timeoutduration)
      elif duration.endswith("h"):
        timeoutduration = 3600 * int(duration[:-1])
        await member.timeout(duration = timeoutduration)
    else:
      e = discord.Embed(title = "Error", description = "Mention a member!", color = random.randint(0, 16777215))
      await ctx.send(embed = e)

  #unban command
  @commands.command(help = "Unban mentioned member", description = "This command is for admins only\nYou can unban members with this command\nUsage: pb!unban (user) [reason]")
  @commands.has_permissions(ban_members = True)
  async def unban(self, ctx, member: discord.Member, *, reason = None):
    e = discord.Embed(title = "Unbanned!", description = f"You were unbanned from server {ctx.guild.name}", color = random.randint(0, 16777215))
    e.set_thumbnail(url = str(ctx.guild.icon))
    await member.send(embed = e)

    await member.unban(reason = reason)
    e = discord.Embed(title = "Success", description = f"Successfully unbanned {member.mention}!", color = random.randint(0, 16777215))
    await ctx.send(embed = e)

  #purge command
  @commands.command(aliases = ["purge", "c"],help = "Purge messages", description = "This command is for admins only\nYou can clear N amount of messages with this command\nUsage: pb!clear (num)")
  @commands.has_permissions(manage_channels = True)
  async def clear(self, ctx, num1: int):
    if num1 > 0:
      if num1 < 100:
        await ctx.message.delete()
        await ctx.channel.purge(limit = num1)
        pquote = purgequotes[random.randint(0, len(purgequotes) - 1)]
        e = discord.Embed(title = "Success", description = f"Purged the channel successfully! {pquote}", color =  random.randint(0, 16777215))
        await ctx.send(embed = e, delete_after = 5)
        #await asyncio.sleep(5)
        #await m.delete()
      else:
        await ctx.send("❌ Please insert a number under 100")
    else:
      await ctx.send("❌ Please insert a number above 0")

  #pin command
  @commands.command(help = "Pin a message", description = "This is useless command don't use it\nUsage: Reply a message and type pb!pin\nUsage 2: pb!pin (message id)")
  @commands.has_permissions(manage_channels = True)
  async def pin(self, ctx, message: discord.Message = None):
    if message == None and ctx.message.reference.resolved != None:
      await ctx.message.reference.resolved.pin()
    else:
      await message.pin()

  #prefix command
  @commands.command(help = "See current prefix or change it", description = "For people with admin perms only\nExample: pb!prefix ?\nNote: Limit is 5 characters")
  async def prefix(self, ctx, prefix = None):
    if ctx.message.author.guild_permissions.administrator or ctx.author.id == ctx.bot.owner.id:
      if not prefix:
        e = discord.Embed(title = "Prefix", description = f"Current prefix is: `{db['prefix'][str(ctx.guild.id)]}`", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
      else:
        if len(prefix) > 5:
          db["prefix"][str(ctx.guild.id)] = prefix[:5]
          e = discord.Embed(title = "Prefix", description = f"Prefix got changed to: `{prefix[:5]}`", color = random.randint(0, 16777215))
          await ctx.send(embed = e)
        else:
          db["prefix"][str(ctx.guild.id)] = prefix
          e = discord.Embed(title = "Prefix", description = f"Prefix got changed to: `{prefix}`", color = random.randint(0, 16777215))
          await ctx.send(embed = e)
    else:
      if not prefix:
        e = discord.Embed(title = "Prefix", description = f"Current prefix is: `{db['prefix'][str(ctx.guild.id)]}`", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
      else:
        e = discord.Embed(title = "Prefix", description = f"You can't change bot's prefix: No admin perms\nCurrent prefix is: `{db['prefix'][str(ctx.guild.id)]}`", color = random.randint(0, 16777215))
        await ctx.send(embed = e)

  @commands.command(help = "Warn people (BETA)")
  @commands.has_permissions(kick_members = True)
  async def warn(self, ctx, member: discord.Member = None, *, reason = "None"):
    if member != None:
      if str(member.id) not in db["warns"]:
        db["warns"][str(member.id)] = []
        updatelist = db["warns"][str(member.id)]
        updatelist.append(reason)
        db["warns"][str(member.id)] = updatelist
        e = discord.Embed(title = "Success", description = f"Warned `{member.name}` for reason: `{reason}`", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
      else:
        updatelist = db["warns"][str(member.id)]
        updatelist.append(reason)
        db["warns"][str(member.id)] = updatelist
        e = discord.Embed(title = "Success", description = f"Warned `{member.name}` for reason: `{reason}`", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
    else:
      e = discord.Embed(title = "Error", description = "Mention a person you want to warn!", color = random.randint(0, 16777215))
      await ctx.send(embed = e)

  @commands.command(help = "See people's warns (BETA)")
  @commands.has_permissions(kick_members = True)
  async def warns(self, ctx, member: discord.Member = None):
    if member != None:
      if str(member.id) in db["warns"] and db["warns"][str(member.id)] != []:
        list = db["warns"][str(member.id)]
        text = ""
        text += f"1. `{list[0]}`"
        for i in range(len(list) - 1):
          text += f"\n{i + 2}. `{list[i + 1]}`"
        e = discord.Embed(title = f"{member.name}'s Warns:", description = text, color = random.randint(0, 16777215))
        await ctx.send(embed = e)
      else:
        e = discord.Embed(title = f"{member.name}'s Warns:", description = "They have no warns", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
    else:
      e = discord.Embed(title = "Error", description = "You can't see nobody's warns!", color = random.randint(0, 16777215))
      await ctx.send(embed = e)

  @commands.command(aliases = ["rwarn"], help = "Remove people's warns (BETA)")
  @commands.has_permissions(kick_members = True)
  async def removewarn(self, ctx, member: discord.Member, index: int):
    if member != None:
      if str(member.id) in db["warns"] and db["warns"][str(member.id)] != []:
        updatelist = db["warns"][str(member.id)]
        try:
          if not len(updatelist) < index or not 0 > index:
            reason = updatelist.pop(int(index - 1))
            db["warns"][str(member.id)] = updatelist
            e = discord.Embed(title = "Success!", description = f"`{member.name}`'s warn: {index}: `{reason}` is deleted!", color = random.randint(0, 16777215))
            await ctx.send(embed = e)
          else:
            e = discord.Embed(title = "Error", description = "This index doesn't exist!", color = random.randint(0, 16777215))
            await ctx.send(embed = e)
        except IndexError:
          e = discord.Embed(title = "Error", description = "This index doesn't exist!", color = random.randint(0, 16777215))
          await ctx.send(embed = e)
      else:
        e = discord.Embed(title = "Error", description = "They have no warns", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
    else:
      e = discord.Embed(title = "Error", description = "You can't delete nobody's warns!", color = random.randint(0, 16777215))
      await ctx.send(embed = e)

def setup(bot):
  bot.add_cog(Moderation(bot))