from typing import Union
import datetime, time
import disnake as discord
import requests as rq
from disnake.ext import commands
from typing import Dict, Any
import redis as rd
import json
import os
import atexit
import random
import asyncio
from dotenv import load_dotenv
load_dotenv()

callsInProgress = {}

class PopcatAPI():
  """Used to communicate with Popcat API"""
  def __init__(self):
    self.BASE_URL = "https://api.popcat.xyz/"

  @staticmethod
  def __convert_iso8601(timestamp: str) -> int:
    """Converts ISO 8601 to UNIX

    Args:
        timestamp (str): ISO 8601 timestamp

    Returns:
        int: UNIX timestamp
    """
    return str(time.mktime(time.strptime(timestamp.replace('T', ' ')[:timestamp.find('.')], '%Y-%m-%d %H:%M:%S')))[:-2]

  def welcome_card(self, top_text: str, middle_text: str, bottom_text: str, avatar_url: str, background_url: str = "https://cdn.discordapp.com/attachments/850808002545319957/859359637106065408/bg.png"):
    """Custom discord welcome card

    Args:
        top_text (str): Members username
        middle_text (str): Custom text
        bottom_text (str): Amount of members
        avatar_url (str): Avatar URL
        background_url (str, optional): Background URL. Defaults to "https://cdn.discordapp.com/attachments/850808002545319957/859359637106065408/bg.png".

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}welcomecard", params = {"background": background_url, "text1": top_text, "text2": middle_text, "text3": bottom_text, "avatar": avatar_url}).url

  def color(self, color_hex: str) -> dict:
    """Check info for a color

    Args:
        color_hex (str): Color HEX

    Returns:
        dict: All the info
    """
    return rq.get(f"{self.BASE_URL}color/{color_hex.replace('#', '')[0:6]}").json()

  def lyrics(self, song_name: str) -> dict:
    """See lyrics of a song

    Args:
        song_name (str): Song name

    Returns:
        dict: All the info
    """
    return rq.get(f"{self.BASE_URL}lyrics", params = {"song": song_name[0:119]}).json()

  def periodic_table(self, element: str) -> dict:
    """Lets you see info about an element in periodic table

    Args:
        element (str): Element name

    Returns:
        dict: All the info
    """
    return rq.get(f"{self.BASE_URL}periodic-table", params = {"element": element[0:119]}).json()

  def pickup_lines(self) -> str:
    """Gives you pickup lines

    Returns:
        str: Pickup line
    """
    return rq.get(f"{self.BASE_URL}pickuplines").json()["pickupline"]

  def imdb(self, query: str) -> dict:
    """Check for info of a movie

    Args:
        query (str): Movie name

    Returns:
        dict: All the info
    """
    r = rq.get(f"{self.BASE_URL}imdb", params = {"q": query}).json()
    vratings = []
    for i in r["ratings"]:
      vstr = ": ".join(v for v in i.values())
      vratings.append(vstr)
    r["ratings"] = vratings
    r["released"] = self.__convert_iso8601(r["released"])
    r["dvd"] = self.__convert_iso8601(r["dvd"])
    return r

  def jail(self, image_url: str = "https://cdn.popcat.xyz/popcat.png") -> str:
    """Jail someone

    Args:
        image_url (str, optional): Image url. Defaults to "https://cdn.popcat.xyz/popcat.png".

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}jail", params = {"image": image_url}).url

  def unforgivable(self, text: str = "Popcat api so trash") -> str:
    """God unforgives you

    Args:
        text (str, optional): Text. Defaults to "Popcat api so trash".

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}unforgivable", params = {"text": text}).url

  def screenshot(self, url: str = "https://google.com") -> str:
    """Screenshot a website

    Args:
        url (str, optional): . Defaults to "https://google.com".

    Returns:
        str: _description_
    """
    return rq.get(f"{self.BASE_URL}screenshot", params = {"url": url if url.startswith(("https://", "http://")) else (("https://" + url[url.find("//") + 2:]) if "//" in url else "https://" + url)}).url

  def random_color(self) -> dict:
    """Get a random color

    Returns:
        dict: Color info
    """
    return self.color(color_hex = rq.get(f"{self.BASE_URL}randomcolor").json()["hex"])

  def steam(self, query: str) -> dict:
    """Get steam games info

    Args:
        query (str): Game name

    Returns:
        dict: All the info
    """
    return rq.get(f"{self.BASE_URL}steam", params = {"q": query}).json()

  def sad_cat(self, text: str = "people hating me for being innocent") -> str:
    """Sad cat looking at candle

    Args:
        text (str, optional): Text on the candle. Defaults to "people hating me for being innocent".

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}sadcat", params = {"text": text}).url

  #def oogway_quote
  #does not work right now

  def communism(self, image_url: str = "https://cdn.popcat.xyz/popcat.png") -> str:
    """Makes the image communist

    Args:
        image_url (str, optional): Image URL. Defaults to "https://cdn.popcat.xyz/popcat.png".

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}communism", params = {"image": image_url}).url

  def car_pictures(self) -> dict:
    """Get random car pictures

    Returns:
        dict: Image URL and author
    """
    return rq.get(f"{self.BASE_URL}car").json()

  def chat_bot(self, msg: str, owner: str, botname: str) -> str:
    """Custom chatbot

    Args:
        msg (str): Message
        owner (str): Bot owner
        botname (str): Bot name

    Returns:
        str: Response
    """
    return rq.get(f"{self.BASE_URL}chatbot", params = {"msg": msg, "owner": owner, "botname": botname}).json()["response"]

  def pooh(self, top_text: str, bottom_text: str) -> str:
    """Pooh as normal and with a tuxedo

    Args:
        top_text (str): Top text
        bottom_text (str): Bottom text

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}pooh", params = {"text1": top_text, "text2": bottom_text}).url

  def shower_thoughts(self) -> str:
    """Shower thoughts

    Returns:
        str: A shower thought
    """
    r = rq.get(f"{self.BASE_URL}showerthoughts").json()
    return f"{r['result']}\n> {r['author']}"

  def quote(self) -> str:
    """Get random quotes

    Returns:
        str: Quote
    """
    return rq.get(f"{self.BASE_URL}quote").json()["quote"]

  def wanted(self, image_url: str = "https://cdn.popcat.xyz/popcat.png") -> str:
    """Be wanted by your whole discord server

    Args:
        image_url (str, optional): Image URL. Defaults to "https://cdn.popcat.xyz/popcat.png".

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}wanted", params = {"image": image_url}).url

  def subreddit(self, query: str) -> dict:
    """Get subreddit info

    Args:
        query (str): Subreddit

    Returns:
        dict: All the info
    """
    return rq.get(f"{self.BASE_URL}subreddit/{query}").json()

  def github(self, query: str) -> dict:
    """Get github info

    Args:
        query (str): Username

    Returns:
        dict: All the info
    """
    r = rq.get(f"{self.BASE_URL}github/{query}").json()
    r["created_at"] = self.__convert_iso8601(r["created_at"])
    r["updated_at"] = self.__convert_iso8601(r["updated_at"])
    return r

  def weather(self, query: str) -> dict:
    """See your city's weather

    Args:
        query (str): City name

    Returns:
        dict: Weather info
    """
    return rq.get(f"{self.BASE_URL}weather", params = {"q": query}).json()

  def who_would_win(self, image1_url: str = "https://cdn.iconscout.com/icon/free/png-512/javascript-2752148-2284965.png", image2_url: str = "https://cdn3.iconfinder.com/data/icons/logos-and-brands-adobe/512/267_Python-512.png") -> str:
    """Who would win?

    Args:
        image1_url (str, optional): Image URL. Defaults to "https://cdn.iconscout.com/icon/free/png-512/javascript-2752148-2284965.png".
        image2_url (str, optional): Image URL. Defaults to "https://cdn3.iconfinder.com/data/icons/logos-and-brands-adobe/512/267_Python-512.png".

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}whowouldwin", params = {"image1": image1_url, "image2": image2_url}).url

  def gun(self, image_url: str = "https://cdn.popcat.xyz/popcat.png") -> str:
    """Make a fitting image with you holding a gun

    Args:
        image_url (str, optional): Image URL. Defaults to "https://cdn.popcat.xyz/popcat.png".

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}gun", params = {"image": image_url}).url

  def lulcat(self, text: str) -> str:
    """Make your text into lulcat

    Args:
        text (str): Text

    Returns:
        str: Result text
    """
    return rq.get(f"{self.BASE_URL}lulcat", params = {"text": text}).json()["text"]

  #def opinion
  #doesn't work for now

  def drake(self, top_text: str, bottom_text: str) -> str:
    """Drake

    Args:
        top_text (str): Top text
        bottom_text (str): Bottom text

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}drake", params = {"text1": top_text, "text2": bottom_text}).url

  #def instagram
  #doesn't work for now

  def npm(self, query: str) -> dict:
    """Get npm package info

    Args:
        query (str): Package name

    Returns:
        dict: All the info
    """
    return rq.get(f"{self.BASE_URL}npm", params = {"q": query}).json()

  def fact(self) -> str:
    """Get a random fact

    Returns:
        str: Fact
    """
    return rq.get(f"{self.BASE_URL}fact").json()["fact"]

  def ship(self, image1_url: str = "https://cdn.popcat.xyz/popcat.png", image2_url: str = "https://cdn3.iconfinder.com/data/icons/logos-and-brands-adobe/512/267_Python-512.png") -> str:
    """Ship yourself with your loved one

    Args:
        image1_url (str, optional): Left image. Defaults to "https://cdn.popcat.xyz/popcat.png".
        image2_url (str, optional): Right image. Defaults to "https://cdn3.iconfinder.com/data/icons/logos-and-brands-adobe/512/267_Python-512.png".

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}ship", params = {"user1": image1_url, "user2": image2_url}).url

  def joke(self) -> str:
    """Get a random joke

    Returns:
        str: Joke
    """
    return rq.get(f"{self.BASE_URL}joke").json()["joke"]

  def biden_tweet(self, text: str = "Popcat API sucks!!") -> str:
    """Biden tweets your text

    Args:
        text (str, optional): The text biden gonna tweet. Defaults to "Popcat API sucks!!".

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}biden", params = {"text": text}).url

  def pikachu(self, text: str = "Hello :O") -> str:
    """Surprised Pikachu!

    Args:
        text (str, optional): Text. Defaults to "Hello :O".

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}pikachu", params = {"text": text}).url

  def mock(self, text: str) -> str:
    """Manipulate your text in sarcastic tone

    Args:
        text (str): Text

    Returns:
        str: Result text
    """
    return rq.get(f"{self.BASE_URL}mock", params = {"text": text}).json()["text"]

  def would_you_rather(self) -> dict:
    """Would you rather

    Returns:
        dict: 2 Choices
    """
    return rq.get(f"{self.BASE_URL}wyr").json()

  def meme(self) -> dict:
    """Get a meme for yourself

    Returns:
        dict: Meme info
    """
    return rq.get(f"{self.BASE_URL}meme").json()

  def colorify(self, image_url: str = "https://cdn.popcat.xyz/popcat.png", color: str = None):
    """Overlay a color over your image

    Args:
        image_url (str, optional): Image URL. Defaults to "https://cdn.popcat.xyz/popcat.png".
        color (str, optional): Color HEX. Defaults to Random.

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}colorify", params = {"image": image_url, "color": color if color else self.random_color()["hex"][1:]}).url

  def drip(self, image_url: str = "https://cdn.popcat.xyz/popcat.png") -> str:
    """Have a drip on yourself

    Args:
        image_url (str, optional): Image URL. Defaults to "https://cdn.popcat.xyz/popcat.png".

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}drip", params = {"image": image_url}).url

  def clown(self, image_url: str = "https://cdn.popcat.xyz/popcat.png") -> str:
    """Be a clown

    Args:
        image_url (str, optional): Image URL. Defaults to "https://cdn.popcat.xyz/popcat.png".

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}clown", params = {"image": image_url}).url

  def translate(self, translate_to: str, text: str):
    """Translate text to alot of languages

    Args:
        translate_to (str): Translate to
        text (str): Text to translate

    Returns:
        str: Translated text
    """
    return rq.get(f"{self.BASE_URL}translate", params = {"to": translate_to, "text": text}).json()["translated"]

  def encode(self, text: str):
    """Encode text to binary

    Args:
        text (str): Text to encode

    Returns:
        str: Binary
    """
    return rq.get(f"{self.BASE_URL}encode", params = {"text": text}).json()["binary"]

  def decode(self, binary: str):
    """Decode binary to normal text

    Args:
        binary (str): Binart

    Returns:
        str: Normal text
    """
    return rq.get(f"{self.BASE_URL}decode", params = {"binary": binary}).json()["text"]

  def uncover(self, image_url: str = "https://cdn.popcat.xyz/popcat.png") -> str:
    """Be in someones wall

    Args:
        image_url (str, optional): Image URL. Defaults to "https://cdn.popcat.xyz/popcat.png".

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}uncover", params = {"image": image_url}).url

  def ad(self, image_url: str = "https://cdn.popcat.xyz/popcat.png") -> str:
    """Advertise yourself

    Args:
        image_url (str, optional): Image URL. Defaults to "https://cdn.popcat.xyz/popcat.png".

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}ad", params = {"image": image_url}).url

  def blur(self, image_url: str = "https://cdn.popcat.xyz/popcat.png") -> str:
    """Blur yourself

    Args:
        image_url (str, optional): Image URL. Defaults to "https://cdn.popcat.xyz/popcat.png".

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}blur", params = {"image": image_url}).url

  def invert(self, image_url: str = "https://cdn.popcat.xyz/popcat.png") -> str:
    """Invert colors of yourself

    Args:
        image_url (str, optional): Image URL. Defaults to "https://cdn.popcat.xyz/popcat.png".

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}invert", params = {"image": image_url}).url

  def grayscale(self, image_url: str = "https://cdn.popcat.xyz/popcat.png") -> str:
    """Become white-black

    Args:
        image_url (str, optional): Image URL. Defaults to "https://cdn.popcat.xyz/popcat.png".

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}grayscale", params = {"image": image_url}).url

  def eight_ball(self) -> str:
    """Ask 8ball some questions

    Returns:
        str: Response
    """
    return rq.get(f"{self.BASE_URL}8ball").json()["answer"]

  #def playstore
  #endpoint in maintenance

  def itunes(self, query: str) -> dict:
    """Search music in iTunes

    Args:
        query (str): Music name

    Returns:
        dict: All the info
    """
    return rq.get(f"{self.BASE_URL}itunes", params = {"q": query}).json()

  def reverse(self, text: str) -> str:
    """Reverse your text

    Args:
        text (str): Text

    Returns:
        str: Reversed text
    """
    return rq.get(f"{self.BASE_URL}reverse", params = {"text": text}).json()["text"]

  def joke_overhead(self, image_url: str = "https://cdn.popcat.xyz/popcat.png") -> str:
    """You misheard the joke

    Args:
        image_url (str, optional): Image URL. Defaults to "https://cdn.popcat.xyz/popcat.png".

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}jokeoverhead", params = {"image": image_url}).url

  def double_struck(self, text: str) -> str:
    """Make your text a bit fancier

    Args:
        text (str): Text

    Returns:
        str: Fancy text
    """
    return rq.get(f"{self.BASE_URL}doublestruck", params = {"text": text}).json()["text"]

  def mnm(self, image_url: str = "https://cdn.popcat.xyz/popcat.png") -> str:
    """Become an M&M

    Args:
        image_url (str, optional): Image URL. Defaults to "https://cdn.popcat.xyz/popcat.png".

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}mnm", params = {"image": image_url}).url

  def pet(self, image_url: str = "https://cdn.popcat.xyz/popcat.png") -> str:
    """Pet someone of your friends

    Args:
        image_url (str, optional): Image URL. Defaults to "https://cdn.popcat.xyz/popcat.png".

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}pet", params = {"image": image_url}).url

  def text_to_morse(self, text: str) -> str:
    """Encode your text to morse

    Args:
        text (str): Text

    Returns:
        str: Morse text
    """
    return rq.get(f"{self.BASE_URL}texttomorse", params = {"text": text}).json()["morse"]

  def caution(self, text: str = "Sample Text") -> str:
    """Caution with your text

    Args:
        text (str, optional): Text. Defaults to "Sample Text".

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}caution", params = {"text": text}).url

  def alert(self, text: str = "Sample Text") -> str:
    """iPhone Alert with your text

    Args:
        text (str, optional): Text. Defaults to "Sample Text".

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}alert", params = {"text": text}).url

  def facts(self, text: str = "Sample Text") -> str:
    """Book of facts with your text

    Args:
        text (str, optional): Text. Defaults to "Sample Text".

    Returns:
        str: Finished image URL
    """
    return rq.get(f"{self.BASE_URL}facts", params = {"text": text}).url

