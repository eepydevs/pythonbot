#cog by Number1#4325
import disnake as discord
from disnake.ext import commands
import random

def uwuize(text):
  emoticons = ["owo", "o~o", "OwO", "O~O", "uwu", "u~u", "UwU", "U~U", "u<u", "u>u", "o<o", "o>o", "O<O", "O>O", "U>U", "U<U", ">w<", ">~<", "<w<", "<~<", "^w^", "^~^", ">~>", ">w>", "@w@", "@~@", "-w-", "-~-", "TwT", "T~T", ".w.", ".~.", "'w'", "'~'" ">:3",":3", "3:", "3:<", ">:>", ":>", ">:<", ":<" "*purr*", "meow!"]
  random.shuffle(emoticons)
  vowels = ("a", "A", "e", "E", "i", "I", "u", "U", "o", "O")
  translation = ""
  chance = random.randint(0, 100)
  if chance >= 25:
    for letter in text:
      if letter.lower() in "r":
        if letter.isupper():
          translation += "W"
        else:
          translation += "w"
      if letter.lower() in "l":
        if letter.isupper():
          translation += "W"
        else:
          translation += "w"
      else: 
        translation += letter
        chance = random.randint(0, 100)
        if chance <= 20:
          if letter in vowels:
            if letter.isupper():
              translation += "W"
            else:
              translation += "w"
        chance = random.randint(0, 100)
        if chance <= 15:
          translation += "~"
    chance = random.randint(0, 100)
    if chance >= 25:
      translation += f" {random.choice(emoticons)}"
    return translation
  else:
    for letter in text:
      translation += letter
      chance = random.randint(0, 100)
      if chance <= 15:
        translation += "~"
    chance = random.randint(0, 100)
    if chance <= 50:
      translation += f" {random.choice(emoticons)}"
    return translation

class Text(commands.Cog):
  def __init__(self, bot):
    self.bot = bot  

  #lowcase command
  @commands.slash_command(name = "lowify", description = "Low case your inputted text!")
  async def slashlowcase(inter, *, text):
    modtext = text.lower()
    await inter.send(modtext)

  #highcase command
  @commands.slash_command(name = "highify", description = "High case your inputted text!")
  async def slashhighcase(inter, *, text):
    modtext = text.upper()
    await inter.send(modtext)

  #spacecase command
  @commands.slash_command(name = "spacify", description = "Space case your inputted text!")
  async def slashspacecase(inter, *, text):
    modtext = " ".join(text)
    await inter.send(modtext)
  
  #titlecase command
  @commands.slash_command(name = "titlize", description = "Title case your inputted text!")
  async def slashtitlecase(inter, *, text):
    modtext = text.title()
    await inter.send(modtext)

  #swapcase command
  @commands.slash_command(name = "swapize", description = "Swap case your inputted text!")
  async def slashswapcase(inter, *, text):
    modtext = text.swapcase()
    await inter.send(modtext)

  #capitaizecase command
  @commands.slash_command(name = "capify", description = "Capitalize your inputted text!")
  async def slashcapitalizecase(inter, *, text):
    modtext = text.capitalize()
    await inter.send(modtext)

  #flip command
  @commands.slash_command(name = "flipify", description = "Flip your inputted text! world!")
  async def slashflipcase(inter, *, text):
    textlist = text.split()
    textlist.reverse()
    textstring = " ".join(textlist)
    await inter.send(textstring)
  
  #reverse command
  @commands.slash_command(name = "reversify", description = "Reverse your inputted text!")
  async def slashreversecase(inter, *, text):
    modtext = text[::-1]
    await inter.send(modtext)

  #mixcase command
  @commands.slash_command(name = "strokify", description = "Mix your inputted text!")
  async def slashmixcase(inter, *, text):
    modtext = " ".join(str().join(random.sample(i, len(i))) for i in text.split())
    await inter.send(modtext)
  
  #uwuize command
  @commands.slash_command(name = "uwuify", description = "UwUize your inputted text!")
  async def uwuize(inter, *, text):
    modtext = uwuize(text)
    await inter.send(modtext)

  #domify command
  @commands.slash_command(name = "domify", description = "Domify your inputted text!")
  async def dot(inter, *, text):
    modtext = text.lower() + "."
    await inter.send(modtext)

  #ifyify command
  @commands.slash_command(name = "ifyify", description = "Ifyify your inputted text!")
  async def ify(inter, *, text):
    modtext = text.split(" ")
    result = []
    for item in modtext:
      result.append(item + "ify")
    await inter.send(" ".join(f"{item}" for item in result))

  #izeize command
  @commands.slash_command(name = "izeize", description = "Izeize your inputted text!")
  async def ize(inter, *, text):
    modtext = text.split(" ")
    result = []
    for item in modtext:
      result.append(item + "ize")
    await inter.send(" ".join(f"{item}" for item in result))

def setup(bot):
  bot.add_cog(Text(bot))