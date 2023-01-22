#cog by maxy#2866
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

def morsifyen(text):
  table = {"A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--", "Z": "--..", "/": "-..-.", "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.", "0": "-----", ",": "--..--", ".": ".-.-.-", "?": "..--..", "!": "-.-.--", " ": "/"}
  textt = text.upper()
  result = []
  for l in textt:
    if l in table:
      result.append(f"{table[l]} ")
  return str().join(result)

def morsifyde(text):
  table = {".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E", "..-.": "F", "--.": "G", "....": "H", "..": "I", ".---": "J", "-.-": "K", ".-..": "L", "--": "M", "-.": "N", "---": "O", ".--.": "P", "--.-": "Q", ".-.": "R", "...": "S", "-": "T", "..-": "U", "...-": "V", ".--": "W", "-..-": "X", "-.--": "Y", "--..": "Z", "-..-.": "/", ".----": "1", "..---": "2", "...--": "3", "....-": "4", ".....": "5", "-....": "6", "--...": "7", "---..": "8", "----.": "9", "-----": "0", "--..--": ",", ".-.-.-": "." ,"..--..": "?", "-.-.--": "!", "/": " "}
  textt = text.replace("_", "-")
  result = []
  if all([True if i in ".-/ " else False for i in textt]):
    for l in textt.split(" "):
      if l in table:
        result.append(table[l])
    return str().join(result)
  else:
    return "none"

def braillede(text):
  table = {"⠟": "Q", "⠺": "W", "⠑": "E", "⠗": "R", "⠞": "T", "⠽": "Y", "⠥": "U", "⠊": "I", "⠕": "O", "⠏": "P", "⠁": "A", "⠎": "S", "⠙": "D", "⠋": "F", "⠛": "G", "⠓": "H", "⠚": "J", "⠅": "K", "⠇": "L", "⠵": "Z", "⠭": "X", "⠉": "C", "⠧": "V", "⠃": "B", "⠝": "N", "⠍": "M", "⠖": "!", "⠢": "?", "⠲": ".", "⠂": ",", " ": " "}
  result = []
  for l in text:
    if l in table:
      result.append(table[l])
  if result:
    return str().join(result)
  else: return "none"

def brailleen(text):
  table = {"Q": "⠟", "W": "⠺", "E": "⠑", "R": "⠗", "T": "⠞", "Y": "⠽", "U": "⠥", "I": "⠊", "O": "⠕", "P": "⠏", "A": "⠁", "S": "⠎", "D": "⠙", "F": "⠋", "G": "⠛", "H": "⠓", "J": "⠚", "K": "⠅", "L": "⠇", "Z": "⠵", "X": "⠭", "C": "⠉", "V": "⠧", "B": "⠃", "N": "⠝", "M": "⠍", "!": "⠖", "?": "⠢", ".": "⠲", ",": "⠂", " ": " "}  
  textt = text.upper()
  result = []
  for l in textt:
    if l in table:
      result.append(table[l])
  if result:
    if str().join(result):
      return str().join(result)
    else: return "none"
  else: return "none"

def binde(text):
  table = {"00110001": "1", "00110010": "2", "00110011": "3", "00110100": "4", "00110101": "5", "00110110": "6", "00110111": "7", "00111000": "8", "00111001": "9", "00110000": "0", "01010001": "Q", "01010111": "W", "01000101": "E", "01010010": "R", "01010100": "T", "01011001": "Y", "01010101": "U", "01001001": "I", "01001111": "O", "01010000": "P", "01000001": "A", "01010011": "S", "01000100": "D", "01000110": "F", "01000111": "G", "01001000": "H", "01001010": "J", "01001011": "K", "01001100": "L", "01011010": "Z", "01011000": "X", "01000011": "C", "01010110": "V", "01000010": "B", "01001110": "N", "01001101": "M", "00111111": "?", "00100001": "!", "00101100": ",", "00101110": ".", "00100000": " "}
  result = []
  for l in text.split(" "):
    if l in table:
      result.append(table[l])
  if result:
    return str().join(result)
  else: return "none"