class CallChannel:
  def __init__(self, interaction: discord.Interaction, channel_id: int = None):
    self.cid = channel_id if (interaction.bot.get_channel(channel_id) if not channel_id else True) else interaction.channel.id

  def link(self, id: str):
    global callsInProgress
    id = str(id)
    if str(self.cid) not in callsInProgress:
      callsInProgress[str(self.cid)] = []
    if id not in callsInProgress:
      callsInProgress[id] = []

    if str(self.cid) not in callsInProgress[id] and id not in callsInProgress[str(self.cid)]:
      callsInProgress[id] = [str(self.cid)]
      callsInProgress[str(self.cid)] = [id]
      return discord.Embed(title="Success", description=f"Linked `{id}` and this channel", color=random.randint(0, 16777215)), True
    else:
      return discord.Embed(title="Error", description="This channel is already linked with another channel", color=random.randint(0, 16777215)), False

  def unlink(self, id: str):
    global callsInProgress
    id = str(id)
    if id not in callsInProgress[str(self.cid)] or str(self.cid) not in callsInProgress[id]:
      return discord.Embed(title="Error", description="Invalid channel id", color=random.randint(0, 16777215)), False
    e = discord.Embed(title="Successfully deleted", color=random.randint(0, 16777215))
    id2 = callsInProgress[str(self.cid)]
    id1 = callsInProgress[id]
    if str(self.cid) in id1:
      if len(id1) == 1:
        del callsInProgress[str(self.cid)]
      else:
        del callsInProgress[str(self.cid)][callsInProgress[str(self.cid)].index(id)]
      e.add_field(name=f"{id} > {self.cid}", value="_ _", inline=False)
    if id in id2:
      if len(id2) == 1:
        del callsInProgress[id]
      else:
        del callsInProgress[id][callsInProgress[id].index(str(self.cid))]
      e.add_field(name=f"{self.cid} > {id}", value="_ _", inline=False)
    return e, True

