from typing import Union
import datetime
import disnake as discord
from rocksdict import Rdict
from disnake.ext import commands
import os

class Singleton(type):
  _instances = {}
  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
    return cls._instances[cls]
    
class RdictManager(metaclass = Singleton):
    def __init__(self, path: str):
        self._path = path
        
    def __enter__(self) -> dict:
        self._rdict = Rdict(self._path)
        if "main" not in self._rdict:
            self._rdict["main"] = {}
        self._var = self._rdict["main"]
        return self._var
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._rdict["main"] = self._var
        self._rdict.close()
        
    def sync(self, cvar: dict = None) -> dict:
        self._c = Rdict(self._path)
        if "main" not in self._c:
            self._c["main"] = {}
        if cvar:
            self._c["main"] = cvar
        self._v = self._c["main"]
        self._c.close()
        return self._v
        
        # with RdictManager(self._path) as self._c:
        #     if cvar:
        #         self._c = cvar
        #     return self._c
        
        

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