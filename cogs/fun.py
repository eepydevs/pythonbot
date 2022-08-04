#cog by Number1#4325
import disnake as discord
from disnake.ext import commands
import requests
import random
import asyncio
import os
from replit import db

responselist = ["Yes.", "It is certain.", "It is decidedly so.", "Without a doubt.", "Yes definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Signs point to yes.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good...", "Very doubtful.", "Maybe...", "No.", "Possibly..", "Concentrate and ask again.", "Cannot predict now.", "Ask again later."]
random.shuffle(responselist)

if "queue" not in db:
  db["queue"] = []

class menurps(discord.ui.Select):
  def __init__(self, inter: discord.Interaction):
    self.inter = inter
    options = [
      discord.SelectOption(label = "Rock", emoji = "🪨", value = "Rock"),
      discord.SelectOption(label = "Paper", emoji = "📄", value = "Paper"),
      discord.SelectOption(label = "Scissors", emoji = "✂️", value = "Scissors")
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
    
  async def callback(self, inter: discord.MessageInteraction):
    moves = ("Rock", "Paper", "Scissors")
    p1 = moves.index(self.values[0].capitalize())
    p2 = random.randrange(0, len(moves))

    if p1 - p2 in (-2, 1):
      e = discord.Embed(title = f"{inter.author.name} won!", description = "Congratulations!", color = random.randint(0, 16777215))
      e.set_footer(text = f"{inter.author.name}: {moves[p1]} | Python bot: {moves[p2]}")
      await inter.response.edit_message(embed = e, view = None)
      return
    elif p1 - p2 in (-1, 2):
      e = discord.Embed(title = f"{inter.author.name} lost!", description = "Be lucky next time!", color = random.randint(0, 16777215))
      e.set_footer(text = f"{inter.author.name}: {moves[p1]} | Python bot: {moves[p2]}")
      await inter.response.edit_message(embed = e, view = None)
      return
    else:
      e = discord.Embed(title = "Tie!", description = "Quite lucky", color = random.randint(0, 16777215))
      e.set_footer(text = f"{inter.author.name}: {moves[p1]} | Python bot: {moves[p2]}")
      await inter.response.edit_message(embed = e, view = None)
      return

class rpsView(discord.ui.View):
  def __init__(self, inter: discord.Interaction):
      super().__init__(timeout = 30)
      self.add_item(menurps(inter))

class Fun(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
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

  @commands.slash_command()
  async def call(self, inter):
    pass
    
  @call.sub_command()
  async def userphone(self, inter):
    '''
    Call someone with the phone!
    '''
    if str(inter.channel.id) in db["linkchannels"]:
      await inter.send("Error: This channel is linked with other channel")
      return
    if str(inter.channel.id) in db["queue"]:
      await inter.send("Error: This channel is already calling someone")
      return
    
    tries, maxtries = 0, 25
    await inter.response.defer()
    db["queue"].append(str(inter.channel.id))
    while True:
      queue = list(db["queue"]).copy()
      if len(queue) > 1:
          id = queue.pop(random.randint(1, len(queue)) - 1)
        #try:
          if id != inter.channel.id:
            db["queue"].pop(db["queue"].index(str(id)))  
            if str(inter.channel.id) not in db["linkchannels"]:
              db["linkchannels"][str(inter.channel.id)] = []
            if str(id) not in db["linkchannels"]:
              db["linkchannels"][str(id)] = []
        
            if str(inter.channel.id) not in db["linkchannels"][str(id)] and str(id) not in db["linkchannels"][str(inter.channel.id)]:
              db["linkchannels"][str(id)].append(str(inter.channel.id))
              db["linkchannels"][str(inter.channel.id)].append(str(id))
            if str(inter.channel.id) in db["queue"]:
              db["queue"].pop(db["queue"].index(str(inter.channel.id)))
            msg = "Success! Connection has been made, say hi!"
            break
        #except: 
        #  msg = "Something went wrong"
        #  break
      if str(inter.channel.id) in db["linkchannels"]:
        msg = "Success! Connection has been made, say hi!"
        break
      tries += 1
      if tries == maxtries:
        db["queue"].pop(db["queue"].index(str(inter.channel.id)))
        msg = "Error: Reached max tries (25)"
        break
      await asyncio.sleep(1)
      continue
    await inter.edit_original_message(msg)

  @call.sub_command()
  async def hangup(self, inter):
    '''
    Stop the call
    '''
    if str(inter.channel.id) not in db["linkchannels"] or len(db["linkchannels"][str(inter.channel.id)]) > 1:
      await inter.send("Error: There is no call in this channel")
      return
    id = db["linkchannels"][str(inter.channel.id)][0]
    id2 = db["linkchannels"][str(inter.channel.id)]
    id1 = db["linkchannels"][id]
    if str(inter.channel.id) in id1:
      if len(id1) == 1:
        del db["linkchannels"][str(inter.channel.id)]
      else:
        del db["linkchannels"][str(inter.channel.id)][db["linkchannels"][str(inter.channel.id)].index(id)]
      await inter.bot.get_channel(int(id)).send("The other party hang up the call")
    if id in id2:
      if len(id2) == 1:
        del db["linkchannels"][id]
      else:
        del db["linkchannels"][id][db["linkchannels"][id].index(str(inter.channel.id))]
    await inter.send("Hang up the call")
    
    
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
    Let the bot to choose something for you

    Parameters
    ----------
    options: Example: thing 1, thing2, 3thing
    '''
    e = discord.Embed(title = "Choice:", description = f"I choose.. {random.choice(options.split(', '))}", color = random.randint(0, 16777215))
    await inter.response.send_message(embed = e)    

  #8ball command slash
  @commands.slash_command(name = "8ball",description = "Usage: pb!eightball (text)")
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
  @commands.slash_command(description = "Play rock paper scissors")
  async def rps(self, inter):
    e = discord.Embed(title = "RPS", description = "Choose a move below!", color = random.randint(0, 16777215))
    await inter.send(embed = e, view = rpsView(inter))
  
    """
    Rock & Paper: Lose -1
    Rock & Scissors: Win -2
    Paper & Rock: Win 1
    Paper & Scissors: Lose -1
    Scissors & Rock: Lose 2
    Scissors & Paper: Win 1
    """

  #repleach command
  @commands.slash_command()
  async def repleach(inter, text: str, rwhat: str, rwith: str):
    '''
    Replace each RWHAT with RWITH (no regex here)
    
    Parameters
    ----------
    text: Text you want to use
    rwhat: What to replace
    rwith: Replace with what
    '''
    await inter.send(text.replace(rwhat, rwith))
    
def setup(bot):
  bot.add_cog(Fun(bot))