class LinkChannel:
  def __init__(self, interaction: discord.Interaction, channel_id: int = None):
    self.cid = channel_id if (interaction.bot.get_channel(channel_id) if not channel_id else True) else interaction.channel.id

  def link(self, id: str):
    global db
    if str(self.cid) not in db["linkchannels"]:
      db["linkchannels"][str(self.cid)] = []
    if id not in db["linkchannels"]:
      db["linkchannels"][id] = []

    if str(self.cid) not in db["linkchannels"][id] and id not in db["linkchannels"][str(self.cid)]:
      db["linkchannels"][id].append(str(self.cid))
      db["linkchannels"][str(self.cid)].append(id)
      return discord.Embed(title="Success", description=f"Linked `{id}` and this channel", color=random.randint(0, 16777215)), True
    else:
      return discord.Embed(title="Error", description="This channel is already linked with another channel", color=random.randint(0, 16777215)), False

  def unlink(self, id: str):
    global db
    if id not in db["linkchannels"][str(self.cid)] or str(self.cid) not in db["linkchannels"][id]:
      return discord.Embed(title="Error", description="Invalid channel id", color=random.randint(0, 16777215)), False
    e = discord.Embed(title="Successfully deleted", color=random.randint(0, 16777215))
    id2 = db["linkchannels"][str(self.cid)]
    id1 = db["linkchannels"][id]
    if str(self.cid) in id1:
      if len(id1) == 1:
        del db["linkchannels"][str(self.cid)]
      else:
        del db["linkchannels"][str(self.cid)][db["linkchannels"][str(self.cid)].index(id)]
      e.add_field(name=f"{id} > {self.cid}", value="_ _", inline=False)
    if id in id2:
      if len(id2) == 1:
        del db["linkchannels"][id]
      else:
        del db["linkchannels"][id][db["linkchannels"][id].index(str(self.cid))]
      e.add_field(name=f"{self.cid} > {id}", value="_ _", inline=False)
    return e, True

