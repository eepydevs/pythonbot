#cog by Number1#4325
import disnake as discord
from disnake.ext import commands
import random
import asyncio
from replit import db

responselist = ["Yes.", "It is certain.", "It is decidedly so.", "Without a doubt.", "Yes definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Signs point to yes.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good...", "Very doubtful.", "Maybe...", "No.", "Possibly.."]


class Fun(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  #say command
  @commands.command(help = "Repeats the thing you said", description = "Usage: pb!say (text)")
  async def say(self, ctx, *, text):
    await ctx.send(f"{text}")

  #choose command
  @commands.command(aliases = ["choice", "choices"], help = "Let the bot to choose something", description = "Usage: pb!choose (*options)\nExample: pb!choose 'thing 1' 'thing 2' 'thing 3'")
  async def choose(self, ctx, *options):
    e = discord.Embed(title = "Choice:", description = f"I choose.. {random.choice(options)}", color = random.randint(0, 16777215))
    await ctx.send(embed = e)
    

  #8ball command
  @commands.command(aliases = ["8ball"], help = "Say any Y/N question and 8ball will answer!", description = "Usage: pb!eightball (text)")
  async def eightball(self, ctx, *, text = ""):
    if text != "":
      e = discord.Embed(title = f"{ctx.author.name}: {text}", description = f"🎱: {random.choice(responselist)}", color = random.randint(0, 16777215))
      if str(ctx.author.id) in db["debug"]:
        e.add_field(name = "Debug", value = f"Variables value:\n{responselist}")
      await ctx.send(embed = e)
    else:
      e = discord.Embed(title = "Error", description = "Type a Y/N question!", color = random.randint(0, 16777215))
      await ctx.send(embed = e)
  
  #coinflip command
  @commands.command(aliases = ["coin"], help = "Flip a coin and get `Heads` or `Tails`", description = "Usage: pb!coinflip")
  async def coinflip(self, ctx):
    e = discord.Embed(title = "The coin flips...", description = "Wait for result", color = random.randint(0, 16777215))
    msg = await ctx.send(embed = e)
    await asyncio.sleep(1)
    e = discord.Embed(title = "Coin landed", description = f"Results: {random.choice(('Tails', 'Heads'))}", color = random.randint(0, 16777215))
    await  msg.edit(embed = e)

  #random command
  @commands.command(aliases = ["rd", "rng"], help = "RNG", description = "You can randomize numbers with this command\nUsage: pb!random (N1) (N2)\nUsage 2: pb!random (N1)")
  async def random(self, ctx, num1: int = None, num2: int = None):
    if num1 != None and num2 != None:
      if num1 < num2:
        randomized = random.randint(num1, num2)
        e = discord.Embed(title = f"Randomized Number: {str(randomized)}", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
      elif num1 == num2:
        await ctx.send("Error: N1 is equal to N2!")
      else:
        randomized = random.randint(num2, num1)
        e = discord.Embed(title = f"Randomized Number: {str(randomized)}", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
    else:
      randomized = random.randrange(num1)
      e = discord.Embed(title = f"Randomized Number: {str(randomized)}", color = random.randint(0, 16777215))
      await ctx.send(embed = e)

  #dice command
  @commands.command(help = "RNG 2", description = "Throw dices")
  async def dice(self, ctx, dices: int = None, faces: int = None):
    if dices != None and faces != None:
      if dices >= 1 and faces >= 1:
        dice = random.randint(1, int(faces * dices))
        e = discord.Embed(title = "Dice", description = f"Number: {dice}", color = random.randint(0, 16777215))
        e.set_thumbnail(url = "https://cdn.discordapp.com/attachments/843562496543817781/905114307556163614/dice.png")
        await ctx.send(embed = e)
      else: 
        await ctx.send("Error: Invalid input")
    else:
      dice = random.randint(1, 6)
      e = discord.Embed(title = "Dice", description = f"Number: {dice}", color = random.randint(0, 16777215))
      e.set_thumbnail(url = "https://cdn.discordapp.com/attachments/843562496543817781/905114307556163614/dice.png")
      await ctx.send(embed = e)

  #math command
  @commands.command(help = "Math questions, wohooo very fun..")
  async def math(self, ctx):
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
      if str(ctx.author.id) in db["debug"]:
        e.add_field(name = "Debug", value = f"Variables value:\n{answer}")
      await ctx.send(embed = e)
      try:
        message = await self.bot.wait_for("message", check = lambda message: message.author == ctx.author and message.channel == ctx.channel, timeout = 60)
        if int(message.content) == answer:
          rng = random.randint(250, 1000)
          e = discord.Embed(title = "Correct!", description = f"It was {answer}", color = random.randint(0, 16777215))
          await ctx.send(embed = e)
        else:
          rng = random.randint(50, 250)
          db["balance"][str(ctx.author.id)] += rng
          e = discord.Embed(title = "Incorrect", description = f"The right answer was {answer}", color = random.randint(0, 1677215))
          await ctx.send(embed = e)
      except asyncio.TimeoutError:
        rng = random.randint(50, 250)
        db["balance"][str(ctx.author.id)] += rng
        e = discord.Embed(title = "Incorrect", description = f"The right answer was {answer}", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
      except ValueError:
        rng = random.randint(50, 250)
        db["balance"][str(ctx.author.id)] += rng
        e = discord.Embed(title = "Incorrect", description = f"The right answer was {answer}", color = random.randint(0, 16777215))
        await ctx.send(embed = e)

  #guess the number command
  @commands.command(aliases = ["gtn"], help = "Guess the number minigame!", description = "Type `stop`/`close`/`leave`/`quit`/`exit` to stop playing\nThe `max` argument is used for maximum amount of count\nThe `tries_amt` argument is used for maximum amount of tries\nNote: 0 in `tries_amt` means infinity tries")
  async def guessthenumber(self, ctx, max: int = 100, tries_amt: int = 0):
    botnum = random.randint(0, max)
    tries = 1
    infinity = False
    if tries_amt == 0:
      infinity = True
    e = discord.Embed(title = "Guess the number!", color = random.randint(0, 16777215))
    e.add_field(name = "Settings", value = f"Infinity tries: {infinity}\nMax tries: {tries_amt}")
    if str(ctx.author.id) in db["debug"]:
      e.add_field(name = "Debug", value = f"Variables value:\n{infinity}, {tries_amt}, {botnum}, {tries}")
    await ctx.send(embed = e)
    while True:
      if infinity == False and tries > tries_amt:
        e = discord.Embed(title = "You lost", description = f"The right answer was {botnum}", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
        break
      message = await self.bot.wait_for("message", check = lambda message: message.author == ctx.author and message.channel == ctx.channel, timeout = 30)
      if message.content.lower() != "stop" and message.content.lower() != "close" and message.content.lower() != "leave" and message.content.lower() != "quit" and message.content.lower() != "exit":
        try:
          if int(message.content) == botnum:
            rng = random.randint(250, 1000)
            e = discord.Embed(title = "Correct!", description = f"Congrats you won\nIt was {botnum}", color = random.randint(0, 16777215))
            e.set_footer(text = f"Took you: {tries} tries")
            await ctx.send(embed = e)
            break
          elif int(message.content) < botnum:
            e = discord.Embed(title = "Incorrect", description = f"Try higher", color = random.randint(0, 1677215))
            if str(ctx.author.id) in db["debug"]:
              e.add_field(name = "Debug", value = f"Variables value:\n{infinity}, {tries_amt}, {botnum}, {tries}")
            e.set_footer(text = f"{tries} Tries")
            await ctx.send(embed = e)
            tries += 1
          elif int(message.content) > botnum:
            e = discord.Embed(title = "Incorrect", description = f"Try lower", color = random.randint(0, 1677215))
            if str(ctx.author.id) in db["debug"]:
              e.add_field(name = "Debug", value = f"Variables value:\n{infinity}, {tries_amt}, {botnum}, {tries}")
            e.set_footer(text = f"{tries} Tries")
            await ctx.send(embed = e)
            tries += 1
        except asyncio.TimeoutError:
          rng = random.randint(50, 250)
          db["balance"][str(ctx.author.id)] += rng
          e = discord.Embed(title = "Timeout", description = f"The right answer was {botnum}", color = random.randint(0, 16777215))
          await ctx.send(embed = e)
        except TimeoutError:
          rng = random.randint(50, 250)
          db["balance"][str(ctx.author.id)] += rng
          e = discord.Embed(title = "Timeout", description = f"The right answer was {botnum}", color = random.randint(0, 16777215))
          await ctx.send(embed = e)
        except ValueError:
          rng = random.randint(50, 250)
          db["balance"][str(ctx.author.id)] += rng
          e = discord.Embed(title = "Input error: Try again", color = random.randint(0, 16777215))
          if str(ctx.author.id) in db["debug"]:
            e.add_field(name = "Debug", value = f"Variables value:\n{infinity}, {tries_amt}, {botnum}, {tries}")
          await ctx.send(embed = e)
      else:
        e = discord.Embed(title = "You left", description = f"The right answer was {botnum}", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
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