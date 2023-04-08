#cog by maxy#2866
import disnake as discord
from disnake.ext import commands
import random
import asyncio
import os
from utils import PopcatAPI, db

popcat = PopcatAPI()

responselist = ["Yes.", "It is certain.", "It is decidedly so.", "Without a doubt.", "Yes definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Signs point to yes.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good...", "Very doubtful.", "Maybe...", "No.", "Possibly..", "Concentrate and ask again.", "Cannot predict now.", "Ask again later."]
random.shuffle(responselist)

if "queue" not in db:
  db["queue"] = None

class menurps(discord.ui.View):
  def __init__(self, inter: discord.Interaction):
    super().__init__(timeout = 60)
    self.inter = inter

  async def move(self, inter: discord.MessageInteraction, button: discord.ui.Button):
    moves = ("Rock", "Paper", "Scissors")
    p1 = moves.index(button.custom_id.capitalize())
    p2 = moves.index(random.choice(moves))

    if p1 - p2 in (-2, 1):
      e = discord.Embed(title = f"{inter.author.name} won!", description = "Congratulations!", color = random.randint(0, 16777215))
      e.set_footer(text = f"{inter.author.name}: {moves[p1]} | Python Bot: {moves[p2]}")
      await inter.response.edit_message(embed = e, view = None)
      return
    elif p1 - p2 in (-1, 2):
      e = discord.Embed(title = f"{inter.author.name} lost!", description = "Be lucky next time!", color = random.randint(0, 16777215))
      e.set_footer(text = f"{inter.author.name}: {moves[p1]} | Python Bot: {moves[p2]}")
      await inter.response.edit_message(embed = e, view = None)
      return
    else:
      e = discord.Embed(title = "Tie!", description = "Quite lucky", color = random.randint(0, 16777215))
      e.set_footer(text = f"{inter.author.name}: {moves[p1]} | Python Bot: {moves[p2]}")
      await inter.response.edit_message(embed = e, view = None)
      return

  async def interaction_check(self, inter: discord.MessageInteraction):
    if inter.author != self.inter.author:
      await inter.send("Those buttons are not for you", ephemeral = True)
      return False
    return True

  @discord.ui.button(label = "Rock", custom_id = "Rock", emoji = "🪨", style = discord.ButtonStyle.blurple)
  async def rock(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
    await self.move(interaction, button)

  @discord.ui.button(label = "Paper", custom_id = "Paper", emoji = "📄", style = discord.ButtonStyle.blurple)
  async def paper(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
    await self.move(interaction, button)

  @discord.ui.button(label = "Scissors", custom_id = "Scissors", emoji = "✂️", style = discord.ButtonStyle.blurple)
  async def scissors(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
    await self.move(interaction, button)

class Fun(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.slash_command(name = "getmeme", description = "Get a meme lol")
  async def slashmeme(inter):
    await inter.response.defer()
    r = popcat.meme()
    e = discord.Embed(url = r['url'], title = f"{r['title']}", color = random.randint(0, 16777215))
    e.set_image(url = f"{r['image']}")
    e.set_footer(text = f"👍: {r['upvotes']} | 🗨️: {r['comments']}")
    await inter.send(embed = e)
    
  #say command slash
  @commands.slash_command(name = "say", description = "Repeats the thing you said")
  async def slashsay(inter, text):
    '''
    Repeats the thing you said
    
    Parameters
    ----------
    text: Text here
    '''
    await inter.response.send_message(f"{text}")
  
  #choose command slash
  @commands.slash_command(name = "choice", description = "Usage: /choice thing 1, thing2, 3 thing")
  async def slashchoice(inter, options):
    '''
    Let the bot choose something for you

    Parameters
    ----------
    options: Example: thing 1, thing2, 3thing
    '''
    e = discord.Embed(title = "Choice:", description = f"I choose.. **{random.choice(options.split(',')).strip()}!**", color = random.randint(0, 16777215))
    await inter.response.send_message(embed = e)    

  #8ball command slash
  @commands.slash_command(name = "8ball", description = "Usage: pb!eightball (text)")
  async def slasheightball(inter, text):
    '''
    Ask 8ball a Y/N question

    Parameters
    ----------
    text: Text here
    '''
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
  @commands.slash_command(name = "random", description = "You can randomize numbers with this command")
  async def slashrandom(inter, num1: int, num2: int):
    '''
    You can randomize numbers with this command

    Parameters
    ----------
    num1: Number 1
    num2: Number 2
    '''
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
  async def slashdice(inter, dices: int = 2, faces: int = 6):
    '''
    Throw dices

    Parameters
    ----------
    dices: Amount of dices
    faces: Amount of faces on each dice
    '''
    if dices >= 1 and faces >= 1:
      dice = random.randint(1, int(faces * dices))
      e = discord.Embed(title = "Dice", description = f"Number: {dice}", color = random.randint(0, 16777215))
      e.set_thumbnail(url = "https://cdn.discordapp.com/attachments/843562496543817781/905114307556163614/dice.png")
      await inter.response.send_message(embed = e)
    else: 
      await inter.response.send_message("Error: Invalid input")

  @commands.slash_command()
  async def minigame(self, inter):
    pass

  #math command
  @minigame.sub_command(name = "math", description = "Math questions, wohooo very fun..")
  async def slashmath(self, inter):
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
  @minigame.sub_command(name = "gtn", description = "The `max` arg is max count. The `tries_amt` arg is max tries. Note: 0 in `tries_amt` = inf tries")
  async def slashguessthenumber(self, inter, max: int = 100, tries_amt: int = 0):
    '''
    Guess the number minigame

    Parameters
    ----------
    max: Maximum count
    tries_amt: Amount of tries you have, 0 = inf
    '''
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
          e = discord.Embed(title = "Timeout", description = f"The right answer was {botnum}", color = random.randint(0, 16777215))
          await inter.send(embed = e)
        except TimeoutError:
          e = discord.Embed(title = "Timeout", description = f"The right answer was {botnum}", color = random.randint(0, 16777215))
          await inter.send(embed = e)
        except ValueError:
          e = discord.Embed(title = "Input error: Try again", color = random.randint(0, 16777215))
          if str(inter.author.id) in db["debug"]:
            e.add_field(name = "Debug", value = f"Variables value:\n{infinity}, {tries_amt}, {botnum}, {tries}")
          await inter.send(embed = e)
      else:
        e = discord.Embed(title = "You left", description = f"The right answer was {botnum}", color = random.randint(0, 16777215))
        await inter.send(embed = e)
        break

  #rps command
  @minigame.sub_command(description = "Play rock paper scissors")
  async def rps(self, inter):
    e = discord.Embed(title = "RPS", description = "Choose a move below!", color = random.randint(0, 16777215))
    await inter.send(embed = e, view = menurps(inter))
  
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