class Singleton(type):
  _instances = {}
  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
    return cls._instances[cls]

class Database(dict):
  def __init__(self, directory: str = "./", filename: str = "db.json"):
      self.__fullpath = directory + filename
      super().__init__()
      self.file = JsonFile(self.__fullpath)
      self.backup = JsonFile(f"{directory}backup.json")
      self.dict = self.file.data
      atexit.register(self.__del)

  def __getitem__(self, key):
      return self.dict[key]

  def __setitem__(self, key, value):
      self.dict[key] = value

  def __repr__(self):
      return self.dict.__repr__()

  def __contains__(self, item):
      return item in self.dict

  def __del(self):
      self.file.data = self.dict
      self.backup.data = self.dict
      self.file.save()
      self.backup.save()

def Embed(
    msg: Union[commands.Context, discord.Interaction, discord.Message],
    description: str = '',
    title: str = '',
    fields: list = [],
    footer: dict = {},
    image: dict = {},
    image_url: str = None,
    thumbnail: dict = {},
    thumbnail_url: str = None,
    video: dict = {},
    video_url: str = None,
    author: dict = {},
    type: str = 'rich',
    timestamp: datetime.datetime = None,
    color: Union[discord.Colour, int] = None,
    colour: Union[discord.Colour, int] = None):
    return discord.Embed.from_dict(
        {
        'title': title,
        'description': description,
        'footer': footer,
        'fields': fields,
        'image': {'url': image_url} if image_url else image,
        'thumbnail': {'url': thumbnail_url} if thumbnail_url else thumbnail,
        'video': {'url': video_url} if video_url else video,
        'author': author if author else {'name': msg.command.name.title() if (isinstance(msg, commands.Context) and msg.command) else msg.data.name.title() if isinstance(msg, discord.Interaction) else '',
        'icon_url': 'https://cdn.discordapp.com/attachments/914750432520331304/933032744349474836/carbot.png'} if isinstance(msg, (commands.Context, discord.Interaction)) else {},
        'type': type,
        'timestamp': timestamp,
        'color': color if color else colour if colour else None
      }
    )

