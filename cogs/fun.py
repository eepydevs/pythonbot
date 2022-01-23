#cog by Number1#4325
import disnake as discord
from disnake.ext import commands
import requests
import random
import asyncio
from replit import db

responselist = ["Yes.", "It is certain.", "It is decidedly so.", "Without a doubt.", "Yes definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Signs point to yes.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good...", "Very doubtful.", "Maybe...", "No.", "Possibly..", "Concentrate and ask again.", "Cannot predict now.", "Ask again later."]
random.shuffle(responselist)


class Fun(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  #clicker experiment command idk
  @commands.command(aliases = ["click"], help = "(BETA)", description = "Play clicker in discord in a bot ultra hd 8k 144fps (BETA)")
  async def clicker(self, ctx):
    coins = 0
    color = random.randint(0, 16777215)
    e = discord.Embed(title = "Clicker", description = f"You have {coins}", color = color)
    e.set_author(name = ctx.author.name, icon_url = ctx.author.avatar)
    view = discord.ui.View(timeout = 60)
    style = discord.ButtonStyle.blurple
    item = discord.ui.Button(style = style, label = "Click here", custom_id = "click", emoji = "🖱️")
    view.add_item(item = item)
    message = await ctx.send(embed = e, view = view)
    while True:
      try:
        interaction = await self.bot.wait_for("interaction", check = lambda interaction: interaction.message == message, timeout = 60)
        if interaction.user.id == ctx.author.id:
          if interaction.data.custom_id == "click":
            #await interaction.response.send_message(content = f"You clicked {interaction.data.custom_id} {coins}!", ephemeral = True)
            coins += 1
            e = discord.Embed(title = "Clicker", description = f"You have {coins}", color = color)
            e.set_author(name = ctx.author.name, icon_url = ctx.author.avatar)
            await interaction.response.edit_message(embed = e)
        else:
          await interaction.response.send_message(content = "You can't click this button, Sorry!", ephemeral = True)
      except:
        await message.edit(view = None)
        view.stop
        break
  
  @commands.slash_command(name = "getmeme", description = "Get a meme lol")
  async def slashmeme(inter):
    r = requests.get("https://meme-api.herokuapp.com/gimme")
    rjson = r.json()
    while True:
      if str(rjson['nsfw']).title() == "True":
        r = requests.get("https://meme-api.herokuapp.com/gimme")
        rjson = r.json()
      else:
        break
    e = discord.Embed(title = f"{rjson['title']}", description = f"Link: {rjson['postLink']}\nMeme by: {rjson['author']}", color = random.randint(0, 16777215))
    e.set_image(url = f"{rjson['url']}")
    e.set_footer(text = f"👍: {rjson['ups']}")
    await inter.send(embed = e)


  #say command slash
  @commands.slash_command(name = "say", description = "Repeats the thing you said")
  async def slashsay(inter, text):
    await inter.response.send_message(f"{text}")
  
  #choose command slash
  @commands.slash_command(name = "choice", description = "Usage: /choice thing 1, thing2, 3 thing")
  async def slashchoice(inter, options):
    e = discord.Embed(title = "Choice:", description = f"I choose.. {random.choice(options.split(', '))}", color = random.randint(0, 16777215))
    await inter.response.send_message(embed = e)    

  #8ball command slash
  @commands.slash_command(name = "8ball",description = "Usage: pb!eightball (text)")
  async def slasheightball(inter, text):
    random.shuffle(responselist)
    e = discord.Embed(title = f"{inter.author.name}: {text}", description = f"🎱: {random.choice(responselist)}", color = random.randint(0, 16777215))
    if str(inter.author.id) in db["debug"]:
      e.add_field(name = "Debug", value = f"Variables value:\n{responselist}")
    await inter.response.send_message(embed = e)
  
  #coinflip command slash
  @commands.slash_command(name = "coinflip", description = "Flip a coin and get `Heads` or `Tails`")
  async def slashcoinflip(inter):
    e = discord.Embed(title = "Coin flipped", description = f"Results: {random.choice(('Tails', 'Heads'))}", color = random.randint(0, 16777215))
    await inter.response.send_message(embed = e)

  #random command slash
  @commands.slash_command(name = "random", description = "You can randomize numbers with this command\nUsage: pb!random (N1) (N2)\nUsage 2: pb!random (N1)")
  async def slashrandom(inter, num1: int, num2: int):
    if num1 < num2:
      randomized = random.randint(num1, num2)
      e = discord.Embed(title = f"Randomized Number: {str(randomized)}", color = random.randint(0, 16777215))
      await inter.response.send_message(embed = e)
    elif num1 == num2:
      await inter.response.send_message("Error: N1 is equal to N2!")
    else:
      randomized = random.randint(num2, num1)
      e = discord.Embed(title = f"Randomized Number: {str(randomized)}", color = random.randint(0, 16777215))
      await inter.response.send_message(embed = e)

  #dice command slash
  @commands.slash_command(name = "dice", description = "Throw dices")
  async def slashdice(inter, dices: int, faces: int):
    if dices >= 1 and faces >= 1:
      dice = random.randint(1, int(faces * dices))
      e = discord.Embed(title = "Dice", description = f"Number: {dice}", color = random.randint(0, 16777215))
      e.set_thumbnail(url = "https://cdn.discordapp.com/attachments/843562496543817781/905114307556163614/dice.png")
      await inter.response.send_message(embed = e)
    else: 
      await inter.response.send_message("Error: Invalid input")

  #math command
  @commands.slash_command(name = "math", description = "Math questions, wohooo very fun..")
  async def slashmath(inter):
      firstNum = random.randint(0, 1000)
      secondNum = random.randint(0, 1000)
      chance = random.randint(0, 100)
      if chance < 25:
        question = f"{firstNum} + {secondNum}"
        answer = firstNum + secondNum
      elif chance < 50:
        question = f"{firstNum} - {secondNum}"
        answer = firstNum - secondNum
      elif chance < 75:
        firstNum = random.randint(0, 50)
        secondNum = random.randint(0, 10)
        question = f"{firstNum} * {secondNum}"
        answer = round(firstNum * secondNum)
      else:
        firstNum = random.randint(0, 50)
        secondNum = random.randint(1, 10)
        question = f"{firstNum} / {secondNum} (rounded)"
        answer = round(firstNum / secondNum)
      
      e = discord.Embed(title = "Math question", description = f"{question} = ?", color = random.randint(0, 16777215))
      if str(inter.author.id) in db["debug"]:
        e.add_field(name = "Debug", value = f"Variables value:\n{answer}")
      await inter.send(embed = e)
      try:
        message = await inter.bot.wait_for("message", check = lambda message: message.author == inter.author and message.channel == inter.channel, timeout = 60)
        if int(message.content) == answer:
          e = discord.Embed(title = "Correct!", description = f"It was {answer}", color = random.randint(0, 16777215))
          await inter.send(embed = e)
        else:
          e = discord.Embed(title = "Incorrect", description = f"The right answer was {answer}", color = random.randint(0, 1677215))
          await inter.send(embed = e)
      except asyncio.TimeoutError:
        e = discord.Embed(title = "Incorrect", description = f"The right answer was {answer}", color = random.randint(0, 16777215))
        await inter.send(embed = e)
      except ValueError:
        e = discord.Embed(title = "Incorrect", description = f"The right answer was {answer}", color = random.randint(0, 16777215))
        await inter.send(embed = e)

  #guess the number command slash
  @commands.slash_command(name = "guessthenumber", description = "The `max` arg is max count. The `tries_amt` arg is max tries. Note: 0 in `tries_amt` = inf tries")
  async def slashguessthenumber(inter, max: int = 100, tries_amt: int = 0):
    botnum = random.randint(0, max)
    tries = 1
    infinity = False
    if tries_amt == 0:
      infinity = True
    e = discord.Embed(title = "Guess the number!", color = random.randint(0, 16777215))
    e.add_field(name = "Settings", value = f"Infinity tries: {infinity}\nMax tries: {tries_amt}", inline = False)
    e.add_field(name = "Info", value = "Type `stop`/`close`/`leave`/`quit`/`exit` to stop playing", inline = False)
    if str(inter.author.id) in db["debug"]:
      e.add_field(name = "Debug", value = f"Variables value:\n{infinity}, {tries_amt}, {botnum}, {tries}")
    await inter.send(embed = e)
    while True:
      if infinity == False and tries > tries_amt:
        e = discord.Embed(title = "You lost", description = f"The right answer was {botnum}", color = random.randint(0, 16777215))
        await inter.send(embed = e)
        break
      message = await inter.bot.wait_for("message", check = lambda message: message.author == inter.author and message.channel == inter.channel, timeout = 30)
      if message.content.lower() != "stop" and message.content.lower() != "close" and message.content.lower() != "leave" and message.content.lower() != "quit" and message.content.lower() != "exit":
        try:
          if int(message.content) == botnum:
            rng = random.randint(250, 1000)
            e = discord.Embed(title = "Correct!", description = f"Congrats you won\nIt was {botnum}", color = random.randint(0, 16777215))
            e.set_footer(text = f"Took you: {tries} tries")
            await inter.send(embed = e)
            break
          elif int(message.content) < botnum:
            e = discord.Embed(title = "Incorrect", description = f"Try higher", color = random.randint(0, 1677215))
            if str(inter.author.id) in db["debug"]:
              e.add_field(name = "Debug", value = f"Variables value:\n{infinity}, {tries_amt}, {botnum}, {tries}")
            e.set_footer(text = f"{tries} Tries")
            await inter.send(embed = e)
            tries += 1
          elif int(message.content) > botnum:
            e = discord.Embed(title = "Incorrect", description = f"Try lower", color = random.randint(0, 1677215))
            if str(inter.author.id) in db["debug"]:
              e.add_field(name = "Debug", value = f"Variables value:\n{infinity}, {tries_amt}, {botnum}, {tries}")
            e.set_footer(text = f"{tries} Tries")
            await inter.send(embed = e)
            tries += 1
        except asyncio.TimeoutError:
          rng = random.randint(50, 250)
          db["balance"][str(inter.author.id)] += rng
          e = discord.Embed(title = "Timeout", description = f"The right answer was {botnum}", color = random.randint(0, 16777215))
          await inter.send(embed = e)
        except TimeoutError:
          rng = random.randint(50, 250)
          db["balance"][str(inter.author.id)] += rng
          e = discord.Embed(title = "Timeout", description = f"The right answer was {botnum}", color = random.randint(0, 16777215))
          await inter.send(embed = e)
        except ValueError:
          rng = random.randint(50, 250)
          db["balance"][str(inter.author.id)] += rng
          e = discord.Embed(title = "Input error: Try again", color = random.randint(0, 16777215))
          if str(inter.author.id) in db["debug"]:
            e.add_field(name = "Debug", value = f"Variables value:\n{infinity}, {tries_amt}, {botnum}, {tries}")
          await inter.send(embed = e)
      else:
        e = discord.Embed(title = "You left", description = f"The right answer was {botnum}", color = random.randint(0, 16777215))
        await inter.send(embed = e)
        break

  #rps command
  @commands.command(help = "Play rock paper scissors", description = "Moves: Rock, Paper, Scissors")
  async def rps(self, ctx):
    moves = ("Rock", "Paper", "Scissors")
    view = discord.ui.View(timeout = 60)
    view.add_item(discord.ui.Select(placeholder = "Select an option", options = [discord.SelectOption(label = "Rock", emoji = "🪨", value = "Rock"), discord.SelectOption(label = "Paper", emoji = "📄", value = "Paper"), discord.SelectOption(label = "Scissors", emoji = "✂️", value = "Scissors")]))
    e = discord.Embed(title = "RPS", description = "Choose a move below!", color = random.randint(0, 16777215))
    message = await ctx.send(embed = e, view = view)
    while True:
      try:
        interaction = await self.bot.wait_for("interaction", check = lambda interaction: interaction.message == message, timeout = 60)
        p1 = moves.index(view.children[0].values[0].capitalize())
        p2 = random.randrange(0, len(moves))

        if p1 - p2 in (-2, 1):
          e = discord.Embed(title = f"{ctx.author.name} won!", description = "Congratulations!", color = random.randint(0, 16777215))
          e.set_footer(text = f"{ctx.author.name}: {moves[p1]} | Python bot: {moves[p2]}")
          await message.edit(embed = e, view = None)
          view.stop()
          break
        elif p1 - p2 in (-1, 2):
          e = discord.Embed(title = f"{ctx.author.name} lost!", description = "Be lucky next time!", color = random.randint(0, 16777215))
          e.set_footer(text = f"{ctx.author.name}: {moves[p1]} | Python bot: {moves[p2]}")
          await message.edit(embed = e, view = None)
          view.stop()
          break
        else:
          e = discord.Embed(title = "Tie!", description = "Quite lucky", color = random.randint(0, 16777215))
          e.set_footer(text = f"{ctx.author.name}: {moves[p1]} | Python bot: {moves[p2]}")
          await message.edit(embed = e, view = None)
          view.stop()
          break
      except asyncio.TimeoutError:
        await message.edit(content = "Timed out")
        view.stop()
        break
  
    """
    Rock & Paper: Lose -1
    Rock & Scissors: Win -2
    Paper & Rock: Win 1
    Paper & Scissors: Lose -1
    Scissors & Rock: Lose 2
    Scissors & Paper: Win 1
    """

def setup(bot):
  bot.add_cog(Fun(bot))