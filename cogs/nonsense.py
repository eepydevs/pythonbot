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
import js2py
import math
import datetime, time
import requests as rq
from replit import db

whitelist_id = [439788095483936768, 417334153457958922, 902371374033670224, 691572882148425809, 293189829989236737, 826509766893371392, 835455268946051092, 901115550695063602]

if "tupper" not in db:
  db["tupper"] = {}

class Required1(str, Enum):
  You = "True"
  Everyone = ""

class Required2(str, Enum):
  Normal = "Normal"
  Await = "Await"

class sendopt(str, Enum):
  Slash = "Slash"
  Seperate = "Seperate"
  Webhook = "Webhook"

class menuthing(discord.ui.Select):
  def __init__(self, inter: discord.Interaction):
    self.inter = inter
    options = [
      discord.SelectOption(label = "Option 1", emoji = "1️⃣", value = "1"),
      discord.SelectOption(label = "Option 2", emoji = "2️⃣", value = "2"),
      discord.SelectOption(label = "Option 3", emoji = "3️⃣", value = "3")
    ]

    super().__init__(
      placeholder="Select option",
      min_values=1,
      max_values=1,
      options=options,
    )
  async def interaction_check(self, inter: discord.MessageInteraction):
        if inter.author != self.inter.author:
            await inter.send("This selection menu is not for you", ephemeral = True)
            return False
        return True
    
  async def callback(self, interaction: discord.MessageInteraction):
    await interaction.send(f"You selected Option {self.values[0]}!", ephemeral = True)

class menuView(discord.ui.View):
  def __init__(self, inter: discord.Interaction):
      super().__init__()
      self.add_item(menuthing(inter))