class JsonFile(object):
  __data: Dict[Any, Any]
  def __init__(self, filename):
      self.filename = filename
      self.__data = {}
      self.load()

  def __enter__(self):
      return self.__data

  def __exit__(self, exc_type, exc_val, exc_tb):
      self.save()

  def __contains__(self, item):
      return item in self.__data

  def load(self):
      try:
          with open(self.filename, 'r') as f:
              self.__data = json.load(f)
      except (FileNotFoundError, json.decoder.JSONDecodeError):
          with open(self.filename, 'w') as f:
              json.dump({}, f)

  def save(self):
      with open(self.filename, "w") as f:
          json.dump(self.__data, f, indent = 4)

  @property
  def data(self):
      return self.__data

  @data.setter
  def data(self, value):
      self.__data = value

class RedisDBLive(dict):
  def __init__(self, name: str = "main", key: str = None, *, host: str, port: int, password: str, client_name: str, charset: str = "utf-8", decode_responses: bool = True, dont_save: bool = False):
    super().__init__()
    self._redis = rd.Redis(host = host, port = port, password = password, client_name = client_name, charset = charset, decode_responses = decode_responses, health_check_interval = 1000)
    atexit.register(self.__del)
    self._backup = JsonFile("backup.json")
    self.__ds = dont_save
    self._name = name
    self._var = {}
    self._key = key if key else name
    self.__load()

  def __getitem__(self, item):
    # if self._var == {}:
    #   self._var = json.loads(self._redis.hget(self._name, self._key))
    return self._var[item]

  def __setitem__(self, key, value):
    self._var[key] = value
    if not self.__ds:
      self._redis.hset(self._name, self._key, json.dumps(self._var))

  def __contains__(self, item):
    # if self._var == {}:
    #   self._var = json.loads(self._redis.hget(self._name, self._key))
    return item in self._var

  def __repr__(self):
    return self._var.__repr__()
      
  def __del(self):
    if not self.__ds:
      try:
        self._redis.hset(self._name, self._key, json.dumps(self._var))
      except Exception as e:
        print(e)
        self._var["crashed"] = True
        self._backup.data = self._var
        self._backup.save()
    self._redis.close()

  def __load(self):
    if self._var == {}:
      if "crashed" in self._backup.data:
        if self._backup.data["crashed"]:
          del self._backup.data["crashed"]
          self._var = self._backup.data
        else:
          self._var = json.loads(self._redis.hget(self._name, self._key))
      else:
        self._var = json.loads(self._redis.hget(self._name, self._key))


