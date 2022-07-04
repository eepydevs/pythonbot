#cog by Number1#4325
import disnake as discord
from disnake.ext import commands
import random

def uwuize(text):
  endings = ["*purrrr...*", "*meooow!*", "*eeeeeeee*", "*quack!*", "*woooof!*"]
  emoticons = ["owo", "o~o", "OwO", "O~O", "uwu", "u~u", "UwU", "U~U", "u<u", "u>u", "o<o", "o>o", "O<O", "O>O", "U>U", "U<U", ">w<", ">~<", "<w<", "<~<", "^w^", "^~^", ">~>", ">w>", "@w@", "@~@", "-w-", "-~-", "TwT", "T~T", ".w.", ".~.", "'w'", "'~'" ">:3",":3", "3:", "3:<", ">:>", ":>", ">:<", ":<", ":V", ":U", ">///<", "O///O", "=///=", "-///-", ">///>", "<///<", ".///.", "^///^"]
  random.shuffle(emoticons)
  random.shuffle(endings)
  vowels = "aAeEiIuUoO"
  y = "dDgGnN"
  translation = ""
  chance = random.randint(0, 100)
  if chance >= 25:
    for letter in text:
      if letter in "rRlL":
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
        if chance <= 30:
          if letter in y:
            if letter.isupper():
              translation += "Y"
            else:
              translation += "y"
        chance = random.randint(0, 100)
        if chance <= 20:
          if letter in vowels:
            if letter.isupper():
              translation += "W"
            else:
              translation += "w"
        chance = random.randint(0, 100)
        if chance <= 15:
          if letter != " ":
            translation += "~"
    chance = random.randint(0, 100)
    if chance <= 20:
      translation += f" {random.choice(endings)}"
    chance = random.randint(0, 100)
    if chance >= 25:
      translation += f" {random.choice(emoticons)}"
  else:
    for letter in text:
      translation += letter
      chance = random.randint(0, 100)
      if chance <= 30:
        if letter in y:
          if letter.isupper():
            translation += "Y"
          else:
            translation += "y"
      chance = random.randint(0, 100)
      if chance <= 15:
        if letter != " ":
          translation += "~"
    chance = random.randint(0, 100)
    if chance <= 20:
      translation += f" {random.choice(endings)}"
    chance = random.randint(0, 100)
    if chance <= 50:
      translation += f" {random.choice(emoticons)}"
  return translation

def indicator(text):
  emojis = {"0": "0️⃣", "1": "1️⃣", "2": "2️⃣", "3": "3️⃣", "4": "4️⃣",
            "5": "5️⃣", "6": "6️⃣", "7": "7️⃣", "8": "8️⃣", "9": "9️⃣",
            "a": "🇦", "b": "🇧", "c": "🇨", "d": "🇩", "e": "🇪", "f": "🇫",
            "g": "🇬", "h": "🇭", "i": "🇮", "j": "🇯", "k": "🇰", "l": "🇱",
            "m": "🇲", "n": "🇳", "o": "🇴", "p": "🇵", "q": "🇶", "r": "🇷",
            "s": "🇸", "t": "🇹", "u": "🇺", "v": "🇻", "w": "🇼", "x": "🇽",
            "y": "🇾", "z": "🇿", "!": "❗", "?": "❓", " ": "⬛", "*": "*️⃣",
            "-": "➖", "+": "➕", "#": "#️⃣", "×": "✖️", "÷": "➗",
            "€": "💶", "£": "💷", "¥": "💴", "$": "💵", "<": "◀️",
            ">": "▶️"}
  result = ""
  for letter in text:
    if letter.lower() in emojis:
      result += f"{emojis[letter.lower()]} "
    else:
      result += f"{letter} "
  return result

