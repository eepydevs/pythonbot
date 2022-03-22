#cog by Number1#4325
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

async def suggest_posts(inter, input):
  return [post for post in db['account'][str(inter.author.id)].keys() if input.lower() in post.lower()][0:24]
  
class Social(commands.Cog):
  def __init__(self, bot):
    self.bot = bot  

  #add account command
  @commands.slash_command(description = "Create your account in social media of Python Bot")
  async def addaccount(inter):
    if str(inter.author.id) not in db["account"]:
      db["account"][str(inter.author.id)] = {}
      db["subs"][str(inter.author.id)] = []
      e = discord.Embed(title = "Success", description = "Account created!", color = random.randint(0, 16777215))
      await inter.send(embed = e)
    else:
      e = discord.Embed(title = "Error", description = "You already have an account!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

  #post command
  @commands.slash_command(description = "Post something. Account required, Has cooldown of 10 minutes")
  @commands.cooldown(rate = 1, per = 600, type = commands.BucketType.user)
  async def post(inter, name, text):
    '''
    Post something. Account required, has cooldown of 10 minutes

    Parameters
    ----------
    name: Name of post
    text: Text of post
    '''
    if str(inter.author.id) in db["account"]:
      updatedict = db["account"][str(inter.author.id)]
      updatedict.update({name: text})
      db["account"][str(inter.author.id)] = updatedict
      e = discord.Embed(title = "Success", description = f"You posted: `{name}: {text}`", color = random.randint(0, 16777215))
      await inter.send(embed = e)
    else:
      e = discord.Embed(title = "Error", description = "Make an account!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      inter.command.reset_cooldown(inter)

  #remove post command
  @commands.slash_command(description = "Remove your post. Account required")
  async def removepost(inter, name: str = commands.Param(autocomplete = suggest_posts)):
    '''
    Remove your posts. Account required
    
    Parameters
    ----------
    name: Name of post here
    '''
    if str(inter.author.id) in db["account"]:
      if name != None or name not in db["account"][str(inter.author.id)]:
        updatedict = db["account"][str(inter.author.id)]
        e = discord.Embed(title = "Success", description = f"Post named `{name}` is deleted!", color = random.randint(0, 16777215))
        await inter.send(embed = e)
        updatedict.pop(name)
        db["account"][str(inter.author.id)] = updatedict
      else:
        e = discord.Embed(title = "Error", description = f"Post named `{name}` doesn't exist!", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)
    else:
      e = discord.Embed(title = "Error", description = "Make an account!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

  #my subs list command
  #@commands.command(aliases = ["mysubslist"], help = "See your subscribers", description = "Account required")
  #async def mysubscriberslist(self, inter):
    #if str(inter.author.id) in db["account"]:
      #if len(db["subs"][str(inter.author.id)]) != 0:
        #sublist = []
        #sublist = ", ".join(f"{inter.guild.get_member(list()[]).mention}" for i in list(db["subs"][str(inter.author.id)]))
        #dblist = list(db['subs'][str(inter.author.id)])
        #for i in range(len(dblist) - 1):
          #if dblist[i - 1] in inter.guild.members:
            #sublist.append(inter.guild.get_member(dblist[i - 1]))
            
        #e = discord.Embed(title = f"{inter.author.name}'s Subscribers list:", description = f"Total subs counter: {len(sublist)}\n{str(sublist)}", color = random.randint(0, 16777215))
        #await inter.send(embed = e)
      #else:
        #e = discord.Embed(title = f"{inter.author.name}'s Subscribers list:", description = "Sorry you have no subscribers :(", color = random.randint(0, 16777215))
        #await inter.send(embed = e)
    #else:
      #e = discord.Embed(title = "Error", description = "You have no account...", color = random.randint(0, 16777215))
      #await inter.send(embed = e)


  #overview command
  @commands.slash_command(description = "See people's profile. Account required")
  async def overview(inter, member: discord.Member = None):
    '''
    See people's profile. Account required

    Parameters
    ----------
    member: Member here
    '''
    if member != None:
      if str(member.id) in db["account"]:
        if len(dict(db["account"][str(member.id)])) != 0:
          posts = dict(db["account"][str(member.id)])
          list1, list2 = list(posts.keys()), list(posts.values())
          names, texts = list1[-1], list2[-1]
          e = discord.Embed(title = f"{member.name}'s posts:", description = f"Posts here\nSubscribers count: {len(db['subs'][str(member.id)])}", color = random.randint(0, 16777215))
          e.add_field(name = names, value = texts)
          for i in range(len(list1) - 1):
            names = f"{list1[-i - 2]}"
            texts = f"{list2[-i - 2]}"
            e.add_field(name = names, value = texts)
          e.set_thumbnail(url = member.avatar)
          await inter.send(embed = e)
        else:
          e = discord.Embed(title = f"{member.name}'s posts:", description = f"Posts here\nSubscribers count: {len(db['subs'][str(member.id)])}", color = random.randint(0, 16777215))
          e.set_thumbnail(url = member.avatar)
          e.add_field(name = "No posts here", value = "Check later!")
          await inter.send(embed = e)
      else:
        e = discord.Embed(title = "Error", description = "They have no account...", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)
    else:
      if str(inter.author.id) in db["account"]:
        if len(dict(db["account"][str(inter.author.id)])) != 0:
          posts = dict(db["account"][str(inter.author.id)])
          list1, list2 = list(posts.keys()), list(posts.values())
          names, texts = list1[-1], list2[-1]
          e = discord.Embed(title = f"{inter.author.name}'s posts:", description = f"Posts here\nSubscribers count: {len(db['subs'][str(inter.author.id)])}", color = random.randint(0, 16777215))
          e.add_field(name = names, value = texts)
          for i in range(len(list1) - 1):
            names = f"{list1[-i - 2]}"
            texts = f"{list2[-i - 2]}"
            e.add_field(name = names, value = texts)
          e.set_thumbnail(url = inter.author.avatar)
          await inter.send(embed = e)
        else:
          e = discord.Embed(title = f"{inter.author.name}'s posts:", description = f"Posts here\nSubscribers count: {len(db['subs'][str(inter.author.id)])}", color = random.randint(0, 16777215))
          e.set_thumbnail(url = inter.author.avatar)
          e.add_field(name = "No posts here", value = "Check later!")
          await inter.send(embed = e)
      else:
        e = discord.Embed(title = "Error", description = "You have no account...", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)

  #view command
  @commands.slash_command(description = "See people's last post. Account required")
  async def view(inter, member: discord.Member = None):
    '''
    See people's last post. Account required

    Parameters
    ----------
    member: Member here
    '''
    if member != None:
      if str(member.id) in db["account"]:
        if len(dict(db["account"][str(member.id)])) != 0:
          posts = dict(db["account"][str(member.id)])
          list1, list2 = list(posts.keys()), list(posts.values())
          names, texts = list1[-1], list2[-1]
          e = discord.Embed(title = f"{member.name}'s latest post:", description = "latest post here", color = random.randint(0, 16777215))
          e.add_field(name = names, value = texts)
          e.set_thumbnail(url = member.avatar)
          await inter.send(embed = e)
        else:
          e = discord.Embed(title = f"{member.name}'s latest post:", description = "latest post here", color = random.randint(0, 16777215))
          e.set_thumbnail(url = member.avatar)
          e.add_field(name = "No posts here", value = "Check later!")
          await inter.send(embed = e)
      else:
        e = discord.Embed(title = "Error", description = "They have no account...", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)

  #subscribe command
  @commands.slash_command(description = "Subscribe to people. Account required")
  async def subscribe(inter, member: discord.Member = None):
    '''
    Subscribe to people\nAccount required

    Parameters
    ----------
    member: Member here
    '''
    
    if member != None:
      if str(member.id) != str(inter.author.id):
        if str(member.id) in db["account"]:
          if str(inter.author.id) in db["account"]:
            if str(inter.author.id) not in db["subs"][str(member.id)]:
              updatelist = db["subs"][str(member.id)]
              updatelist.append(str(inter.author.id))
              db["subs"][str(member.id)] = updatelist
              e = discord.Embed(title = "Success", description = f"Subscribed to `{member.name}`!", color = random.randint(0, 16777215))
              await inter.send(embed = e)
            else:
              e = discord.Embed(title = "Error", description = "You're already subscribed to this person!", color = random.randint(0, 16777215))
              await inter.send(embed = e, ephemeral = True)
          else:
            e = discord.Embed(title = "Error", description = "You have no account...", color = random.randint(0, 16777215))
            await inter.send(embed = e, ephemeral = True)
        else:
          e = discord.Embed(title = "Error", description = "They have no account...", color = random.randint(0, 16777215))
          await inter.send(embed = e, ephemeral = True)
      else:
        e = discord.Embed(title = "Error", description = "You can't subscribe to yourself", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)
    else:
      e = discord.Embed(title = "Error", description = "Mention a person!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

  #unsubscribe command
  @commands.slash_command(description = "Unsubscribe from people. Account required")
  async def unsubscribe(inter, member: discord.Member = None):
    '''
    Unsubscribe from people. Account required

    Parameters
    ----------
    member: Member here
    '''
    if member != None:
      if str(member.id) != str(inter.author.id):
        if str(member.id) in db["account"]:
          if str(inter.author.id) in db["account"]:
            if str(inter.author.id) in db["subs"][str(member.id)]:
              updatelist = list(db["subs"][str(member.id)])
              updatelist.remove(str(inter.author.id))
              db["subs"][str(member.id)] = updatelist
              e = discord.Embed(title = "Success", description = f"Unsubscribed from `{member.name}`!", color = random.randint(0, 16777215))
              await inter.send(embed = e, ephemeral = True)
            else:
              e = discord.Embed(title = "Error", description = "You're already unsubscribed from this person!", color = random.randint(0, 16777215))
              await inter.send(embed = e, ephemeral = True)
          else:
            e = discord.Embed(title = "Error", description = "You have no account...", color = random.randint(0, 16777215))
            await inter.send(embed = e, ephemeral = True)
        else:
          e = discord.Embed(title = "Error", description = "They have no account...", color = random.randint(0, 16777215))
          await inter.send(embed = e, ephemeral = True)
      else:
        e = discord.Embed(title = "Error", description = "You can't unsubscribe from yourself", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)
    else:
      e = discord.Embed(title = "Error", description = "Mention a person!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

def setup(bot):
  bot.add_cog(Social(bot))