class RedisDB(dict):
  def __init__(self, name: str = "main", key: str = None, *, host: str, port: int, password: str, client_name: str, charset: str = "utf-8", decode_responses: bool = True, dont_save: bool = False):
    self._redis = rd.Redis(host = host, port = port, password = password, client_name = client_name, charset = charset, decode_responses = decode_responses, health_check_interval = 1000)
    super().__init__()
    self._backup = JsonFile("backup.json")
    self._name = name
    self.__ds = dont_save
    self._key = key if key else name
    self._var = self._load(True)
    atexit.register(self.__del)

  def __getitem__(self, key):
      return self._var[key]

  def __setitem__(self, key, value):
      self._var[key] = value
      if not self.__ds:
        self._save()

  def __repr__(self):
      return self._var.__repr__()

  def __enter__(self) -> dict:
      return self._load()

  def __exit__(self, exc_type, exc_value, exc_traceback):
      if not self.__ds:
        self._save()

  def __contains__(self, item):
      return item in self._var

  def _load(self, backup = False):
      if self._key not in self._redis.keys():
          self._redis.hset(self._name, self._name, "{}")
      self._var = json.loads(self._redis.hget(self._name, self._key))
      if backup:
          if self._var != self._backup.data and self._backup.data:
              self._var = self._backup.data
              self._backup.data = {}
              self._backup.save()
      return self._var

  def _save(self):
      try:
          if self._var != json.loads(self._redis.hget(self._name, self._key)):
              self._redis.hset(self._name, self._key, json.dumps(self._var))
      except Exception:
          self._backup.data = self._var
          self._backup.save()

  def __del(self):
      if not self.__ds:
          self._save()
      self._redis.close()

