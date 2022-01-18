#cog by Number1#4325
import disnake as discord
from disnake.ext import commands
from enum import Enum
import random
import asyncio
import math
import datetime, time
from replit import db


whitelist_id = [439788095483936768, 417334153457958922, 902371374033670224, 691572882148425809, 293189829989236737, 826509766893371392, 835455268946051092, 901115550695063602]

class Required1(str, Enum):
  You = "True"
  Everyone = ""

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

  #listener
  #@commands.Cog.listener()
  #async def on_message_edit(self, ctx):
  #  if ctx.command.name == "eval":
  #    await self.eval(self, ctx, ctx.args[0])
    

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
  async def slashembed(inter, ephemeral: Required1, content = "", author_name = "", author_icon = "", title = "", desc = "", footer = "", footer_icon = "", thumbnail = "", image = ""):
    '''
    Makes an embed for you
    Parameters
    ----------
    ephemeral: Visibility of the embed, required
    content: Text outside embed, default is none
    author_name: Author name, default is your name
    author_icon: Author icon, default is your pfp
    title: Embed title, default is none
    desc: Embed Description, default is none
    footer: Embed footer, default is none
    footer_icon: Footer icon, default is none
    thumbnail: Embed thumbnail, default is none
    image: Embed image, default is none
    '''
    if author_icon == "":
      author_icon = str(inter.author.avatar)[:-10]
    if author_name == "":
      author_name = inter.author.name
    e = discord.Embed(title = title, description = desc, color = random.randint(0, 16777215))
    e.set_author(name = author_name, icon_url = author_icon)
    e.set_footer(text = footer, icon_url = footer_icon)
    e.set_thumbnail(url = thumbnail)
    e.set_image(url = image)
    await inter.send(content = content, embed = e, ephemeral = ephemeral)
  
  #embed 2.0 command
  @commands.slash_command(aliases = ["emb2"], description = "Makes more advanced embed with title, description, footer and image")
  async def embed2(inter, options = ""):
    blacklist = ["time.sleep", "sleep", "open", "exec", "license", "help", "exit", "quit", "os", "eval"]
    list = options.split("/ ")
    errornum = 0
    num = 0
    num2 = 1
    title = ""
    desc = ""
    footer = ""
    imagelink = ""
    thumblink = ""
    while num <= int(len(list) - 1):
      if "title:" in list[num]:
        if "|" in str(list[num])[6:]:
          if int(inter.author.id) in whitelist_id:
            codelist = str(list[num])[6:].split("|")
            num2 = 1
            while num2 < int(len(codelist) - 1):
              if any(i in codelist[num2] for i in blacklist):
                errornum = 1
                e = discord.Embed(title = "Error", description = "None", color = random.randint(0, 16777215))
                await inter.send(embed = e)
                break
              else:
                codelist[num2] = eval(codelist[num2], {'__builtins__': __builtins__, '__import__': None, 'eval': None, 'random': random, 'ctx': inter, 'int': int, 'str': str, 'len': len, 'time': time, 'datetime': datetime, 'mktime': time.mktime, 'math': math, 'quit': None, 'exit': None, 'help': None, 'license': None, 'exec': None, 'print': None, 'os': None, 'open': None, 'sleep': None, 'time.sleep': None})
                num2 += 2
            text = ""
            for x in codelist:
              text += str(x)
            title = text
          else:
            title = str(list[num])[6:]
        else:
          title = str(list[num])[6:]
      elif "desc:" in list[num]:
        if "|" in str(list[num])[5:]:
          if int(inter.author.id) in whitelist_id:
            codelist = str(list[num])[5:].split("|")
            num2 = 1
            while num2 < int(len(codelist) - 1):
              if any(i in codelist[num2] for i in blacklist):
                errornum = 1
                e = discord.Embed(title = "Error", description = "None", color = random.randint(0, 16777215))
                await inter.send(embed = e)
                break
              else:
                codelist[num2] = eval(codelist[num2], {'__builtins__': __builtins__, '__import__': None, 'eval': None, 'random': random, 'ctx': inter, 'int': int, 'str': str, 'len': len, 'time': time, 'datetime': datetime, 'mktime': time.mktime, 'math': math, 'quit': None, 'exit': None, 'help': None, 'license': None, 'exec': None, 'print': None, 'os': None, 'open': None, 'sleep': None, 'time.sleep': None})
                num2 += 2
            text = ""
            for x in codelist:
              text += str(x)
            desc = text
          else:
            desc = str(list[num])[5:]
        else:
          desc = str(list[num])[5:]
      elif "footer:" in list[num]:
        if "|" in str(list[num])[7:]:
          if int(inter.author.id) in whitelist_id:
            codelist = str(list[num])[7:].split("|")
            num2 = 1
            while num2 < int(len(codelist) - 1):
              if any(i in codelist[num2] for i in blacklist):
                errornum = 1
                e = discord.Embed(title = "Error", description = "None", color = random.randint(0, 16777215))
                await inter.send(embed = e)
                break
              else:
                codelist[num2] = eval(codelist[num2], {'__builtins__': __builtins__, '__import__': None, 'eval': None, 'random': random, 'ctx': inter, 'int': int, 'str': str, 'len': len, 'time': time, 'datetime': datetime, 'mktime': time.mktime, 'math': math, 'quit': None, 'exit': None, 'help': None, 'license': None, 'exec': None, 'print': None, 'os': None, 'open': None, 'sleep': None, 'time.sleep': None})
                num2 += 2
            text = ""
            for x in codelist:
              text += str(x)
            footer = text
          else:
            footer = str(list[num])[7:]
        else:
          footer = str(list[num])[7:]
      elif "imagelink:" in list[num]:
        imagelink = str(list[num])[10:]
      elif "thumblink:" in list[num]:
        thumblink = str(list[num])[10:]
      num += 1
    if not errornum == 1:
      e = discord.Embed(title = title, description = desc, color = random.randint(0, 16777215))
      e.set_author(name = inter.author.name, icon_url = inter.author.avatar)
      e.set_image(url = imagelink)
      e.set_thumbnail(url = thumblink)
      e.set_footer(text = footer)
      await inter.send(embed = e)

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