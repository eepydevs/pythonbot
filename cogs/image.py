#cog by maxy#2866
import asyncio
import disnake as discord
import random
from disnake.ext import commands
from utils import RedisManager, PopcatAPI, Upload

popcat = PopcatAPI()

class Image(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.slash_command()
  async def image(self, inter):
    pass
  
  @image.sub_command()
  async def jail(self, inter, member: discord.Member):
    '''
    Jail someone
    
    Parameters
    ----------
    member: Member here'''
    await inter.response.defer()
    e = discord.Embed(title = f"{member.name} got jailed", color = random.randint(0, 16667215))
    e.set_image(popcat.jail(str(member.avatar)))
    await inter.send(embed = e)
    
  @image.sub_command()
  async def unforgivable(self, inter, text: str):
    '''
    Unforgivable
    
    Parameters
    ----------
    text: Text
    '''
    await inter.response.defer()
    e = discord.Embed(color = random.randint(0, 16667215))
    e.set_image(popcat.unforgivable(text))
    await inter.send(embed = e)
    
  @image.sub_command()
  async def sadcat(self, inter, text: str):
    '''
    Sad cat looks at text
    
    Parameters
    ----------
    text: Text
    '''
    await inter.response.defer()
    e = discord.Embed(color = random.randint(0, 16667215))
    e.set_image(popcat.sad_cat(text))
    await inter.send(embed = e)
    
  @image.sub_command()
  async def cars(self, inter):
    '''
    Get random car images
    '''
    await inter.response.defer()
    r = popcat.car_pictures()
    e = discord.Embed(title = r["title"], color = random.randint(0, 16667215))
    e.set_image(r["image"])
    await inter.send(embed = e)
    
  @image.sub_command()
  async def pooh(self, inter, top_text: str, bottom_text: str):
    '''
    Normal and Tuxedo Pooh
    
    Parameters
    ----------
    top_text: Top text
    bottom_text: Bottom text
    '''
    await inter.response.defer()
    e = discord.Embed(color = random.randint(0, 16667215))
    e.set_image(popcat.pooh(top_text, bottom_text))
    await inter.send(embed = e)
    
  @image.sub_command()
  async def wanted(self, inter, member: discord.Member):
    '''
    Make someone wanted
    
    Parameters
    ----------
    member: Member here'''
    await inter.response.defer()
    e = discord.Embed(title = f"{member.name} is wanted", color = random.randint(0, 16667215))
    e.set_image(popcat.wanted(str(member.avatar)))
    await inter.send(embed = e)
    
  @image.sub_command()
  async def whowouldwin(self, inter, image_url1: str, image_url2: str):
    '''
    Who would win?
    
    Paramaters
    ----------
    image_url1: Left image
    image_url2: Right image
    '''
    await inter.response.defer()
    e = discord.Embed(title = "Who would win?", color = random.randint(0, 16667215))
    e.set_image(popcat.who_would_win(image_url1, image_url2))
    await inter.send(embed = e)
    
  @image.sub_command()
  async def gun(self, inter, member: discord.Member):
    '''
    Give a gun to yourself
    
    Parameters
    ----------
    member: Member here'''
    await inter.response.defer()
    e = discord.Embed(title = f"{member.name} is now armed", color = random.randint(0, 16667215))
    e.set_image(popcat.gun(str(member.avatar).replace("?size=1024", str())))
    await inter.send(embed = e)
    
  @image.sub_command()
  async def drake(self, inter, top_text: str, bottom_text: str):
    '''
    Drake with top and bottom text
    
    Paramaters
    ----------
    image_url1: Top text
    bottom_text: Bottom text
    '''
    await inter.response.defer()
    e = discord.Embed(color = random.randint(0, 16667215))
    e.set_image(popcat.drake(top_text, bottom_text))
    await inter.send(embed = e)
    
  @image.sub_command()
  async def ship(self, inter, member1: discord.Member = None, *, member2: discord.Member = None):
    '''
    Ship someone
    
    Parameters
    ----------
    member1: Left user, Defaults to yourself
    member2: Right user, Defaults to random
    '''
    await inter.response.defer()
    if member1 is None: member1 = inter.author
    if member2 is None: member2 = random.choice(inter.guild.members)
    e = discord.Embed(title = "You two make a cute couple together!", color = random.randint(0, 16667215))
    e.set_image(popcat.ship(str(member1.avatar).replace("?size=1024", str()), str(member2.avatar).replace("?size=1024", str())))
    await inter.send(embed = e)\
    
  @image.sub_command()
  async def bidentweet(self, inter, text: str):
    '''
    Biden tweets your text
    
    Parameters
    ----------
    text: Text
    '''
    await inter.response.defer()
    e = discord.Embed(color = random.randint(0, 16667215))
    e.set_image(popcat.biden_tweet(text))
    await inter.send(embed = e)
  
  @image.sub_command()
  async def pikachu(self, inter, text: str):
    '''
    Surprised pikachu
    
    Parameters
    ----------
    text: Text
    '''
    await inter.response.defer()
    e = discord.Embed(color = random.randint(0, 16667215))
    e.set_image(popcat.pikachu(text))
    await inter.send(embed = e)
    
  @image.sub_command()
  async def colorify(self, inter, member: discord.Member, color_hex: str):
    '''
    Make yourself colorful
    
    Parameters
    ----------
    member: Member here
    color_hex: HEX of a color
    '''
    await inter.response.defer()
    e = discord.Embed(color = random.randint(0, 16667215))
    e.set_image(popcat.colorify(str(member.avatar), color_hex))
    await inter.send(embed = e)  
  
  @image.sub_command()
  async def drip(self, inter, member: discord.Member):
    '''
    Have some drip
    
    Parameters
    ----------
    member: Member here'''
    await inter.response.defer()
    e = discord.Embed(title = f"{member.name} got dripped up", color = random.randint(0, 16667215))
    e.set_image(popcat.drip(str(member.avatar)))
    await inter.send(embed = e)
    
  @image.sub_command()
  async def clown(self, inter, member: discord.Member):
    '''
    Someone clowned you
    
    Parameters
    ----------
    member: Member here'''
    await inter.response.defer()
    e = discord.Embed(title = f"{member.name} got clowned", color = random.randint(0, 16667215))
    e.set_image(popcat.clown(str(member.avatar)))
    await inter.send(embed = e)
    
  @image.sub_command()
  async def advert(self, inter, member: discord.Member):
    '''
    Make yourself an advert
    
    Parameters
    ----------
    member: Member here'''
    await inter.response.defer()
    e = discord.Embed(title = f"{member.name} got advertised", color = random.randint(0, 16667215))
    e.set_image(popcat.ad(str(member.avatar)))
    await inter.send(embed = e)
    
  @image.sub_command()
  async def blur(self, inter, member: discord.Member):
    '''
    Blur yourself
    
    Parameters
    ----------
    member: Member here'''
    await inter.response.defer()
    e = discord.Embed(title = f"{member.name} got blured", color = random.randint(0, 16667215))
    e.set_image(popcat.blur(str(member.avatar)))
    await inter.send(embed = e)
  
  @image.sub_command()
  async def invert(self, inter, member: discord.Member):
    '''
    Get inverted
    
    Parameters
    ----------
    member: Member here'''
    await inter.response.defer()
    e = discord.Embed(title = f"{member.name} got inverted", color = random.randint(0, 16667215))
    e.set_image(popcat.invert(str(member.avatar)))
    await inter.send(embed = e)
    
  @image.sub_command()
  async def grayscale(self, inter, member: discord.Member):
    '''
    Become white-black
    
    Parameters
    ----------
    member: Member here'''
    await inter.response.defer()
    e = discord.Embed(title = f"{member.name} got grayscaled", color = random.randint(0, 16667215))
    e.set_image(popcat.grayscale(str(member.avatar).replace("?size=1024", str())))
    await inter.send(embed = e)
    
  @image.sub_command()
  async def joke_overhead(self, inter, member: discord.Member):
    '''
    You misheard the joke
    
    Parameters
    ----------
    member: Member here'''
    await inter.response.defer()
    e = discord.Embed(title = f"{member.name} got a joke over their head", color = random.randint(0, 16667215))
    e.set_image(popcat.joke_overhead(str(member.avatar).replace("?size=1024", str())))
    await inter.send(embed = e)
    
  @image.sub_command()
  async def pet(self, inter, member: discord.Member):
    '''
    Pet someone :3
    
    Parameters
    ----------
    member: Member here'''
    await inter.response.defer()
    dl = Upload(popcat.pet(str(member.avatar)), f"pet{member.id}.gif", "./image/")
    dl.download()
    with open(f"./image/pet{member.id}.gif", "rb") as file:
      msg = await inter.bot.get_channel(1060317600057393317).send(file = discord.File(file))
      e = discord.Embed(title = f"{member.name} got petted", color = random.randint(0, 16667215))
      e.set_image(msg.attachments[0].url)
      await inter.send(embed = e)
    dl.delete()
      
  @image.sub_command()
  async def caution(self, inter, text: str):
    '''
    Create a caution
    
    Parameters
    ----------
    text: Text
    '''
    await inter.response.defer()
    e = discord.Embed(color = random.randint(0, 16667215))
    e.set_image(popcat.caution(text))
    await inter.send(embed = e)
    
  @image.sub_command()
  async def alert(self, inter, text: str):
    '''
    Create an alert
    
    Parameters
    ----------
    text: Text
    '''
    await inter.response.defer()
    e = discord.Embed(color = random.randint(0, 16667215))
    e.set_image(popcat.alert(text))
    await inter.send(embed = e)
    
  @image.sub_command()
  async def facts_book(self, inter, text: str):
    '''
    Put text into facts book
    
    Parameters
    ----------
    text: Text
    '''
    await inter.response.defer()
    e = discord.Embed(color = random.randint(0, 16667215))
    e.set_image(popcat.facts(text))
    await inter.send(embed = e)
  
def setup(bot):
  bot.add_cog(Image(bot))