def ifyed(text):
  endings = ["ing", "ly", "ed", "y", "ie", "ize", "ify"]
  result = []
  for word in text.split(" "):
    saveword = word
    randomrange = random.randint(3, 10)
    for i in range(randomrange):
      chance = random.randint(0, 100)
      if chance <= 30:
        random.shuffle(endings)
        saveword += random.choice(endings)
    result.append(saveword)
  return " ".join(result)

'''def morsify(text):
  table = {"A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "--.-", "Z": "--..", "/": " ", "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.", "0": "-----"}
  textt = text.upper()
  result = []
  for l in textt.split(" "):
    if l in table:
      result.append(table[l])
    else:
      result.append(" ")
  return str().join(result)'''

class Text(commands.Cog):
  def __init__(self, bot):
    self.bot = bot  

  #lowcase command
  @commands.slash_command(name = "lowify", description = "Low case your inputted text!")
  async def slashlowcase(inter, *, text):
    '''
    Low case your inputted text!

    Parameters
    ----------
    text: Text here
    '''
    modtext = text.lower()
    await inter.send(modtext)

  #highcase command
  @commands.slash_command(name = "highify", description = "High case your inputted text!")
  async def slashhighcase(inter, *, text):
    '''
    High case your inputted text!

    Parameters
    ----------
    text: Text here
    '''
    modtext = text.upper()
    await inter.send(modtext)

  #spacecase command
  @commands.slash_command(name = "spacify", description = "Space case your inputted text!")
  async def slashspacecase(inter, *, text):
    '''
    Space case your inputted text!

    Parameters
    ----------
    text: Text here
    '''
    modtext = " ".join(text)
    await inter.send(modtext)
  
  #titlecase command
  @commands.slash_command(name = "titlize", description = "Title case your inputted text!")
  async def slashtitlecase(inter, *, text):
    '''
    Title case your inputted text!

    Parameters
    ----------
    text: Text here
    '''
    modtext = text.title()
    await inter.send(modtext)

  #swapcase command
  @commands.slash_command(name = "swapize", description = "Swap case your inputted text!")
  async def slashswapcase(inter, *, text):
    '''
    Swap case your inputted text!

    Parameters
    ----------
    text: Text here
    '''
    modtext = text.swapcase()
    await inter.send(modtext)

  #capitaizecase command
  @commands.slash_command(name = "capify", description = "Capitalize your inputted text!")
  async def slashcapitalizecase(inter, *, text):
    '''
    Capitalize your inputted text!

    Parameters
    ----------
    text: Text here
    '''
    modtext = text.capitalize()
    await inter.send(modtext)

  #flip command
  @commands.slash_command(name = "flipify", description = "Flip your inputted text!")
  async def slashflipcase(inter, *, text):
    '''
    Flip your inputted text!

    Parameters
    ----------
    text: Text here
    '''
    textlist = text.split()
    textlist.reverse()
    textstring = " ".join(textlist)
    await inter.send(textstring)
  
  #reverse command
  @commands.slash_command(name = "reversify", description = "Reverse your inputted text!")
  async def slashreversecase(inter, *, text):
    '''
    Reverse your inputted text!

    Parameters
    ----------
    text: Text here
    '''
    modtext = text[::-1]
    await inter.send(modtext)

  #mixcase command
  @commands.slash_command(name = "strokify", description = "Mix your inputted text!")
  async def slashmixcase(inter, *, text):
    '''
    Mix your inputted text!

    Parameters
    ----------
    text: Text here
    '''
    modtext = " ".join(str().join(random.sample(i, len(i))) for i in text.split())
    await inter.send(modtext)
  
  #uwuize command
  @commands.slash_command(name = "fuwwify", description = "UwUize your inputted text!")
  async def uwuize(inter, *, text):
    '''
    UwUize your inputted text!

    Parameters
    ----------
    text: Text here
    '''
    modtext = uwuize(text)
    await inter.send(modtext)

  #domify command
  @commands.slash_command(name = "domify", description = "Domify your inputted text!")
  async def dot(inter, *, text):
    '''
    Domify your inputted text!

    Parameters
    ----------
    text: Text here
    '''
    modtext = text.lower() + "."
    await inter.send(modtext)

  #ifyify command
  @commands.slash_command(name = "ifyify", description = "Ifyify your inputted text!")
  async def ify(inter, *, text):
    '''
    Ifyify your inputted text!

    Parameters
    ----------
    text: Text here
    '''
    modtext = text.split(" ")
    result = []
    for item in modtext:
      result.append(item + "ify")
    await inter.send(" ".join(f"{item}" for item in result))

  #izeize command
  @commands.slash_command(name = "izeize", description = "Izeize your inputted text!")
  async def ize(inter, *, text):
    '''
    Izeize your inputted text!

    Parameters
    ----------
    text: Text here
    '''
    modtext = text.split(" ")
    result = []
    for item in modtext:
      result.append(item + "ize")
    await inter.send(" ".join(f"{item}" for item in result))

  @commands.slash_command()
  async def brickify(self, inter, text):
    '''
    Brickify your inputted text!

    Parameters
    ----------
    text: Text here
    '''
    text = text.lower()
    text.replace('yes', 'yee')
    text.replace('no', 'nope')
    text.replace('hello','hewwo').replace('hi', 'hii')
    text.replace("'",'')
    text = f"{random.choice(['hmm', 'heh', 'lol', 'uhm', 'yeah'])} {text} {random.choice([':V', 'u<u', 'o<o', ':)', '🍞', '~'])}"
    await inter.send(text)

  @commands.slash_command()
  async def shoutify(self, inter, text):
    '''
    SHhOuttIfY yyOuR inPUtTedd TeXXt!!!

    Parameters
    ----------
    text: TeXXt hEre?!
    '''
    text = ''.join(random.choice([c.upper(), c.lower()])*int(random.random()*1.3+1) for c in text)
    text += random.choice(['!!!', '?!'])
    await inter.send(text)

  @commands.slash_command()
  async def spoilerize(self, inter, text):
    '''
    Spoiler your inputted text

    Parameters
    ----------
    text: Text here
    '''
    await inter.send(''.join(f'||{c}||' for c in text))

  @commands.slash_command(name = "sortify", description = "Sort your inputted text!")
  async def sort(inter, *, text):
    '''
    Sort your inputted text!

    Parameters
    ----------
    text: Text here
    '''
    modtext = sorted(text.split(" "), )
    await inter.send(" ".join(modtext))

  @commands.slash_command(name = "qmaify")
  async def qma(inter, *, text):
    '''
    Qmaify your inputted text!

    Parameters
    ----------
    text: Text here
    '''
    await inter.send(f"- {text}")

  @commands.slash_command(name = "remixuerify")
  async def remixuer(inter, *, text):
    '''
    Remixuerify your inputted text!

    Parameters
    ----------
    text: Text here
    '''
    catemoji = ["😺", "😸", "😹", "😻", "😼", "😽", "🙀", "😿", "😾"]
    random.shuffle(catemoji)
    await inter.send(f"{random.choice(catemoji)} {text}")

  @commands.slash_command(name = "indicatorify")
  async def indicatorify(inter, *, text):
    '''
    Indicatorify your inputted text!

    Parameters
    ----------
    text: Text here
    '''
    modtext = indicator(text)
    await inter.send(modtext)

  @commands.slash_command(name = "ifyinglyedy")
  async def ifyending(inter, *, text):
    '''
    Ifyinglyedy your inputted text!

    Parameters
    ----------
    text: Text here
    '''
    modtext = ifyed(text)
    await inter.send(modtext)

  """@commands.slash_command()
  async def morse(inter, *, text):
    '''
    Morsify your inputted text
    
    Parameters
    ----------
    text: Text here
    '''
    if all([True if i in ".-/ " else False for i in text]):
      await inter.send(morsify(text))
    else:
      await inter.send("none")"""
    
def setup(bot):
  bot.add_cog(Text(bot))