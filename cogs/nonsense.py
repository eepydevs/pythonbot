#cog by Number1#4325
import disnake as discord
from disnake.ext import commands
import random
import asyncio
import math
import datetime, time
from replit import db


whitelist_id = [439788095483936768, 417334153457958922, 902371374033670224, 691572882148425809, 293189829989236737, 826509766893371392, 835455268946051092]

def shuffle(x):
  return random.sample(x, len(x))

def calc(text):
  check = text.split(" ")
  whitelist = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "/", "%", "+", "-", "(", ")", " "]
  for i in range(len(check)):
    if len(check[i]) < 10:
      continue
    else:
      raise Exception("Maximum amount of characters per spaced string is 10!")
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
  @commands.command(aliases = ["e"], help = "Execute python code (limited)", description = "ONLY FOR PEOPLE THAT ARE IN WHITELIST\nExecute python code and see results\nexample: pb!eval random.randint(0, 10)", hidden = True)
  @commands.check(lambda ctx: ctx.author.id in whitelist_id)
  async def eval(self, ctx, *, code):
    blacklist = ["time.sleep", "sleep", "open", "exec", "license", "help", "exit", "quit", "os", "eval"]
    try:
      if ctx.author.id == ctx.bot.owner.id:
        e = discord.Embed(title = "Eval:", description = f"{eval(code)}", color = random.randint(0, 16777215)) 
        await ctx.send(embed = e)
        await ctx.message.add_reaction("✅")
      else:
        if any(i in code for i in blacklist):
          e = discord.Embed(title = "Error", description = "None", color = random.randint(0, 16777215))
          await ctx.send(embed = e)
          await ctx.message.add_reaction("❌")
        else:
          e = discord.Embed(title = "Eval:", description = f"{eval(code, {'__builtins__': __builtins__, '__import__': None, 'eval': None, 'random': random, 'ctx': ctx, 'int': int, 'str': str, 'len': len, 'time': time, 'datetime': datetime, 'mktime': time.mktime, 'math': math, 'quit': None, 'exit': None, 'help': None, 'license': None, 'exec': None, 'print': None, 'os': None, 'open': None, 'sleep': None, 'time.sleep': None, 'shuffle': lambda x: random.sample(x, len(x))})}", color = random.randint(0, 16777215))
          await ctx.send(embed = e)
          await ctx.message.add_reaction("✅")
    except Exception as error:
      e = discord.Embed(title = "Error", description = error, color = random.randint(0, 16777215))
      await ctx.send(embed = e)
      await ctx.message.add_reaction("❌")
  
  #calculator command
  @commands.command(aliases = ["calc"], help = "Calculate anything you need! (basic math)", description = "Usage: pb!calculator (equation)\nExample: pb!calculator 1 + 2\nOutput: 3")
  async def calculator(self, ctx, *, equation):
    try:
      e = discord.Embed(title = "Calculator", description = f"{equation} = {calc(equation)}", color = random.randint(0, 16777215))
      await ctx.send(embed = e)
    except ValueError:
      e = discord.Embed(title = "Calculator", description = "Something went wrong... (You may have used non-int)", color = random.randint(0, 16777215))
      await ctx.send(embed = e)
  
  #embed command
  @commands.command(aliases = ["emb"], help = "Makes embed with title, description and footer", description = "You can make embeds with this command\nUsage: `pb!embed (title) (description) (footer)`\nExample: `pb!embed \"Hello title!\" \"Hello description!\" \"Hello footer!\"`")
  async def embed(self, ctx, title = "", desc = "", footer = ""):
    e = discord.Embed(title = title, description = desc, color = random.randint(0, 16777215))
    e.set_author(name =  ctx.author.name, icon_url = str(ctx.author.avatar)[:-10])
    e.set_footer(text = footer)
    await ctx.send(embed = e)
  
  #embed 2.0 command
  @commands.command(aliases = ["emb2"], help = "Makes more advanced embed with title, description, footer and image", description = "You can make embeds with this command\nUsage: `pb!embed2 (title:text)/ (desc:text)/ (footer:text)/ (imagelink:link)/ (thumblink:link)`\nExample: `pb!embed2 title:Hello title!/ desc:Hello description!/ footer:Hello footer!/ imagelink:*link here*/ thumblink:*link here*`\nYou can execute python code (limited) with |*code*|\nEXECUTING CODE WORKS ONLY FOR WHITELISTED PEOPLE!")
  async def embed2(self, ctx, *, options = ""):
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
          if int(ctx.author.id) in whitelist_id:
            codelist = str(list[num])[6:].split("|")
            num2 = 1
            while num2 < int(len(codelist) - 1):
              if any(i in codelist[num2] for i in blacklist):
                errornum = 1
                e = discord.Embed(title = "Error", description = "None", color = random.randint(0, 16777215))
                await ctx.send(embed = e)
                break
              else:
                codelist[num2] = eval(codelist[num2], {'__builtins__': __builtins__, '__import__': None, 'eval': None, 'random': random, 'ctx': ctx, 'int': int, 'str': str, 'len': len, 'time': time, 'datetime': datetime, 'mktime': time.mktime, 'math': math, 'quit': None, 'exit': None, 'help': None, 'license': None, 'exec': None, 'print': None, 'os': None, 'open': None, 'sleep': None, 'time.sleep': None})
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
          if int(ctx.author.id) in whitelist_id:
            codelist = str(list[num])[5:].split("|")
            num2 = 1
            while num2 < int(len(codelist) - 1):
              if any(i in codelist[num2] for i in blacklist):
                errornum = 1
                e = discord.Embed(title = "Error", description = "None", color = random.randint(0, 16777215))
                await ctx.send(embed = e)
                break
              else:
                codelist[num2] = eval(codelist[num2], {'__builtins__': __builtins__, '__import__': None, 'eval': None, 'random': random, 'ctx': ctx, 'int': int, 'str': str, 'len': len, 'time': time, 'datetime': datetime, 'mktime': time.mktime, 'math': math, 'quit': None, 'exit': None, 'help': None, 'license': None, 'exec': None, 'print': None, 'os': None, 'open': None, 'sleep': None, 'time.sleep': None})
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
          if int(ctx.author.id) in whitelist_id:
            codelist = str(list[num])[7:].split("|")
            num2 = 1
            while num2 < int(len(codelist) - 1):
              if any(i in codelist[num2] for i in blacklist):
                errornum = 1
                e = discord.Embed(title = "Error", description = "None", color = random.randint(0, 16777215))
                await ctx.send(embed = e)
                break
              else:
                codelist[num2] = eval(codelist[num2], {'__builtins__': __builtins__, '__import__': None, 'eval': None, 'random': random, 'ctx': ctx, 'int': int, 'str': str, 'len': len, 'time': time, 'datetime': datetime, 'mktime': time.mktime, 'math': math, 'quit': None, 'exit': None, 'help': None, 'license': None, 'exec': None, 'print': None, 'os': None, 'open': None, 'sleep': None, 'time.sleep': None})
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
      e.set_author(name = ctx.author.name, icon_url = ctx.author.avatar)
      e.set_image(url = imagelink)
      e.set_thumbnail(url = thumblink)
      e.set_footer(text = footer)
      await ctx.send(embed = e)

  #contains command
  @commands.command(aliases = ["includes"], help = "See if any word contains selected letter/word", description = "Example: pb!contains b abc\nexample 2: ?contains hello \"hello world\"")
  async def contains(self, ctx, letter_or_word, word):
    result = str(letter_or_word in word)
    e = discord.Embed(title = "Results of ?contains:", description = f"Does {word} contain {letter_or_word}?: {result}", color = random.randint(0, 16777215))
    await ctx.send(embed = e)

  #test (edit message) command
  @commands.command(help = "test command", description = "example: pb!edit \"hello\" 10 \"hello world\"\nnum = seconds")
  async def edit(self, ctx, text, num: int, editedtext):
    msg = await ctx.send(text)
    await asyncio.sleep(num)
    await msg.edit(content = editedtext)

  #test 2 (buttons message) command
  @commands.command(help = "test command 2", description = "idk lol", hidden = True)
  async def button(self, ctx):
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
    await ctx.send("button test lmao", view = view)
    while True:
        interaction = await self.bot.wait_for("interaction")
        if interaction.user.id == ctx.author.id:
          await interaction.send(content = f"You clicked a button!", ephemeral = True)
        else:
          await interaction.send(content = "You can't click this button, Sorry!", ephemeral = True)
  
  #test 3 (select command) command
  @commands.command(aliases = ["menu"], help = "test command 3", hidden = True)
  async def select(self, ctx):
    view = discord.ui.View(timeout = 60)
    view.add_item(discord.ui.Select(placeholder = "Select an option", options = [discord.SelectOption(label = "Option 1", emoji = "1️⃣", value = "1"), discord.SelectOption(label = "Option 2", emoji = "2️⃣", value = "2"), discord.SelectOption(label = "Option 3", emoji = "3️⃣", value = "3")]))
    message = await ctx.send("Select Menu", view = view)
    while True:
      try:
        interaction = await self.bot.wait_for("interaction", check = lambda interaction: interaction.message == message, timeout = 60)
        await interaction.send(content = f"You selected Option {view.children[0].values[0]}!", ephemeral = True)
      except asyncio.TimeoutError:
        view.stop()
        break

  #send emoji command
  @commands.command(aliases = ["sendemo", "semo"], help = "Send emoji as bot", description = "Send selected emoji")
  async def sendemoji(self, ctx, emoji: discord.Emoji):
    await ctx.trigger_typing()
    await ctx.send(emoji.url)

  #create invite command
  #fixed annoying spelling mistake
  @commands.command(aliases = ["cinvite"], help = "Create an invite for server you're currently in", description = "Send help\nExample: pb!createinvite 1 (after 1 days invite expires) 0 (0 = infinity uses)\nNote: Max days: 7, max uses: 100\nHas cooldown of 1 minute")
  @commands.cooldown(rate = 1, per = 60, type = commands.BucketType.user)
  async def createinvite(self, ctx, days: int = 7, uses: int = 0):
    try:
      maxage = 86400 * days
      invite = await ctx.channel.create_invite(max_age = maxage, max_uses = uses, unique = False)
      await ctx.send(f"Link: {invite.url}")
    except ValueError:
      await ctx.send("Error: Alls the arguments must be ints!")
      ctx.command.reset_cooldown(ctx)

  #youare command
  @commands.command(aliases = ["imare"], help = "See how you are `N% _____` (nice, cool for example)", description = "Usage: pb!youare (text)\nExample: `pb!youare Nice`\nOutput: You are 65% Nice")
  async def youare(self, ctx, *, text = ""):
    percentage = random.randint(0, 100)
    e = discord.Embed(title = f"{ctx.author.name},", description = f"You are {percentage}% {text}", color = random.randint(0, 16777215))
    await ctx.send(embed = e)
      
def setup(bot):
  bot.add_cog(Nonsense(bot))