class buttonthing(discord.ui.View):
  def __init__(self, inter: discord.Interaction):
    super().__init__(timeout = 60)
    self.inter = inter
    
  async def interaction_check(self, inter: discord.MessageInteraction):
    if inter.author != self.inter.author:
      await inter.send("Those buttons are not for you", ephemeral = True)
      return False
    return True
    
  @discord.ui.button(label = "Primary", custom_id = "Primary", emoji = "1️⃣", style = discord.ButtonStyle.blurple)
  async def primary_button(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
    await interaction.send("You clicked Primary", ephemeral = True)

  @discord.ui.button(label = "Secondary", custom_id = "Secondary", emoji = "2️⃣", style = discord.ButtonStyle.gray)
  async def secondary_button(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
    await interaction.send("You clicked Secondary", ephemeral = True)

  @discord.ui.button(label = "Success", custom_id = "Success", emoji = "✅", style = discord.ButtonStyle.green)
  async def success_button(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
    await interaction.send("You clicked Success", ephemeral = True)

  @discord.ui.button(label = "Danger", custom_id = "Danger", emoji = "⚠️", style = discord.ButtonStyle.red)
  async def danger_button(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
    await interaction.send("You clicked Danger", ephemeral = True)

  """@discord.ui.button(label = "Link", custom_id = "Link", emoji = "🔗", style = discord.ButtonStyle.gray)
  async def link_button(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
    await interaction.send("You clicked Link", ephemeral = True)""" #this one i guess is useless lmao
  # who useless? - UNKNOWN
  # guess who writed this!

  
def shuffle(x):
  return random.sample(x, len(x))

async def suggest_tupper(inter, input):
  return [tupper for tupper in db["tupper"][str(inter.author.id)][0:24].keys() if input.lower() in tupper.lower()] if db["tupper"][str(inter.author.id)] else ["You have nothing! Go create a tupper!"]

def runbf(str):
  array = [0] * 30000
  i = 0
  codei = 0
  codeiStack = []
  strp = []
  while codei < len(str):
    l = str[codei]
    #increase
    if l == '+':
      array[i] = ((array[i] + 1) % 255)
    #decrease
    elif l == '-':
      array[i] = ((array[i] - 1) % 255)
    #go one cell right
    elif l == ">":
      i += 1
    #go one cell left
    elif l == "<":
      i -= 1
    #input ascii character in strp array
    elif l == ".":
      strp.append(chr(array[i]))
    #join every letter in strp array and print
    elif l == '[':
      codeiStack.append(codei)
    elif l == ']':
      if array[i] != 0:
        #restart the loop
        codei = codeiStack[-1]
      else:
        #exit the loop
        codeiStack.pop()
    codei += 1
  if len(strp) != 0:
    return "".join(f"{ll}" for ll in strp)
  else:
    pass

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
    try:
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
    except:
      pass

  @commands.slash_command(name = "urban")
  async def slashurban(inter, query):
    '''
    See meaning of term you need
    Parameters
    ----------
    query: Your term here!
    '''
    try:
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
    except:
      e = discord.Embed(title = "Error", description = "Something went wrong...", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

  @commands.slash_command(name = "md")
  async def md(inter, *, ephemeral: Required1 = Required1.You, text):
    '''
    .md Format your message
    Parameters
    ----------
    ephemeral: Visibilty of embed
    text: Input text here, // for newline
    '''
    modtext = text.split("//")
    if modtext[0].strip().startswith("# "):
      title = modtext.pop(0)[2:]
    else:
      title = ".md format"
    if "\n".join(modtext).replace("- ", "• ").find("## ") == -1:
      desc = "\n".join(modtext).replace("- ", "• ")
    else:
      descindex = "\n".join(modtext).replace("- ", "• ").find("## ")
      desc = "\n".join(modtext).replace("- ", "• ")[:descindex]
    e = discord.Embed(title = title, description = desc, color = random.randint(0, 16777215))
    subheaders = "//".join(modtext).split("## ")
    indexsh = 1
    for item in modtext:
      if item.strip().startswith("## "):
        if "\n".join(subheaders[indexsh].split("//")[1:]).replace("- ", "• "):
          val = "\n".join(subheaders[indexsh].split("//")[1:]).replace("- ", "• ")
        else:
          val = "_ _"
        e.add_field(name = item[3:], value = val, inline = False)
        indexsh += 1
    await inter.send(embed = e, ephemeral = ephemeral)
    
    
  
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

    new_webhook = await inter.channel.create_webhook(name="PythonBot Webhook", reason="PythonBot webhook usage in commands")
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

  #eval python command
  @commands.slash_command(name = "evalpy", description = "ONLY FOR PEOPLE THAT ARE IN WHITELIST. Execute python code and see results")
  @commands.check(lambda inter: inter.author.id in whitelist_id)
  async def evalpy(inter, *, ephemeral: Required1 = Required1.You, send_way: Required2 = Required2.Normal, code):
    '''
    Only for people that are in whitelist

    Parameters
    ----------
    ephemeral: Visibility of eval
    send_way: Available ways: Normal, Await
    code: Code here
    '''
    blacklist = ["time.sleep", "sleep", "open", "exec", "license", "help", "exit", "quit", "os", "eval", "reset_cooldown", "run", "clear", "unload_extension", "load_extension", "leave"]
    try:
      if inter.author.id == inter.bot.owner.id:
        if send_way == "Normal":
          e = discord.Embed(title = "PyEval:", description = f"```py\n{code}\n```\nResult: ```\n{eval(code)}\n```", color = random.randint(0, 16777215)) 
          await inter.send(embed = e, ephemeral = ephemeral)
        elif send_way == "Await":
          e = discord.Embed(title = "Await PyEval:", description = f"```py\n{code}\n```", color = random.randint(0, 16777215))
          await inter.send(embed = e, ephemeral = ephemeral)
          await eval(code)
      else:
        if send_way == "Normal":
          if any(i in code for i in blacklist):
            e = discord.Embed(title = "Error", description = "```'NoneType' is not callable```", color = random.randint(0, 16777215))
            await inter.send(embed = e, ephemeral = True)
          else:
            e = discord.Embed(title = "PyEval:", description = f"```py\n{code}\n```\nResult:\n```\n{eval(code, {'__builtins__': __builtins__, '__import__': None, 'eval': None, 'random': random, 'inter': inter, 'int': int, 'str': str, 'len': len, 'time': time, 'datetime': datetime, 'mktime': time.mktime, 'math': math, 'quit': None, 'exit': None, 'help': None, 'license': None, 'exec': None, 'print': None, 'os': None, 'open': None, 'sleep': None, 'time.sleep': None, 'shuffle': lambda x: random.sample(x, len(x)), 'reset_cooldown': None, 'run': None, 'clear': None, 'unload_extension': None, 'load_extension': None, 'discord': discord})}\n```", color = random.randint(0, 16777215))
            await inter.send(embed = e, ephemeral = ephemeral)
        else:
          if any(i in code for i in blacklist):
            e = discord.Embed(title = "Error", description = "```'NoneType' is not callable```", color = random.randint(0, 16777215))
            await inter.send(embed = e, ephemeral = True)
          else:
            e = discord.Embed(title = "PyEval:", description = f"```py\n{code}\n```", color = random.randint(0, 16777215))
            await inter.send(embed = e, ephemeral = ephemeral)
            await eval(code, {'__builtins__': __builtins__, '__import__': None, 'eval': None, 'random': random, 'inter': inter, 'int': int, 'str': str, 'len': len, 'time': time, 'datetime': datetime, 'mktime': time.mktime, 'math': math, 'quit': None, 'exit': None, 'help': None, 'license': None, 'exec': None, 'print': None, 'os': None, 'open': None, 'sleep': None, 'time.sleep': None, 'shuffle': lambda x: random.sample(x, len(x)), 'reset_cooldown': None, 'run': None, 'clear': None, 'unload_extension': None, 'load_extension': None, 'discord': discord})
    except Exception as error:
      e = discord.Embed(title = "Error", description = f"```{error}```", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

  #eval javascript command
  @commands.slash_command(name = "evaljs", description = "bot owner only. Execute javascript code and see results")
  @commands.check(lambda inter: inter.author.id in whitelist_id)
  async def evaljs(inter, *, ephemeral: Required1 = Required1.You, code):
    '''
    nobody can use this sadly

    Parameters
    ----------
    ephemeral: Visibility of eval
    code: Code here
    '''
    try:
      if inter.author.id == inter.bot.owner.id:
        e = discord.Embed(title = "JSEval:", description = f"```js\n{code}\n```\nResult: ```\n{js2py.eval_js(code)}\n```", color = random.randint(0, 16777215)) 
        await inter.send(embed = e, ephemeral = ephemeral)
    except Exception as error:
      e = discord.Embed(title = "Error", description = f"```{error}```", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
    
  #eval brainfudge command
  @commands.slash_command(name = "execbf", description = "Execute brainfudge code and see results")
  async def evalbf(inter, *, ephemeral: Required1 = Required1.You, code):
    '''
    Execute brainfudge code and see the results

    Parameters
    ----------
    ephemeral: Visibility of eval
    code: Code here
    '''
    try:
      e = discord.Embed(title = "BFEval:", description = f"```bf\n{code}\n```\nResult: ```\n{runbf(code)}\n```", color = random.randint(0, 16777215)) 
      await inter.send(embed = e, ephemeral = ephemeral)
    except:
      e = discord.Embed(title = "Error", description = f"Something went wrong. Try again...", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
    
  
  #calculator command
  @commands.slash_command(name = "calc", description = "Calculate anything you need! (basic math)")
  async def slashcalculator(inter, equation):
    '''
    Calculate basic math

    Parameters
    ----------
    equation: Example: 1 + 1
    '''
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

      new_webhook = await inter.channel.create_webhook(name="PythonBot Webhook", reason="PythonBot webhook usage in commands")
      await new_webhook.send(content = content, embed = e, username = inter.bot.user.display_name, avatar_url = inter.bot.user.avatar)
    else:
      await inter.send(content = content, embed = e, ephemeral = ephemeral)

  #test 2 (buttons message) command
  @commands.slash_command(name = "button", description = "test command 2")
  async def slashbutton(inter):
    await inter.send("button test lol", view = buttonthing(inter))
        
  #test 3 (select command) command
  @commands.slash_command(name = "menu", description = "test command 3")
  async def select(inter):
    view = menuView(inter.author)

    await inter.send("Select Menu", view = view)

  #send emoji command
  @commands.slash_command(name = "sendemoji", description = "Send emoji as bot")
  async def slashsendemoji(inter, emoji: discord.Emoji):
    '''
    Send emoji as bot

    Parameters
    ----------
    emoji: Emoji here
    '''
    await inter.response.send_message(emoji.url)

  #someone command
  @commands.slash_command(name = "someone", description = "Ping random person (Just like @someone back in 2018)")
  @commands.has_permissions(administrator = True)
  async def someone(inter):
    while True:
      member = random.choice(inter.guild.members)
      if member.bot:
        continue
      else:
        break
    await inter.send(member.mention)

  #qrcode group
  @commands.slash_command()
  async def qrcode(self, inter):
    pass

  #create
  @qrcode.sub_command()
  async def create(self, inter, content: str):
    '''
    Create a qrcode i guess

    Parameters
    ----------
    content: Qrcode will contain content written here
    '''
    await inter.send(f"https://api.qrserver.com/v1/create-qr-code/?data={content[0:899].replace(' ', '%20').replace('/', '%2F').replace(':', '%3A').replace('=', '%3D').replace('?', '%3F')}&qzone=2&size=350x350")
    
  #read
  @qrcode.sub_command()
  async def read(self, inter, qrcode: str):
    '''
    Read a qrcode i guess
    
    Parameters
    ----------
    qrcode: Qrcode here (MUST BE A LINK)
    '''
    await inter.response.defer()
    json = rq.get(f"http://api.qrserver.com/v1/read-qr-code/?fileurl={qrcode.replace(' ', '%20').replace('/', '%2F').replace(':', '%3A').replace('=', '%3D').replace('?', '%3F')}").json()
    await inter.edit_original_message(content = f"Contents: {json[0]['symbol'][0]['data']}")

  #tupper group
  @commands.slash_command()
  async def tupper(self, inter):
    if str(inter.author.id) not in db["tupper"]:
      db["tupper"][str(inter.author.id)] = {}

  #create tupper
  @tupper.sub_command()
  async def create(self, inter, name, avatar):
    '''
    Create a tupper!

    Parameters
    ----------
    name: Name for tupper
    avatar: Avatar for tupper (MUST BE A LINK)
    '''
    if name not in db["tupper"][str(inter.author.id)]:
      db["tupper"][str(inter.author.id)].update({str(name): str(avatar)})
      e = discord.Embed(title = "Success", description = f"Tupper named: `{name}` is created!", color = random.randint(0, 16777215))
      e.set_image(url = avatar)
      await inter.send(embed = e, ephemeral = True)
    else:
      e = discord.Embed(title = "Error", description = f"Tupper named: `{name}` already exists!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

  #use tupper
  @tupper.sub_command()
  async def say(self, inter, *, tupper: str = commands.Param(autocomplete = suggest_tupper), content):
    '''
    Use tupper to say something!

    Parameters
    ----------
    tupper: Tupper you want to use
    content: Text here
    '''
    if tupper in db["tupper"][str(inter.author.id)]:
      e = discord.Embed(title = "Success", description = f"Successfully sent `{content}` as `{tupper}`", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      channel_webhooks = await inter.channel.webhooks()
      webhook_count = 0

      for webhook in channel_webhooks:
        if webhook.user.id == inter.bot.user.id and webhook.name == "PythonBot Webhook":
            await webhook.send(
                content = content, username = tupper, avatar_url = db["tupper"][str(inter.author.id)].get(tupper)
            )
            return

      new_webhook = await inter.channel.create_webhook(name="PythonBot Webhook", reason="PythonBot webhook usage in commands")
      await new_webhook.send(content = content, username = tupper, avatar_url = db["tupper"][str(inter.author.id)].get(tupper))
    else:
      e = discord.Embed(title = "Error", description = f"Tupper named: `{tupper}` doesn't exist!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

  #delete tupper
  @tupper.sub_command()
  async def delete(self, inter, tupper: str = commands.Param(autocomplete = suggest_tupper)):
    '''
    Delete existing tupper

    Parameters
    ----------
    tupper: Tupper you want to delete
    '''
    if tupper in db["tupper"][str(inter.author.id)]:
      del db["tupper"][str(inter.author.id)][tupper]
      e = discord.Embed(title = "Success", description = f"Tupper named: `{tupper}` is deleted!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
    else:
      e = discord.Embed(title = "Error", description = f"Tupper named: `{tupper}` doesn't exist!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

  #edit tupper
  @tupper.sub_command()
  async def edit(self, inter, *, tupper: str = commands.Param(autocomplete = suggest_tupper), new_name, avatar):
    '''
    Edit a tupper!

    Parameters
    ----------
    tupper: Tupper you want to edit
    new_name: New name for tupper
    avatar: New avatar for tupper (MUST BE A LINK)
    '''
    if tupper in db["tupper"][str(inter.author.id)]:
      del db["tupper"][str(inter.author.id)][tupper]
      db["tupper"][str(inter.author.id)].update({str(new_name): str(avatar)})
      e = discord.Embed(title = "Success", description = f"Tupper's name: `{tupper}` is now edited to `{new_name}`!", color = random.randint(0, 16777215))
      e.set_image(url = avatar)
      await inter.send(embed = e, ephemeral = True)
    else:
      e = discord.Embed(title = "Error", description = f"Tupper named: `{tupper}` doesn't exist!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

  @commands.slash_command()
  async def screenshot(inter, site: str):
    '''
    Screenshot a website

    Parameters
    ----------
    site: Site URL
    '''
    if any([site.startswith("https://"), site.startswith("http://")]):
      e = discord.Embed(title = site, description = "If you don't see image then url doesn't work", color = random.randint(0, 16777215))
      e.set_image(url = f"https://api.popcat.xyz/screenshot?url={site}")
      await inter.send(embed = e, ephemeral = True)
    else:
      e = discord.Embed(title = "Error", description = "Invalid URL", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      
def setup(bot):
  bot.add_cog(Nonsense(bot))