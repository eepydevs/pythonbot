#cog by Number1#4325
import disnake as discord
from disnake.ext import commands
from enum import Enum
import re
import os
import utils
import random
import asyncio
import requests
import math
import datetime, time
from replit import db

bad_words = os.getenv("badwords")

whitelist_id = [439788095483936768, 417334153457958922, 902371374033670224, 691572882148425809, 293189829989236737, 826509766893371392, 835455268946051092, 901115550695063602]

class Required1(str, Enum):
  You = "True"
  Everyone = ""

class sendopt(str, Enum):
  Slash = "Slash"
  Seperate = "Seperate"
  Webhook = "Webhook"

def shuffle(x):
  return random.sample(x, len(x))

def calc(text):
  check = text.split(" ")
  whitelist = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "/", "%", "+", "-", "(", ")", " ", "."]
  for i in range(len(check)):
    if len(check[i]) < 15:
      continue
    else:
      raise Exception("Maximum amount of characters per spaced string is 15!")
  if all(i in whitelist for i in text):
    return eval(text)
  else:
    raise ValueError("Something went wrong... (You may have used non-int)")

class Nonsense(commands.Cog):
  def __init__(self, bot):
    self.bot = bot  

  @commands.Cog.listener()
  async def on_message(self, msg):
    if msg.author.bot:
      return
    if str(msg.guild.id) in db["serversetting"]["nqn"]:
      reg = ':[a-zA-Z]+:'
      other = re.split(reg, msg.content)
      emjs = re.findall(reg, msg.content)
      content=other[0]
      for i in range(len(emjs)):
        myemjs = tuple(filter(lambda emj: emj.name==emjs[i][1:-1], self.bot.emojis))
        emj = f'<:{myemjs[0].name}:{myemjs[0].id}>' if (any(myemjs) and not other[i].endswith('<')) else emjs[i]
        content+=emj+other[i+1]
        
      if content==msg.content: return
      if msg.reference and len(msg.content.split())==1:
        await msg.delete()
        await self.react.__call__(msg, myemjs[0], msg.reference.resolved)
      else:
        webhook = (await utils.Webhook((await self.bot.get_context(msg))))
        await msg.delete()
        await webhook.send(content=content, username=msg.author.display_name, avatar_url=msg.author.avatar)

  @commands.slash_command(name = "urban")
  async def slashurban(inter, query):
    '''
    See meaning of term you need
    Parameters
    ----------
    query: Your term here!
    '''
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
    querystring = {"term": query}
    headers = {
        'x-rapidapi-key': os.getenv('urbanAPI'),
        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    rjson = response.json()
    e = discord.Embed(title = f"Urban Dictionary Meaning for: {query}", url = rjson['list'][0]['permalink'], color = random.randint(0, 16777215))
    e.add_field(name = "Definition:", value = rjson['list'][0]['definition'], inline = False)
    e.add_field(name = "Example:", value = rjson['list'][0]['example'], inline = False)
    e.set_footer(text = f"👍: {rjson['list'][0]['thumbs_up']} / 👎: {rjson['list'][0]['thumbs_down']} | Author: {rjson['list'][0]['author']}")
    await inter.send(embed = e)
    #except:
    #  e = discord.Embed(title = "Error", description = "Something went wrong...", color = random.randint(0, 16777215))
    #  await inter.send(embed = e, ephemeral = True)


  @commands.slash_command(name = "copy-person")
  @commands.bot_has_permissions(manage_webhooks = True)
  async def userecho(inter, member: discord.Member, *, content):
    '''
    Copy someone!
    Parameters
    ----------
    member: Mention a person to copy
    content: Input text here
    '''
    await inter.send(f"Successfully sent `{content}` as `{member}`", ephemeral = True) 
    channel_webhooks = await inter.channel.webhooks()
    webhook_count = 0

    for webhook in channel_webhooks:
        if webhook.user.id == inter.bot.user.id and webhook.name == "PythonBot Webhook":
            await webhook.send(
                content=content, username=member.display_name, avatar_url=member.avatar
            )
            return

    new_webhook = await inter.channel.create_webhook(name="PythonBot Webook", reason="PythonBot webhook usage in commands")
    await new_webhook.send(content=content, username=member.display_name, avatar_url=member.avatar)

  @commands.slash_command()
  async def react(self, inter, emoji:discord.Emoji, message:discord.Message):
    '''
    Let a Tupper add a Reaction

    Parameters
    ----------
    emoji: The Emoji to react with
    message:  The Message Url you want to react to
    '''
    await message.add_reaction(emoji)
    if isinstance(inter, discord.Message):
      sent = await inter.author.send('Reaction added!\nMake sure to add your own Reaction for it to stay')
    else:
      await inter.send('Reaction added!\nMake sure to add your own Reaction for it to stay', ephemeral=True)
      sent = inter.response
    try:
      await self.bot.wait_for('reaction_add', check=lambda react, user: react.message==message and user==inter.author, timeout=10)
      await message.remove_reaction(emoji, self.bot.user)
      await sent.delete()
      return
    except:
      await message.remove_reaction(emoji, self.bot.user)
      await sent.delete()

  #eval command
  @commands.slash_command(name = "eval", description = "ONLY FOR PEOPLE THAT ARE IN WHITELIST. Execute python code and see results")
  @commands.check(lambda inter: inter.author.id in whitelist_id)
  async def eval(inter, *, ephemeral: Required1 = Required1.You, code):
    blacklist = ["time.sleep", "sleep", "open", "exec", "license", "help", "exit", "quit", "os", "eval", "reset_cooldown", "run", "clear", "unload_extension", "load_extension"]
    try:
      if inter.author.id == inter.bot.owner.id:
        e = discord.Embed(title = "Eval:", description = f"```py\n{code}\n```\nResult: ```\n{eval(code)}\n```", color = random.randint(0, 16777215)) 
        await inter.send(embed = e, ephemeral = ephemeral)
      else:
        if any(i in code for i in blacklist):
          e = discord.Embed(title = "Error", description = "```'NoneType' is not callable```", color = random.randint(0, 16777215))
          await inter.send(embed = e, ephemeral = True)
        else:
          e = discord.Embed(title = "Eval:", description = f"```py\n{code}\n```\nResult:\n```\n{eval(code, {'__builtins__': __builtins__, '__import__': None, 'eval': None, 'random': random, 'inter': inter, 'int': int, 'str': str, 'len': len, 'time': time, 'datetime': datetime, 'mktime': time.mktime, 'math': math, 'quit': None, 'exit': None, 'help': None, 'license': None, 'exec': None, 'print': None, 'os': None, 'open': None, 'sleep': None, 'time.sleep': None, 'shuffle': lambda x: random.sample(x, len(x)), 'reset_cooldown': None, 'run': None, 'clear': None, 'unload_extension': None, 'load_extension': None})}\n```", color = random.randint(0, 16777215))
          await inter.send(embed = e, ephemeral = ephemeral)
    except Exception as error:
      e = discord.Embed(title = "Error", description = f"```{error}```", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
  
  #calculator command
  @commands.slash_command(name = "calc", description = "Calculate anything you need! (basic math)")
  async def slashcalculator(inter, equation):
    e = discord.Embed(title = "Calculator", description = f"{equation} = {calc(equation)}", color = random.randint(0, 16777215))
    await inter.send(embed = e)
  
  #embed command
  @commands.slash_command(name = "embed")
  async def slashembed(inter, ephemeral: Required1, *, _send: sendopt = sendopt.Slash, content = "", author_name = "", author_icon = "", title = "", desc = "", footer = "", footer_icon = "", color = random.randint(0, 16777215), thumbnail = "", image = ""):
    '''
    Makes an embed for you
    Parameters
    ----------
    ephemeral: Visibility of the embed, required
    _send: How to send embed, default is slash
    content: Text outside embed, default is none
    author_name: Author name, default is your name
    author_icon: Author icon, default is your pfp
    title: Embed title, default is none
    desc: Embed Description, default is none
    footer: Embed footer, default is none
    footer_icon: Footer icon, default is none
    color: Embed color, default is random
    thumbnail: Embed thumbnail, default is none
    image: Embed image, default is none
    '''
    if author_icon == "":
      author_icon = str(inter.author.avatar)[:-10]
    if author_name == "":
      author_name = inter.author.name
    e = discord.Embed(title = title, description = desc, color = color)
    e.set_author(name = author_name, icon_url = author_icon)
    e.set_footer(text = footer, icon_url = footer_icon)
    e.set_thumbnail(url = thumbnail)
    e.set_image(url = image)
    if _send == "Seperate":
      await inter.send("Successfully sent seperated embed", ephemeral = True)
      await inter.send(content = content, embed = e, ephemeral = ephemeral)
    elif _send == "Webhook":
      await inter.send("Successfully sent embed as webhook", ephemeral = True)
      channel_webhooks = await inter.channel.webhooks()
      webhook_count = 0

      for webhook in channel_webhooks:
        if webhook.user.id == inter.bot.user.id and webhook.name == "PythonBot Webhook":
            await webhook.send(
                content = content, embed = e, username = inter.bot.user.display_name, avatar_url = inter.bot.user.avatar
            )
            return

      new_webhook = await inter.channel.create_webhook(name="PythonBot Webook", reason="PythonBot webhook usage in commands")
      await new_webhook.send(content = content, embed = e, username = inter.bot.user.display_name, avatar_url = inter.bot.user.avatar)
    else:
      await inter.send(content = content, embed = e, ephemeral = ephemeral)

  #test 2 (buttons message) command
  @commands.slash_command(name = "button", description = "test command 2", hidden = True)
  async def slashbutton(inter):
    view = discord.ui.View(timeout = 60)
    style = discord.ButtonStyle.blurple
    item = discord.ui.Button(style = style, label = "Primary", custom_id = "Primary", emoji = "1️⃣")
    style1 = discord.ButtonStyle.gray
    item1 = discord.ui.Button(style = style1, label = "Secondary", custom_id = "Secondary", emoji = "2️⃣")
    style2 = discord.ButtonStyle.green
    item2 = discord.ui.Button(style = style2, label = "Success", custom_id = "Success", emoji = "✅")
    style3 = discord.ButtonStyle.red
    item3 = discord.ui.Button(style = style3, label = "Danger", custom_id = "Danger", emoji = "⚠️")
    style4 = discord.ButtonStyle.gray
    item4 = discord.ui.Button(style = style4, label = "Link", url = "https://www.youtube.com/c/MrBeast6000", emoji = "🔗")
    #style5 = discord.ButtonStyle.red
    #item5 = discord.ui.Button(style = style5, label = "Disable", custom_id = "Disable", emoji = "⛔")
    view.add_item(item = item)
    view.add_item(item = item1)
    view.add_item(item = item2)
    view.add_item(item = item3)
    view.add_item(item = item4)
    #view.add_item(item = item5)
    message = await inter.send("button test lmao", view = view)
    while True:
      try:
        interaction = await inter.bot.wait_for("interaction", check = lambda interaction: interaction.message == message, timeout = 60)
        if interaction.user.id == inter.author.id:
          await interaction.response.send_message(content = f"You clicked {interaction.data.custom_id}!", ephemeral = True)
        else:
          await interaction.response.send_message(content = "You can't click this button, Sorry!", ephemeral = True)
      except asyncio.TimeoutError:
        view.stop()
        break
        
  #test 3 (select command) command
  @commands.slash_command(name = "menu", description = "test command 3", hidden = True)
  async def select(inter):
    view = discord.ui.View(timeout = 60)
    view.add_item(discord.ui.Select(placeholder = "Select an option", options = [discord.SelectOption(label = "Option 1", emoji = "1️⃣", value = "1"), discord.SelectOption(label = "Option 2", emoji = "2️⃣", value = "2"), discord.SelectOption(label = "Option 3", emoji = "3️⃣", value = "3")]))
    message = await inter.send("Select Menu", view = view)
    while True:
      try:
        interaction = await inter.bot.wait_for("interaction", check = lambda interaction: interaction.message == message, timeout = 60)
        await interaction.send(content = f"You selected Option {view.children[0].values[0]}!", ephemeral = True)
      except asyncio.TimeoutError:
        view.stop()
        break

  #send emoji command
  @commands.slash_command(name = "sendemoji", description = "Send emoji as bot")
  async def slashsendemoji(inter, emoji: discord.Emoji):
    await inter.response.send_message(emoji.url)
    
def setup(bot):
  bot.add_cog(Nonsense(bot))