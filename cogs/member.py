import disnake as discord
from disnake.ext import commands
import random
import asyncio
import datetime, time
from replit import db

waiquotes = ["Your cool", "Your pro", "I dont know who are you", "Your 228 iq", "Your The Le` Pro!", "Que pro"]

class Member(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  #member nick command
  @commands.command(aliases = ["mu", "useris"], help = "Shows mentioned member's usernmae", description = "Usage: pb!membernick (@mention)")
  async def memberuser(self, ctx, member: discord.Member = None):
    if member != None:
      e = discord.Embed(title = "Member's nick:", description = f"{member.name}", color = random.randint(0, 16777215))
      await ctx.send(embed = e)
    else:
      e = discord.Embed(title = "Message author's nick:", description = f"{ctx.author.name}", color = random.randint(0, 16777215))
      await ctx.send(embed = e)
  
  #member pfp command
  @commands.command(aliases = ["mpfp", "mavatar", "avataris"], help = "Shows mentioned member's avatar", description = "Usage: pb!membernick (@mention)")
  async def memberavatar(self, ctx, member: discord.Member = None):
    if member != None:
      e = discord.Embed(title = f"{member}'s avatar:", description = "nice pfp ngl", color = random.randint(0, 16777215))
      e.set_image(url = member.avatar)
      await ctx.send(embed = e)
    else:
      e = discord.Embed(title = f"{ctx.author}'s avatar:", description = "nice pfp ngl", color = random.randint(0, 16777215))
      e.set_image(url = ctx.author.avatar)
      await ctx.send(embed = e)

  #member info command
  @commands.command(aliases = ["mi", "whois"], help = "Shows mentioned member's info", description = "Usage: pb!memberinfo (@mention)")
  async def memberinfo(self, ctx, member: discord.Member = None):
    if member != None:
      role_list = []

      for role in member.roles:
        if role.name != "@everyone":
          role_list.append(role.mention)

      b = ",".join(role_list)
      e = discord.Embed(title = f"Member info: {member}", description = f"Joined server date: <t:{str(time.mktime(member.joined_at.timetuple()))[:-2]}:R>\nCreated account date: <t:{str(time.mktime(member.created_at.timetuple()))[:-2]}:R>", color = random.randint(0, 16777215))
      e.set_thumbnail(url = str(member.avatar))
      if len(role_list) != 0:
        e.add_field(name = f"Roles ({len(role_list)}):", value = "".join([b]), inline = False)
      else:
        e.add_field(name = "Roles (0)", value = "None")
      e.add_field(name = "Top role:", value = member.top_role.mention, inline = False)
      if member.guild_permissions.administrator:
        e.add_field(name = "Administrator?", value = "True" , inline = False)
      else:
        e.add_field(name = "Administrator?", value = "False", inline = False)
      e.add_field(name = "Icon url:", value = str(member.avatar)[:-10], inline = False)
      e.set_footer(text = f"ID: {member.id}")
      await ctx.send(embed = e)
    else:
      rgwai = waiquotes[random.randint(0, len(waiquotes) - 1)]
      role_list = []

      for role in ctx.author.roles:
        if role.name != "@everyone":
          role_list.append(role.mention)

      b = ",".join(role_list)
      e = discord.Embed(title = f"Member info: {ctx.author}", description = f"Joined server date: <t:{str(time.mktime(ctx.author.joined_at.timetuple()))[:-2]}:R>\nCreated account date: <t:{str(time.mktime(ctx.author.created_at.timetuple()))[:-2]}:R>", color = random.randint(0, 16777215))
      e.set_thumbnail(url = str(ctx.author.avatar))
      if len(role_list) != None:
        e.add_field(name = f"Roles ({len(role_list)}):", value = "".join([b]), inline = False)
      else:
        e.add_field(name = "Roles (0):", value = "None")
      e.add_field(name = "Top role:", value = ctx.author.top_role.mention, inline = False)
      if ctx.author.guild_permissions.administrator:
        e.add_field(name = "Administrator?", value = "True" , inline = False)
      else:
        e.add_field(name = "Administrator?", value = "False", inline = False)
      e.add_field(name = "Icon url:", value = str(ctx.author.avatar)[:-10], inline = False)
      e.add_field(name = "Quote:", value = f"{rgwai}")
      e.set_footer(text = f"ID: {ctx.author.id}")
      await ctx.send(embed = e)

def setup(bot):
  bot.add_cog(Member(bot))