def binen(text):
  table = {"1": "00110001", "2": "00110010", "3": "00110011", "4": "00110100", "5": "00110101", "6": "00110110", "7": "00110111", "8": "00111000", "9": "00111001", "0": "00110000", "Q": "01010001", "W": "01010111", "E": "01000101", "R": "01010010", "T": "01010100", "Y": "01011001", "U": "01010101", "I": "01001001", "O": "01001111", "P": "01010000", "A": "01000001", "S": "01010011", "D": "01000100", "F": "01000110", "G": "01000111", "H": "01001000", "J": "01001010", "K": "01001011", "L": "01001100", "Z": "01011010", "X": "01011000", "C": "01000011", "V": "01010110", "B": "01000010", "N": "01001110", "M": "01001101", "?": "00111111", "!": "00100001", ",": "00101100", ".": "00101110", " ": "00100000"}
  textt = text.upper()
  result = []
  for l in textt:
    if l in table:
      result.append(table[l])
  if result:
    if str().join(result):
      return " ".join(result)
    else: return "none"
  else: return "none"

class Text(commands.Cog):
  def __init__(self, bot):
    self.bot = bot  

  @commands.slash_command()
  async def text(self, inter):
    pass
  
  @text.sub_command_group(name = "decode", description = "Decode encoded text")
  async def decode(self, inter):
    pass

  @decode.sub_command
  async def braille(self, inter, text):
    '''
    Braille decode your inputted text
    
    Parameters
    ----------
    text: Text here
    '''
    await inter.response.defer()
    await inter.send(braillede(text))

  @decode.sub_command()
  async def binary(self, inter, text):
    '''
    Binary decode your inputted text
    
    Parameters
    ----------
    text: Text here
    '''
    await inter.response.defer()
    await inter.send(binde(text))


  @decode.sub_command()
  async def morse(self, inter, text):
    '''
    Morse decode your inputted text
    
    Parameters
    ----------
    text: Text here
    '''
    await inter.response.defer()
    await inter.send(morsifyde(text))

  @text.sub_command_group(name = "encode", description = "Encode text")
  async def encode(self, inter):
    pass

  @encode.sub_command()
  async def braille(self, inter, text):
    '''
    Braille encode your inputted text
    
    Parameters
    ----------
    text: Text here
    '''
    await inter.response.defer()
    await inter.send(brailleen(text))

  @encode.sub_command()
  async def binary(self, inter, text):
    '''
    Binary encode your inputted text
    
    Parameters
    ----------
    text: Text here
    '''
    await inter.response.defer()
    await inter.send(binen(text))

  @encode.sub_command()
  async def morse(self, inter, text):
    '''
    Morse encode your inputted text
    
    Parameters
    ----------
    text: Text here
    '''
    await inter.response.defer()
    await inter.send(morsifyen(text))

  #flip command
  @text.sub_command(name = "flipify", description = "Flip your inputted text!")
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
  @text.sub_command(name = "reversify", description = "Reverse your inputted text!")
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
  @text.sub_command(name = "strokify", description = "Mix your inputted text!")
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
  @text.sub_command(name = "fuwwify", description = "UwUize your inputted text!")
  async def uwuize(inter, *, text):
    '''
    UwUize your inputted text!

    Parameters
    ----------
    text: Text here
    '''
    modtext = uwuize(text)
    await inter.send(modtext)

  #ifyify command
  @text.sub_command(name = "ifyify", description = "Ifyify your inputted text!")
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
  @text.sub_command(name = "izeize", description = "Izeize your inputted text!")
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

  @text.sub_command()
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

  @text.sub_command()
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

  @text.sub_command()
  async def spoilerize(self, inter, text):
    '''
    Spoiler your inputted text

    Parameters
    ----------
    text: Text here
    '''
    await inter.send(''.join(f'||{c}||' for c in text))

  @text.sub_command(name = "sortify", description = "Sort your inputted text!")
  async def sort(inter, *, text):
    '''
    Sort your inputted text!

    Parameters
    ----------
    text: Text here
    '''
    modtext = sorted(text.split(" "), )
    await inter.send(" ".join(modtext))
    

  @text.sub_command(name = "indicatorify")
  async def indicatorify(inter, *, text):
    '''
    Indicatorify your inputted text!

    Parameters
    ----------
    text: Text here
    '''
    modtext = indicator(text)
    await inter.send(modtext)

  @text.sub_command(name = "ifyinglyedy")
  async def ifyending(inter, *, text):
    '''
    Ifyinglyedy your inputted text!

    Parameters
    ----------
    text: Text here
    '''
    modtext = ifyed(text)
    await inter.send(modtext)
    
  #repleach command
  @text.sub_command()
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
  bot.add_cog(Text(bot))