async def Webhook(ctx, channel = None):
  if ctx != None:
    if channel != None:
      for webhook in (await channel.webhooks()):
        if webhook.user.id == ctx.bot.user.id and webhook.name == "PythonBot Webhook":
          return webhook
      return (await channel.create_webhook(name="PythonBot Webhook"))

    for webhook in (await ctx.channel.webhooks()):
      if webhook.user.id == ctx.bot.user.id and webhook.name == "PythonBot Webhook":
        return webhook
    return (await ctx.channel.create_webhook(name="PythonBot Webhook"))

# noinspection PyBroadException
class Upload():
  def __init__(self, url: str, filename: str, path: str = "./", _chunk_size: int = 1024, _delete_after: float = 0):
    self._url = url
    self._filename = filename
    self._path = path
    self.__chunk_size = _chunk_size
    self.__delete_after = _delete_after

  def __enter__(self):
    if not os.path.exists(self._path):
      self.createDirectory(self._path)
    self._opnfile = open((self._path + self._filename), "wb")
    r = rq.get(self._url, stream = True)
    for chunk in r.iter_content(self.__chunk_size):
      if not chunk:
        break
      self._opnfile.write(chunk)
    return self._opnfile

  def __exit__(self, exc_type, exc_value, exc_traceback):
    self._opnfile.close()
    if self.__delete_after:
      time.sleep(self.__delete_after)
    os.remove(f"{self._path}{self._filename}")

  def createDirectory(self, directories: str):
    c_path = "."
    for dirs in directories.split("/")[1:]:
      if dirs:
        c_path = c_path + f"/{dirs}"
        if not os.path.exists(c_path):
          os.mkdir(c_path)

  def download(self):
    if not os.path.exists(self._path):
      self.createDirectory(self._path)
    with open((self._path + self._filename), "wb") as opnfile:
      r = rq.get(self._url, stream = True)
      for chunk in r.iter_content(self.__chunk_size):
        if not chunk:
          break
        opnfile.write(chunk)
      return opnfile

  def delete(self):
    try:
      if self.__delete_after:
        time.sleep(self.__delete_after)
      os.remove(f"{self._path}{self._filename}")
    except Exception as e:
      print(f"{e.__class__.__name__}: {e}")
    return None

def dividers(array: list, divider: str = " | "):
  ft = []
  for i in array:
    if i:
      ft.append(i)
  return divider.join(ft) if divider else ""

dontsave = False
if os.environ["TEST"] != "y":
  dontsave = True

db = None
try:
  db = RedisDBLive("bot", host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = None, dont_save = dontsave)
except Exception:
  db = Database()
