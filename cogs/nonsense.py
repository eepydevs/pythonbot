#cog by maxy#2866
import disnake as discord
from disnake.ext import commands
from enum import Enum
import ossapi as osu
import re
import os
import utils
import random
import asyncio
import json
import math
from webcolors import hex_to_rgb
import roblox as rblx
from roblox.thumbnails import AvatarThumbnailType
import datetime, time
import requests as rq
from utils import RedisManager, PopcatAPI
from dotenv import load_dotenv
from pp_calc import calc as pp
load_dotenv()

popcat = PopcatAPI()

osuapi = osu.OssapiV2(18955, os.environ["OSU"])
whitelist_id = [439788095483936768, 417334153457958922, 902371374033670224, 691572882148425809, 293189829989236737, 826509766893371392, 835455268946051092, 901115550695063602]

ranks = {
  'D': '<:D_:1054751662394318888>',
  'C': '<:C_:1054751660431392768>',
  'B': '<:B_:1054751658879483934>',
  'A': '<:A_:1054751657138847834>',
  'S': '<:S_:1054751655452745738>',
  'SH': '<:SH:1054751653758255104>',
  'XH': '<:XH:1054751664436944897>',
  'X': '<:X_:1054751667687522336>',
}

crblx = rblx.Client(os.environ["RBLXS"])

with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
  if "tupper" not in db:
    db["tupper"] = {}

  if "customcmd" not in db:
    db["customcmd"] = {}

  if "linkchannels" not in db:
    db["linkchannels"] = {}

  if "bookmarks" not in db:
    db["bookmarks"] = {}
    
  if "apifavs" not in db:
    db["apifavs"] = {}
    
def esc_md(text: str):
  return text.replace('_', '\_').replace('*', '\*').replace('`', '\`').replace('~', '\~')
  
calc_acc = lambda c300 = 0, c100 = 0, c50 = 0, miss = 0: round((300 * c300 + 100 * c100 + 50 * c50) / 300 / (c300 + c100 + c50 + miss) * 100, 2)
  
class Required1(str, Enum):
  You = "True"
  Everyone = ""

class Required2(str, Enum):
  Normal = "Normal"
  Await = "Await"

class menuthing(discord.ui.Select):
  def __init__(self, inter: discord.Interaction):
    self.inter = inter
    options = [
      discord.SelectOption(label = "Option 1", emoji = "1️⃣", value = "1"),
      discord.SelectOption(label = "Option 2", emoji = "2️⃣", value = "2"),
      discord.SelectOption(label = "Option 3", emoji = "3️⃣", value = "3")
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
    
  async def callback(self, interaction: discord.MessageInteraction):
    await interaction.send(f"You selected Option {self.values[0]}!", ephemeral = True)

class menuView(discord.ui.View):
  def __init__(self, inter: discord.Interaction):
      super().__init__()
      self.add_item(menuthing(inter))

class buttonthing(discord.ui.View):
  def __init__(self, inter: discord.Interaction):
    super().__init__(timeout = 60)
    self.inter = inter
    
  async def interaction_check(self, inter: discord.MessageInteraction):
    if inter.author != self.inter.author:
      await inter.send("Those buttons are not for you", ephemeral = True)
      return False
    return True
    
  @discord.ui.button(label = "Primary", custom_id = "Primary", emoji = "1️⃣", style = discord.ButtonStyle.blurple)
  async def primary_button(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
    await interaction.send("You clicked Primary", ephemeral = True)

  @discord.ui.button(label = "Secondary", custom_id = "Secondary", emoji = "2️⃣", style = discord.ButtonStyle.gray)
  async def secondary_button(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
    await interaction.send("You clicked Secondary", ephemeral = True)

  @discord.ui.button(label = "Success", custom_id = "Success", emoji = "✅", style = discord.ButtonStyle.green)
  async def success_button(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
    await interaction.send("You clicked Success", ephemeral = True)

  @discord.ui.button(label = "Danger", custom_id = "Danger", emoji = "⚠️", style = discord.ButtonStyle.red)
  async def danger_button(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
    await interaction.send("You clicked Danger", ephemeral = True)

  """@discord.ui.button(label = "Link", custom_id = "Link", emoji = "🔗", style = discord.ButtonStyle.gray)
  async def link_button(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
    await interaction.send("You clicked Link", ephemeral = True)"""
  
def shuffle(x):
  return random.sample(x, len(x))

async def suggest_snip(inter, input):
  with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
    if str(inter.author.id) not in db["apifavs"]:
      db["apifavs"][str(inter.author.id)] = {}
    if not input:
      input = "https://api.popcat.xyz"
    return [input] + [fav for fav in list(db["apifavs"][str(inter.author.id)].keys()) if input.lower() in fav.lower()][0:23] if db["apifavs"][str(inter.author.id)] and [fav for fav in list(db["apifavs"][str(inter.author.id)].keys()) if input.lower() in fav.lower()][0:24] else [input]
  
async def suggest_dsnip(inter, input):
  with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
    if str(inter.author.id) not in db["apifavs"]:
      db["apifavs"][str(inter.author.id)] = {}
    return [fav for fav in list(db["apifavs"][str(inter.author.id)].keys()) if input.lower() in fav.lower()][0:24] if db["apifavs"][str(inter.author.id)] and [fav for fav in list(db["apifavs"][str(inter.author.id)].keys()) if input.lower() in fav.lower()][0:24] else ["You have nothing! Go create a snippet!"]

async def suggest_tupper(inter, input):
  with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
    if str(inter.author.id) not in db["tupper"]:
      db["tupper"][str(inter.author.id)] = {}
    return [tupper for tupper in list(db["tupper"][str(inter.author.id)].keys()) if input.lower() in tupper.lower()][0:24] if db["tupper"][str(inter.author.id)] and [tupper for tupper in list(db["tupper"][str(inter.author.id)].keys()) if input.lower() in tupper.lower()][0:24] else ["You have nothing! Go create a tupper!"]

async def suggest_rblxuser(inter, input):
  if not input:
    input = "ROBLOX"
  if len(input) < 4:
    return ["Username is too short"]
  try:
    return [user.name async for user in crblx.user_search(input, max_items = 30) if input.lower() in user.name.lower()][0:24] if [user.name async for user in crblx.user_search(input, max_items = 30) if input.lower() in user.name.lower()][0:24] else ["Users not found"]
  except rblx.InternalServerError:
    return ["Users not found"]

async def suggest_command(inter, input):
  with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
    if str(inter.author.id) not in db["notes  "]:
      db["customcmd"][str(inter.author.id)] = {}
    return [command for command in list(db["customcmd"][str(inter.author.id)].keys()) if input.lower() in command.lower()][0:24] if db["customcmd"][str(inter.author.id)] and [command for command in list(db["customcmd"][str(inter.author.id)].keys()) if input.lower() in command.lower()][0:24] else ["You have nothing! Go create a command!"]

def runbf(str):
  array = [0] * 30000
  i = 0
  codei = 0
  codeiStack = []
  strp = []
  while codei < len(str):
    l = str[codei]
    #increase
    if l == '+':
      array[i] = ((array[i] + 1) % 255)
    #decrease
    elif l == '-':
      array[i] = ((array[i] - 1) % 255)
    #go one cell right
    elif l == ">":
      i += 1
    #go one cell left
    elif l == "<":
      i -= 1
    #input ascii character in strp array
    elif l == ".":
      strp.append(chr(array[i]))
    #join every letter in strp array and print
    elif l == '[':
      codeiStack.append(codei)
    elif l == ']':
      if array[i] != 0:
        #restart the loop
        codei = codeiStack[-1]
      else:
        #exit the loop
        codeiStack.pop()
    codei += 1
  if len(strp) != 0:
    return "".join(f"{ll}" for ll in strp)
  else:
    pass

def calc(text):
  check = text.split(" ")
  whitelist = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "/", "%", "+", "-", "(", ")", " ", "."]
  for i in range(len(check)):
    if len(check[i]) < 15:
      continue
    else:
      raise Exception("Maximum amount of characters per spaced string is 15!")
  if all(i in whitelist for i in text):
    return eval(text)
  else:
    raise ValueError("Something went wrong... (You may have used non-int)")

def express(inter, text):
  table = {"{author}": inter.author.name, "{author.mention}": f"<@{inter.author.id}>",
           "{server}": inter.guild.name, "{server.id}": str(inter.guild.id),
           "{channel}": inter.channel.name, "{channel.id}": str(inter.channel.id)}

  result = []
  splitted = text.split(" ")
  for word in splitted:
    if word.lower() in table:
      result.append(table[word.lower()])
    else:
      result.append(word)

  return " ".join(result)
    
class Nonsense(commands.Cog):
  def __init__(self, bot):
    self.bot = bot  

  @commands.Cog.listener()
  async def on_message(self, msg):
    if msg.author.bot or msg.author.discriminator == 0000:
      return
    try:
      with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
        if str(msg.guild.id) in db["serversetting"]["nqn"]:
          reg = ':[a-zA-Z]+:'
          other = re.split(reg, msg.content)
          emjs = re.findall(reg, msg.content)
          content=other[0]
          for i in range(len(emjs)):
            myemjs = tuple(filter(lambda emj: emj.name==emjs[i][1:-1], self.bot.emojis))
            emj = f'<:{myemjs[0].name}:{myemjs[0].id}>' if (any(myemjs) and not other[i].endswith('<')) else emjs[i]
            content+=emj+other[i+1]
            
          if content==msg.content: return
          if msg.reference and len(msg.content.split())==1:
            await msg.delete()
            await self.react.__call__(msg, myemjs[0], msg.reference.resolved)
          else:
            webhook = (await utils.Webhook((commands.Context(message = msg, bot = self.bot, view = None))))
            await msg.delete()
            await webhook.send(content=content, username=msg.author.display_name, avatar_url=msg.author.avatar, allowed_mentions=discord.AllowedMentions.none())
            
        if "linkchannels" in db:
          with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
            if str(msg.channel.id) in list(db["linkchannels"].keys()):
              for channel in db["linkchannels"][str(msg.channel.id)]:
                webhook = (await utils.Webhook((commands.Context(message = msg, bot = self.bot, view = None)), self.bot.get_channel(int(channel))))
                atch = ' '.join([f"[{i.filename}]({i.url})" for i in msg.attachments])
                rlatch = None
                rmsg = ''
                if not msg.reference is None:
                  rlatch = ' '.join([f"[{i.filename}]({i.url})" for i in msg.reference.resolved.attachments])
                  rmsg = ("> " + "\n> ".join(msg.reference.resolved.content.split("\n")) + (("\n> " + f"[ {rlatch} ]") if rlatch else "")   + f"\n@{msg.reference.resolved.author.name}{('#' + msg.reference.resolved.author.discriminator) if int(msg.reference.resolved.author.discriminator) != 0000 else ''}\n" if not msg.reference is None else "")
                await webhook.send(content= ((rmsg if len(rmsg) < 1999 else ('> `Too many replies to show!`' + f"\n@{msg.reference.resolved.author.name}{('#' + msg.reference.resolved.author.discriminator) if int(msg.reference.resolved.author.discriminator) != 0000 else ''}\n" if not msg.reference is None else "")) + msg.content + (('\n' + f"[ {atch} ]") if msg.attachments else ''))[0:1999], username=f"{msg.author.name}#{msg.author.discriminator} ({msg.guild.name})", avatar_url=msg.author.avatar, allowed_mentions=discord.AllowedMentions.none())
    except:
      pass
    
  @commands.slash_command()
  async def api(self, inter):
    with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
      if str(inter.author.id) not in db["apifavs"]:
        db["apifavs"][str(inter.author.id)] = {}
  
  @api.sub_command()
  async def request(self, inter, baseurl: str = commands.Param(autocomplete = suggest_snip), options = None, params: str = None, ephemeral: Required1 = Required1.You):
    '''
    GET Request something from an API
    
    Parameters
    ----------
    ephemeral: Visibility of the embed | Default: You
    baseurl: API Base URL to request | Example: https://api.popcat.xyz
    options: Options for API request | Example: /github/peppy
    params: Parameters to use in the request | Example: uid=123, score=456
    '''
    with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
      if options:
        if baseurl in db["apifavs"][str(inter.author.id)]: baseurl = db["apifavs"][str(inter.author.id)][baseurl]       
        if baseurl.endswith("/") and options.startswith("/"): url = baseurl[:-1] + options
        else:
          if not any([baseurl.endswith("/"), options.startswith("/")]):
            url = baseurl + "/" + options
          else:
            url = baseurl + options
      else:
        url = baseurl
      if not url.startswith(("https://", "http://")): url = "https://" + url
      furl = None
      await inter.response.defer(ephemeral = ephemeral)
      if inter.author.id in whitelist_id:
        e = discord.Embed(url = url, title = f"API: {url}", color = random.randint(0, 16667215))
        param = {}
        if not params is None:
          for i in params.split(","):
            param.update({i.split("=")[0].strip(): i.split("=")[1].strip()})
        response = rq.get(url = url, params = param if param else None)
        e.add_field(name = "Complete URL", value = f"```{response.url}```", inline = False)
        try:
          rjson = [json.dumps(response.json()), True]
        except rq.JSONDecodeError:
          e.set_image(url = response.url)
          rjson = ["VVV (no picture means there is nothing as result or an error)", False]
        except rq.ConnectionError:
          rjson = ["Something went wrong...", False]
        e.add_field(name = "Results", value = f"```json\n{rjson[0]}\n```" if rjson[1] else f"`{rjson[0]}`", inline = False)
      else:
        e = discord.Embed(url = url, title = f"API: {url}", color = random.randint(0, 16667215))
        param = {}
        if not params is None:
          for i in params.split(","):
            param.update({i.split("=")[0].strip(): i.split("=")[1].strip()})
        furl = f"{url}?" + "&".join(f"{k}={v}" for k, v in zip(param.keys(), param.values()))
        e.add_field(name = "Complete URL", value = f"```{furl}```", inline = False)
    view = discord.ui.View()
    style = discord.ButtonStyle.gray
    item = discord.ui.Button(style = style, label = "Requested API URL", url = furl if furl else response.url)
    view.add_item(item)
    await inter.send(embed = e, view = view)
    
  @api.sub_command()
  async def snip(inter, snipname, url):
    '''
    Create a Custom Command for yourself

    Parameters
    ----------
    snipname: Snippet name
    url: API Base URL | Example: https://api.popcat.xyz/
    '''
    await inter.response.defer(ephemeral = True)
    with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
      if snipname not in db["apifavs"][str(inter.author.id)]:
        db["apifavs"][str(inter.author.id)].update({snipname: url})
        e = discord.Embed(title = "Successful", description = f"Successfully added `{snipname}`", color = random.randint(0, 16777215))
        await inter.send(embed = e)
      else:
        e = discord.Embed(title = "Error", description = "A snippet with this name already exists", color = random.randint(0, 16777215))
        await inter.send(embed = e)    

  @api.sub_command()
  async def delete(inter, snipname: str = commands.Param(autocomplete = suggest_dsnip)):
    '''
    Delete an existing snippet

    Parameters
    ----------
    snipname: Snippet to delete 
    '''
    await inter.response.defer(ephemeral = True)
    with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
      if snipname in db["apifavs"][str(inter.author.id)]:
        db["apifavs"][str(inter.author.id)].pop(snipname)
        e = discord.Embed(title = "Successful", description = f"Successfully removed `{snipname}`", color = random.randint(0, 16777215))
        await inter.send(embed = e)
      else:
        e = discord.Embed(title = "Error", description = "This snippet doesn't exist", color = random.randint(0, 16777215))
        await inter.send(embed = e)

  @commands.slash_command()
  async def info(self, inter):
    pass
    
  @info.sub_command()
  async def github(self, inter, username: str):
    '''
    See someones Github profile
    
    Parameters
    ----------
    username: Github username
    '''
    await inter.response.defer()
    r = popcat.github(username)
    e = discord.Embed(url = r["url"], title = (username + f" [{r['account_type']}]"), description = f"Followers: `{r['followers']}`\nFollowing: `{r['following']}`" + (f'\nPublic repos: `{r["public_repos"]}`' if r['public_repos'] != '0' else '') + (f'\nPublic gists: `{r["public_gists"]}`' if r['public_gists'] != '0' else '') + "\n" + (f'\nLocation: `{r["location"]}`' if r['location'] != 'None' else '') + (f'\nCompany: `{r["company"]}`' if r['company'] != 'None' else '') + (f'\nBlog: `{r["blog"]}`' if r['blog'] != 'None' else '') + (f'\nEmail: `{r["email"]}`' if r['email'] != 'None' else '') + (f'\nTwitter: `{r["twitter"]}`' if r['twitter'] != 'Not set' else ''), color = random.randint(0, 16667215)) 
    e.add_field(name = "Registered", value = f"<t:{r['created_at']}:R>")
    e.add_field(name = "Last updated", value = f"<t:{r['updated_at']}:R>")
    e.add_field(name = "Bio", value = r["bio"], inline = False)
    e.set_thumbnail((r["avatar"]))
    await inter.send(embed = e)
    
  @info.sub_command()
  async def steam(self, inter, game_name: str):
    '''
    See info about a Steam game
    
    Parameters
    ----------
    game_name: Game name here
    '''
    await inter.response.defer()
    r = popcat.steam(game_name)
    if not "error" in r:
      e = discord.Embed(url = r["website"] if r["website"] != "None" else None, title = f"{r['name']} [{r['type'].title()}]", description = r["description"].replace("&quot;", '"'), color = random.randint(0, 16667215))
      e.add_field(name = "Developed by", value = ", ".join(r["developers"]))
      e.add_field(name = "Published by", value = ", ".join(r["publishers"]))
      e.add_field(name = "Price", value = r["price"], inline = False)
      e.set_image(r["banner"])
      await inter.send(embed = e)
    else:
      e = discord.Embed(title = "Error", description = r["error"], color = random.randint(0, 16667215))
      await inter.send(embed = e)
      

  @commands.slash_command()
  async def tetrio(self, inter):
    pass
  
  @tetrio.sub_command()
  async def stats(self, inter):
    """
    See global stats of TETR.IO    
    """
    await inter.response.defer()
    url = "https://ch.tetr.io/api/general/stats"
    response = rq.request("GET", url)
    rjson = response.json()["data"]
    e = discord.Embed(url = "https://ch.tetr.io/", title = "TETR.IO Server stats", color = random.randint(0, 16667215))
    e.add_field(name = f"Total players: {rjson['usercount']}", value = f"> Of which registered: `{rjson['usercount'] - rjson['anoncount']}`" + "\n" + f"> Of which anonymous: `{rjson['anoncount']}`" + "\n" + f"> Of which ranked: `{rjson['rankedcount']}`" + "\n" + f"Users registered a second\*: `{round(rjson['usercount_delta'])}` (rounded)" + "\n" + "\n" + f"Replays stored: `{rjson['replaycount']}`" + "\n" + f"Games played: `{rjson['gamesplayed']}`" + "\n" + f"> Of which finished: `{rjson['gamesfinished']}`" + "\n" + f"Games played a second\*: `{round(rjson['gamesplayed_delta'])}` (rounded)"+ "\n" + "\n" + f"Time played\*\*: `{round(rjson['gametime'] / 60 / 60)}` hours" + "\n" + f"--------------- or `{round(rjson['gametime'] / 60 / 60 / 24)}` days" + "\n" + f"--------------- or `{round(rjson['gametime'] / 60 / 60 / 24 / 365)}` years" + "\n" + "\n" + f"Pieces placed: `{rjson['piecesplaced']}`" + "\n" + f"Keypresses: `{rjson['inputs']}`", inline = False)
    e.set_footer(text = "* Through the last minute, ** Rounded")
    await inter.edit_original_message(embed = e)
    
  @tetrio.sub_command()
  async def user(self, inter, user: str):
    """
    Search for user info in TETR.IO
   
    Parameters
    ----------  
    user: User Name or MongoID 
    """
    user = user.lower()
    await inter.response.defer()
    url = f"https://ch.tetr.io/api/users/{user}"
    response = rq.request("GET", url)
    if "data" in response.json():
      rjson = response.json()["data"]["user"]
      league = rjson["league"]
      e = discord.Embed(url = f"https://ch.tetr.io/u/{user}", title = f"{esc_md(rjson['username'])} `[{rjson['role'].upper()}]`" + (f" `[✅]`" if rjson['verified'] else "") + (f" `[{'⭐' * rjson['supporter_tier']}]`" if rjson['supporter_tier'] else ""), description = ((f"Country: :flag_{rjson['country'].lower()}:" if rjson['country'] != "XM" else "Country: The Moon") if rjson["country"] else ""), color = random.randint(0, 16667215))
      e.add_field(name = "Joined:", value = f"<t:{str(time.mktime(time.strptime(rjson['ts'].replace('T', ' ')[:rjson['ts'].find('.')], '%Y-%m-%d %H:%M:%S')))[:-2]}:R>" if "ts" in rjson else "Here since the beginning")
      e.add_field(name = "Statistics:", value = f"Experience: `{rjson['xp']}`\nPlay time: `{round(rjson['gametime'] / 60 / 60) if rjson['gametime'] else 0}` hours\nOnline games: `{rjson['gamesplayed']}`\n> Of which wins: `{rjson['gameswon']}`", inline = False)
      if league['gamesplayed']:
        e.add_field(name = "Tetra League:", value = f"Rank: **`{league['rank'].upper()}`**" + "\n" + ((f"Top rank: **`{league['bestrank'].upper()}`**" + "\n") if "bestrank" in league else "") + f"Record: **`{league['gameswon']}`**/`{league['gamesplayed']}` (`{'%.2f'%(league['gameswon'] / league['gamesplayed'] * 100) if league['gameswon'] and league['gamesplayed'] else 0}%`)" + "\n" + ((f"Rating: `{'%.2f'%(league['rating'])}`" + "\n") if "rating" in league else "") + ((f"Glicko: **`{'%.2f'%(league['glicko'])}`**±`{'%.2f'%(league['rd'])}`" + "\n") if "glicko" in league else "") + ((f"APM: `{league['apm']}`" + "\n") if "apm" in league else "") + ((f"PPS: `{league['pps']}`" + "\n") if "pps" in league else "") + ((f"VS: `{league['vs']}`" + "\n") if "vs" in league else ""), inline = True)
      e.set_footer(text = f"ID: {rjson['_id']}")
    else:
      rjson = response.json()
      e = discord.Embed(title = "Error", description = f"```{rjson['error']}```", color = random.randint(0, 16667215))
    await inter.send(embed = e)

  @commands.slash_command()
  async def osu(self, inter):
    pass

  @osu.sub_command()
  async def beatmap(self, inter, beatmapid: int):
    """
    Search for beatmap info in osu!

    Parameters
    ----------
    beatmapid: Beatmap id (INT)
    """
    info = osuapi.beatmap(beatmap_id = beatmapid)
    ranks = ["🕐 Pending", "⏫ Ranked", "✅ Approved", "✅ Qualified", "❤️ Loved", ":grave: Graveyard" "🕐 WIP"]
    m, s = divmod(info.total_length, 60)
    h, m = divmod(m, 60)
    e = discord.Embed(url = str(info.url), title = f'{info.beatmapset().artist} - {info.beatmapset().title} [{info.version}]', description = (f'Source: `{info.beatmapset().source}`' + '\n' if info.beatmapset().source else '') + '\n' + f'Status: `{ranks[info.status.value]}`' + '\n' + f'Submitted: <t:{int(datetime.datetime.fromisoformat(str(info.beatmapset().submitted_date)).timestamp())}:R>' + '\n' + f'Last updated: <t:{int(datetime.datetime.fromisoformat(str(info.beatmapset().last_updated)).timestamp())}:R>', color = random.randint(0, 16777215))
    e.add_field(name = "Beatmap info:", value = f'> Mapped by `{info.beatmapset().creator}`' + '\n' + f'> Max combo: `{info.max_combo}x`' + '\n' + f'> ⏲️ (BPM): `{info.bpm}`, ⏱️: `{m:02d}:{s:02d}`' + '\n' + f'> CS: `{info.cs}`, AR: `{info.ar}`, OD: `?`, HP: `{info.drain}`, Star rating: `{info.difficulty_rating} ⭐`' + '\n' + f'> Sucess rate: `{round(info.passcount / info.playcount * 100)}% ({info.passcount} / {info.playcount})`, ❤️ Favorited `{info.beatmapset().favourite_count}` times', inline = False)
    e.add_field(name = "Objects:", value = f"🔘: `{info.count_circles}`" + "\n" + f"➿: `{info.count_sliders}`" + "\n" + f"🔄: `{info.count_spinners}`", inline = False)
    e.add_field(name = "Misc:", value = f"Scorable: {str(info.is_scoreable)}" + "\n" + ((f"Features: `🎞️ Storyboard`" if info.beatmapset().storyboard else f"Features: `📼 Video`") if info.beatmapset().video or info.beatmapset().storyboard else "Features: `none`"), inline = False)
    e.set_thumbnail(url = str(info.beatmapset().covers.list_2x)) 
    e.set_footer(text = f"ID: {info.beatmapset_id} > {beatmapid}")
    await inter.send(embed = e)
    
  @osu.sub_command()
  async def user(self, inter, user: str):
    """
    Search for user info in osu!
    
    Parameters
    ----------
    user: User name or id
    """
    try:
      info = osuapi.user(user = user)
      rgb = tuple(hex_to_rgb(info.profile_colour)) if info.profile_colour else None 
      e = discord.Embed(url = f"https://osu.ppy.sh/users/{info.id}", title = esc_md(str(info.username)) + (f" `[#{info.statistics.global_rank}]`" if info.statistics.global_rank else "") + ((" `[" + "❤️" * info.support_level + "]`") if info.is_supporter else "") + (" `[🐍]`" if info.id == 13628906 else "") + (" `[PPY]`" if info.id == 2 else "") + (" `[DEV]`" if info.id in [2, 989377, 3562660, 1040328, 2387883, 102, 10751776, 718454, 102335, 941094, 307202, 1857058] else "") + (" `[GMT]`" if info.is_moderator or info.is_admin else "") + (" `[SPT]`" if info.id in [3242450, 5428812, 941094, 2295078, 444506, 1040328, 1857058, 3469385] else "") + (" `[BOT]`" if info.is_bot else "") + (" `[🟢]`" if info.is_online else ""), description = f"Country: `{info.country.name}` :flag_{info.country_code.lower()}: {(f'`[#{info.statistics.country_rank}]`' if info.statistics.global_rank else '')}" + ("\n" + f"Formerly known as: `{', '.join(str(i) for i in list(info.previous_usernames))}`" if list(info.previous_usernames) else "") + "\n" + ((f"Discord: `{info.discord}`"  + "\n") if info.discord else "") + (f"Plays with `{', '.join(str(style.name.lower().title()) for style in list(info.playstyle))}`" if info.playstyle else ""), color = discord.Color.from_rgb(r = rgb[0], g = rgb[1], b = rgb[2]) if info.profile_colour else random.randint(0, 16667215))
      e.add_field(name = "Joined:", value = f"<t:{int(info.join_date.timestamp())}:R>", inline = True)
      e.add_field(name = "Last visited:", value = f"<t:{int(info.last_visit.timestamp())}:R>")
      if not info.is_bot:
        e.add_field(name = "Statistics:", value = f"Performance Points: `{round(info.statistics.pp)}`" + "\n" +  f"Ranked Score: `{info.statistics.ranked_score}`" + "\n" + f"Hit Accuracy: `{info.statistics.hit_accuracy}%`" + "\n" + f"Play Count: `{info.statistics.play_count}`" + "\n" + f"Total Score: `{info.statistics.total_score}`" + "\n" + f"Total Hits: `{info.statistics.total_hits}`" + "\n" + f"Maximum Combo: `{info.statistics.maximum_combo}`" + "\n" + f"Replays watched by others: `{info.statistics.replays_watched_by_others}`", inline = False)
      if info.cover.url:
        e.set_image(url = str(info.cover.url))
      e.set_thumbnail(url = str(info.avatar_url))
      e.set_footer(text = f"ID: {info.id}")
      await inter.send(embed = e)
    except ValueError:
      e = discord.Embed(title = "Error", description = "User not found", color = random.randint(0, 16667215))
      await inter.send(embed = e, ephemeral = True)
      
  @osu.sub_command()
  async def rs(self, inter, user: str, index: int = 1):
    """
    See information about most recent score of mentioned user
    
    Parameters
    ----------
    user: User name or id
    index: Index of score (default: 1)
    """
    try:
      if req := osuapi.user_scores(osuapi.user(user = user).id, "recent"):
        await inter.response.defer()
        if index < 1:
          index = 1
        elif index > len(req):
          index = len(req)
        info = req[index - 1]
        ppifranked = 0
        ppaccifranked = 0
        if info.pp and info.mode.value == "osu":
          if not info.perfect and info.mode.value == 'osu':
            accfc = calc_acc(info.statistics.count_300 + info.statistics.count_geki + info.statistics.count_miss, info.statistics.count_100 + info.statistics.count_katu, info.statistics.count_50)
            #ppfc = pp.pp(l = f'https://osu.ppy.sh/osu/{info.beatmap.id}', c100 = info.statistics.count_100 + info.statistics.count_katu, c50 = info.statistics.count_50, mod_s = (str(info.mods)) if str(info.mods) != 'NM' else '', combo = osuapi.beatmap(beatmap_id = info.beatmap.id).max_combo)
            ppaccfc = pp.pp(l = f'https://osu.ppy.sh/osu/{info.beatmap.id}', acc = accfc, mod_s = (str(info.mods)) if str(info.mods) != 'NM' else '', combo = osuapi.beatmap(beatmap_id = info.beatmap.id).max_combo)
          if info.perfect and info.mode.value == 'osu' and round(info.accuracy * 100, 2) != 100.00:
            ppaccss = pp.pp(l = f'https://osu.ppy.sh/osu/{info.beatmap.id}', acc = 100.00, mod_s = (str(info.mods)) if str(info.mods) != 'NM' else '', combo = osuapi.beatmap(beatmap_id = info.beatmap.id).max_combo)
        elif not info.pp and info.mode.value == "osu":
          acc = calc_acc(info.statistics.count_300 + info.statistics.count_geki, info.statistics.count_100 + info.statistics.count_katu, info.statistics.count_50, info.statistics.count_miss)
          ppifranked = pp.pp(l = f'https://osu.ppy.sh/osu/{info.beatmap.id}', acc = acc, mod_s = (str(info.mods)) if str(info.mods) != 'NM' else '', combo = osuapi.beatmap(beatmap_id = info.beatmap.id).max_combo)
          ppaccifranked = pp.pp(l = f'https://osu.ppy.sh/osu/{info.beatmap.id}', c100 = info.statistics.count_100 + info.statistics.count_katu, c50 = info.statistics.count_50, misses = info.statistics.count_miss, mod_s = (str(info.mods)) if str(info.mods) != 'NM' else '', combo = osuapi.beatmap(beatmap_id = info.beatmap.id).max_combo)
        e = discord.Embed(url = f"https://osu.ppy.sh/b/{info.beatmap.id}", title = f"{info.beatmap.beatmapset().title} [{info.beatmap.version}] {('+' + str(info.mods) + ' ') if str(info.mods) != 'NM' else ''}[{info.beatmap.difficulty_rating}⭐]", description = f"> {ranks[info.rank.value]} - **`{'%.2f'%(info.pp) if info.pp else ppifranked}PP{('/' + str(ppaccifranked) + 'PP') if not ppifranked == ppaccifranked else ''}`**" + (" (If ranked) " if not info.pp else '') + (f"(`{ppaccfc}PP` for `{'%.2f'%(accfc)}%` FC)" if info.pp and info.mode.value == 'osu' and not info.perfect else "") + (f"(`{ppaccss}PP` for {ranks['X'] if str(info.mods) == 'NM' else ranks['XH']})" if info.pp and info.mode.value == 'osu' and info.perfect and round(info.accuracy * 100, 2) != 100 else "") + f" - **`{'%.2f'%(info.accuracy * 100)}%`**{' FC' if info.perfect else ''}\n> {info.score:,} - x{info.max_combo}/{osuapi.beatmap(beatmap_id = info.beatmap.id).max_combo} - [{info.statistics.count_300 + info.statistics.count_geki}/{info.statistics.count_100 + info.statistics.count_katu}/{info.statistics.count_50}/{info.statistics.count_miss}]" + f"\n\n<t:{int(time.mktime(info.created_at.timetuple())) + 10800}:R> on osu! Bancho", color = random.randint(0, 16667215))
        e.set_thumbnail(url = str(info.beatmap.beatmapset().covers.list_2x))
        e.set_footer(text = f"Beatmap ID: {info.beatmap.beatmapset_id} > {info.beatmap.id}")
        await inter.send(f"**Recent {info.mode.name.lower()}! score for [{esc_md(osuapi.user(user = user).username)}](https://osu.ppy.sh/users/{osuapi.user(user = user).id}):**", embed = e)
      else:
        e = discord.Embed(title = "Error", description = "This user does not have any recent scores...", color = random.randint(0, 16667215))
        await inter.send(embed = e, ephemeral = True)
    except ValueError:
      e = discord.Embed(title = "Error", description = "User not found", color = random.randint(0, 16667215))
      await inter.send(embed = e, ephemeral = True)
      
  @osu.sub_command()
  async def ppacc(self, inter, id: str, acc: float = 100.00, mods: str = "NM"):
    '''
    Calculate osu! PP using accuracy
    
    Parameters
    ----------
    id: Beatmap ID
    acc: Accuracy
    mods: Mods string (example: HDDT) 
    '''
    if acc > 100.00: acc = 100.00
    elif acc < 0.00: acc = 0.00
    try:
      info = osuapi.beatmap(beatmap_id = id)
      ppacc = pp.pp(l = f'https://osu.ppy.sh/osu/{id}', acc = acc, mod_s = (str(mods)) if str(mods) != 'NM' else '')
      e = discord.Embed(url = f"https://osu.ppy.sh/osu/{id}",title = f"PP calculation for: {info.beatmapset().title} [{info.version}] {('+' + str(mods).upper() + ' ') if str(mods).upper() != 'NM' else ''}[{info.difficulty_rating}⭐]", description = f"**`{ppacc}PP`** - `{acc}%`", color = random.randint(0, 16667215))
      await inter.send(embed = e)
    except ValueError:
      e = discord.Embed(title = "Error", description = "Beatmap not found", color = random.randint(0, 16667215))
      await inter.send(embed = e, ephemeral = True)
      
  @osu.sub_command()
  async def acc(self, inter, c300: int = 0, c100: int = 0, c50: int = 0, misses: int = 0):
    '''
    Calculate osu! accuracy using hitcircle scores
    
    Parameters
    ----------
    c300: Amount of 300's
    c100: Amount of 100's
    c50: Amount of 50's
    misses: Amount of misses
    ''' 
    if any([c300, c100, c50, misses]):
      result = calc_acc(c300, c100, c50, misses)
      e = discord.Embed(title = "Accuracy calculation", description = f"**`{result}%`** - [{c300}/{c100}/{c50}/{misses}]", color = random.randint(0, 16667215))
      await inter.send(embed = e)
    else:
      result = 100.00
      e = discord.Embed(title = "Accuracy calculation", description = f"**`{result}%`**", color = random.randint(0, 16667215))
      await inter.send(embed = e)
      
  #roblox group
  @commands.slash_command()
  async def roblox(self, inter):
    pass

  @roblox.sub_command()
  async def user(self, inter, username: str = commands.Param(autocomplete = suggest_rblxuser)):
    '''
    See users info by username
    
    Parameters
    ----------
    username: Name of a user
    '''
    
    try: 
      user = await crblx.get_user_by_username(username, expand = True)
      avatar = await crblx.thumbnails.get_user_avatar_thumbnails(users = [user], type = AvatarThumbnailType.headshot, size = (420, 420))
    except rblx.UserNotFound: 
      e = discord.Embed(title = "Error", description = "Invalid username", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
      
    e = discord.Embed(title = f"{(user.display_name + ' ' + f'(@{user.name})') if user.name != user.display_name else f'{user.name}'}'s profile:", color = random.randint(0, 16777215), url = f"https://www.roblox.com/users/{user.id}/profile")
    e.add_field(name = "Created at:", value = f"<t:{str(time.mktime(user.created.timetuple()))[:-2]}:R>", inline = False)
    if user.description:
      e.add_field(name = "Description:", value = user.description, inline = False)
    e.set_footer(text = f"ID: {user.id}")
    e.set_thumbnail(url = avatar[0].image_url)
    await inter.send(embed = e  )

  @roblox.sub_command()
  async def id(self, inter, userid: int):
    '''
    See users info by ID
    
    Parameters
    ----------
    userid: ID of a user
    '''
    
    try:
      user = await crblx.get_user(int(userid))
      avatar = await crblx.thumbnails.get_user_avatar_thumbnails(users = [user], type = AvatarThumbnailType.headshot, size = (420, 420))
    except rblx.UserNotFound:
      e = discord.Embed(title = "Error", description = "Invalid ID", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    
    e = discord.Embed(title = f"{(user.display_name + ' ' + f'(@{user.name})') if user.name != user.display_name else f'{user.name}'}'s profile:", color = random.randint(0, 16777215), url = f"https://www.roblox.com/users/{user.id}/profile")
    e.add_field(name = "Created at:", value = f"<t:{str(time.mktime(user.created.timetuple()))[:-2]}:R>", inline = False)
    if user.description:
      e.add_field(name = "Description:", value = user.description, inline = False)
    e.set_footer(text = f"ID: {user.id}")
    e.set_thumbnail(url = avatar[0].image_url)
    await inter.send(embed = e)

  @roblox.sub_command()
  async def group(self, inter, groupid):
    '''
    See groups info by ID
    
    Parameters
    ----------
    groupid: ID of a group
    '''
    
    try:
      group = await crblx.get_channelgroup(int(groupid))
      icon = await crblx.thumbnails.get_group_icons(groups = [group], size = (420, 420))
      
    except rblx.GroupNotFound:
      e = discord.Embed(title = "Error", description = "Invalid ID", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return

    e = discord.Embed(title = f"{group.name}'s Info:", color = random.randint(0, 16777215), url = f"https://www.roblox.com/groups/{group.id}/LSPLASH#!/about")
    e.add_field(name = f"Amount of members:", value = f"{group.member_count}", inline = False)
    e.add_field(name = "Owner:", value = f"{(group.owner.display_name + ' ' + f'(@{group.owner.name})') if group.owner.name != group.owner.display_name else f'{group.owner.name}'}", inline = False)
    if group.shout:
      e.add_field(name = "Shout:", value = f"{(group.shout.poster.display_name + ' ' + f'(@{group.shout.poster.name})') if group.shout.poster.name != group.shout.poster.display_name else f'{group.shout.poster.name}'}" + "\n" + f"> {group.shout.body}" + "\n" + f"> <t:{str(time.mktime(group.shout.updated.timetuple()))[:-2]}:R>")
    e.set_footer(text = f"ID: {group.id}")
    e.set_thumbnail(url = icon[0].image_url)
    await inter.send(embed = e)

  #channel group
  @commands.slash_command()
  async def channel(self, inter):
    pass

  @channel.sub_command()
  @commands.is_owner()
  async def link(self, inter, id):
    '''
    Creates a link with current channelimp and mentioned channel (ID)
    
    Parameters
    ----------
    id: Channel ID
    '''
    if inter.bot.get_channel(int(id)) is None or str(inter.channel.id) == id:
      e = discord.Embed(title = "Error", description = "Invalid channel id", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
      if str(inter.channel.id) not in db["linkchannels"]:
        db["linkchannels"][str(inter.channel.id)] = []
      if id not in db["linkchannels"]:
        db["linkchannels"][id] = []

      if str(inter.channel.id) not in db["linkchannels"][id] and id not in db["linkchannels"][str(inter.channel.id)]:
        db["linkchannels"][id].append(str(inter.channel.id))
        db["linkchannels"][str(inter.channel.id)].append(id)
        e = discord.Embed(title = "Success", description = f"Linked `{id}` and this channel", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)
      else:
        e = discord.Embed(title = "Error", description = "This channel is already linked with another channel", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)

  @channel.sub_command()
  @commands.is_owner()
  async def unlink(self, inter, id):
    '''
    Unlinks current channel and mentioned channel (ID)
    
    Parameters
    ----------
    id: Channel ID
    '''
    with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
      if id not in db["linkchannels"][str(inter.channel.id)] or str(inter.channel.id) not in db["linkchannels"][id]:
        e = discord.Embed(title = "Error", description = "Invalid channel id", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)
        return
      e = discord.Embed(title = "Successfully deleted", color = random.randint(0, 16777215))
      id2 = db["linkchannels"][str(inter.channel.id)]
      id1 = db["linkchannels"][id]
      if str(inter.channel.id) in id1:
        if len(id1) == 1:
          del db["linkchannels"][str(inter.channel.id)]
        else:
          del db["linkchannels"][str(inter.channel.id)][db["linkchannels"][str(inter.channel.id)].index(id)]
        e.add_field(name = f"{id} > {inter.channel.id}", value = "_ _", inline = False)
      if id in id2:
        if len(id2) == 1:
          del db["linkchannels"][id]
        else:
          del db["linkchannels"][id][db["linkchannels"][id].index(str(inter.channel.id))]
        e.add_field(name = f"{inter.channel.id} > {id}", value = "_ _", inline = False)
      await inter.send(embed = e, ephemeral = True)
      
  @commands.slash_command(name = "urban")
  async def slashurban(inter, query):
    '''
    See meaning of term you need
    Parameters
    ----------
    query: Your term here!
    '''
    try:
      url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
      querystring = {"term": query}
      headers = {
          'x-rapidapi-key': os.environ["URBANAPI"],
          'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
          }
      response = rq.request("GET", url, headers=headers, params=querystring)
      rjson = response.json()
      e = discord.Embed(title = f"Urban Dictionary Meaning for: {query}", url = rjson['list'][0]['permalink'], color = random.randint(0, 16777215))
      e.add_field(name = "Definition:", value = rjson['list'][0]['definition'], inline = False)
      e.add_field(name = "Example:", value = rjson['list'][0]['example'], inline = False)
      e.set_footer(text = f"👍: {rjson['list'][0]['thumbs_up']} / 👎: {rjson['list'][0]['thumbs_down']} | Author: {rjson['list'][0]['author']}")
      await inter.send(embed = e)
    except:
      e = discord.Embed(title = "Error", description = "Something went wrong...", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

  @commands.slash_command(name = "md")
  async def md(inter, *, ephemeral: Required1 = Required1.You, text):
    '''
    .md Format your message
    Parameters
    ----------
    ephemeral: Visibilty of embed
    text: Input text here, // for newline
    '''
    modtext = text.split("//")
    if modtext[0].strip().startswith("# "):
      title = modtext.pop(0)[2:]
    else:
      title = ".md format"
    if "\n".join(modtext).replace("- ", "• ").find("## ") == -1:
      desc = "\n".join(modtext).replace("- ", "• ")
    else:
      descindex = "\n".join(modtext).replace("- ", "• ").find("## ")
      desc = "\n".join(modtext).replace("- ", "• ")[:descindex]
    e = discord.Embed(title = title, description = desc, color = random.randint(0, 16777215))
    subheaders = "//".join(modtext).split("## ")
    indexsh = 1
    for item in modtext:
      if item.strip().startswith("## "):
        if "\n".join(subheaders[indexsh].split("//")[1:]).replace("- ", "• "):
          val = "\n".join(subheaders[indexsh].split("//")[1:]).replace("- ", "• ")
        else:
          val = "_ _"
        e.add_field(name = item[3:], value = val, inline = False)
        indexsh += 1
    await inter.send(embed = e, ephemeral = ephemeral)
    
  @commands.slash_command(name = "copy-person")
  @commands.bot_has_permissions(manage_webhooks = True)
  async def userecho(inter, member: discord.Member, *, content):
    '''
    Copy someone!
    Parameters
    ----------
    member: Mention a person to copy
    content: Input text here
    '''
    await inter.send(f"Successfully sent `{content}` as `{member}`", ephemeral = True) 
    channel_webhooks = await inter.channel.webhooks()
    webhook_count = 0

    for webhook in channel_webhooks:
        if webhook.user.id == inter.bot.user.id and webhook.name == "PythonBot Webhook":
            await webhook.send(
                content=content, username=member.display_name, avatar_url=member.avatar, allowed_mentions=discord.AllowedMentions.none()
            )
            return

    new_webhook = await inter.channel.create_webhook(name="PythonBot Webhook", reason="PythonBot webhook usage in commands")
    await new_webhook.send(content=content, username=member.display_name, avatar_url=member.avatar, allowed_mentions=discord.AllowedMentions.none())

  @commands.slash_command()
  async def react(self, inter, emoji:discord.Emoji, message:discord.Message):
    '''
    Let a Tupper add a Reaction

    Parameters
    ----------
    emoji: The Emoji to react with
    message:  The Message Url you want to react to
    '''
    await message.add_reaction(emoji)
    if isinstance(inter, discord.Message):
      sent = await inter.author.send('Reaction added!\nMake sure to add your own Reaction for it to stay')
    else:
      await inter.send('Reaction added!\nMake sure to add your own Reaction for it to stay', ephemeral=True)
      sent = inter.response
    try:
      await self.bot.wait_for('reaction_add', check=lambda react, user: react.message==message and user==inter.author, timeout=10)
      await message.remove_reaction(emoji, self.bot.user)
      await sent.delete()
      return
    except:
      await message.remove_reaction(emoji, self.bot.user)
      await sent.delete()

  #eval python command
  @commands.slash_command(name = "evalpy", description = "ONLY FOR PEOPLE THAT ARE IN WHITELIST. Execute python code and see results")
  @commands.check(lambda inter: inter.author.id in whitelist_id)
  async def evalpy(inter, *, ephemeral: Required1 = Required1.You, send_way: Required2 = Required2.Normal, code):
    '''
    Only for people that are in whitelist

    Parameters
    ----------
    ephemeral: Visibility of eval
    send_way: Available ways: Normal, Await
    code: Code here
    '''
    blacklist = ["time.sleep", "sleep", "open", "exec", "license", "help", "exit", "quit", "os", "eval", "reset_cooldown", "run", "clear", "unload_extension", "load_extension", "leave", "token", "http"]
    await inter.response.defer(ephemeral = ephemeral)
    try:
      if inter.author.id == inter.bot.owner.id:
        if send_way == "Normal":
          e = discord.Embed(title = "PyEval:", description = f"```py\n{code}\n```\nResult: ```\n{eval(code)}\n```", color = random.randint(0, 16777215)) 
          await inter.send(embed = e)
        elif send_way == "Await":
          e = discord.Embed(title = "Await PyEval:", description = f"```py\n{code}\n```", color = random.randint(0, 16777215))
          await inter.send(embed = e)
          await eval(code)
      else:
        if send_way == "Normal":
          if any(i in code for i in blacklist):
            e = discord.Embed(title = "Error", description = "```'NoneType' is not callable```", color = random.randint(0, 16777215))
            await inter.send(embed = e)
          else:
            e = discord.Embed(title = "PyEval:", description = f"```py\n{code}\n```\nResult:\n```\n{eval(code, {'__builtins__': __builtins__, '__import__': None, 'eval': None, 'random': random, 'inter': inter, 'int': int, 'str': str, 'len': len, 'time': time, 'datetime': datetime, 'mktime': time.mktime, 'math': math, 'quit': None, 'exit': None, 'help': None, 'license': None, 'exec': None, 'print': None, 'os': None, 'open': None, 'sleep': None, 'time.sleep': None, 'shuffle': lambda x: random.sample(x, len(x)), 'reset_cooldown': None, 'run': None, 'clear': None, 'unload_extension': None, 'load_extension': None, 'discord': discord})}\n```", color = random.randint(0, 16777215))
            await inter.send(embed = e)
        else:
          if any(i in code for i in blacklist):
            e = discord.Embed(title = "Error", description = "```'NoneType' is not callable```", color = random.randint(0, 16777215))
            await inter.send(embed = e)
          else:
            e = discord.Embed(title = "PyEval:", description = f"```py\n{code}\n```", color = random.randint(0, 16777215))
            await inter.send(embed = e)
            await eval(code, {'__builtins__': __builtins__, '__import__': None, 'eval': None, 'random': random, 'inter': inter, 'int': int, 'str': str, 'len': len, 'time': time, 'datetime': datetime, 'mktime': time.mktime, 'math': math, 'quit': None, 'exit': None, 'help': None, 'license': None, 'exec': None, 'print': None, 'os': None, 'open': None, 'sleep': None, 'time.sleep': None, 'shuffle': lambda x: random.sample(x, len(x)), 'reset_cooldown': None, 'run': None, 'clear': None, 'unload_extension': None, 'load_extension': None, 'discord': discord})
    except Exception as error:
      e = discord.Embed(title = "Error", description = f"```{error}```", color = random.randint(0, 16777215))
      await inter.send(embed = e)
    
  #eval brainfudge command
  @commands.slash_command(name = "execbf", description = "Execute brainfudge code and see results")
  async def evalbf(inter, *, ephemeral: Required1 = Required1.You, code):
    '''
    Execute brainfudge code and see the results

    Parameters
    ----------
    ephemeral: Visibility of eval
    code: Code here
    '''
    try:
      e = discord.Embed(title = "BFEval:", description = f"```bf\n{code}\n```\nResult: ```\n{runbf(code)}\n```", color = random.randint(0, 16777215)) 
      await inter.send(embed = e, ephemeral = ephemeral)
    except:
      e = discord.Embed(title = "Error", description = f"Something went wrong. Try again...", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
  
  #embed command
  @commands.slash_command(name = "embed")
  async def slashembed(inter, ephemeral: Required1, *, content = "", author_name = "", author_icon = "", title = "", desc = "", footer = "", footer_icon = "", color = random.randint(0, 16777215), thumbnail = "", image = ""):
    '''
    Makes an embed for you
    Parameters
    ----------
    ephemeral: Visibility of the embed, required
    content: Text outside embed, default is none
    author_name: Author name, default is your name
    author_icon: Author icon, default is your pfp
    title: Embed title, default is none
    desc: Embed Description, default is none
    footer: Embed footer, default is none
    footer_icon: Footer icon, default is none
    color: Embed color, default is random
    thumbnail: Embed thumbnail, default is none
    image: Embed image, default is none
    '''
    if author_icon == "":
      author_icon = str(inter.author.avatar)[:-10]
    if author_name == "":
      author_name = inter.author.name
    e = discord.Embed(title = title, description = desc, color = color)
    e.set_author(name = author_name, icon_url = author_icon)
    e.set_footer(text = footer, icon_url = footer_icon)
    e.set_thumbnail(url = thumbnail)
    e.set_image(url = image)
    await inter.send(content = content, embed = e, ephemeral = ephemeral)

  #test 2 (buttons message) command
  @commands.slash_command(name = "button", description = "test command 2")
  async def slashbutton(inter):
    await inter.send("button test lol", view = buttonthing(inter))
        
  #test 3 (select command) command
  @commands.slash_command(name = "menu", description = "test command 3")
  async def select(inter):
    view = menuView(inter.author)

    await inter.send("Select Menu", view = view)

  #send emoji command
  @commands.slash_command(name = "sendemoji", description = "Send emoji as bot")
  async def slashsendemoji(inter, emoji: discord.Emoji):
    '''
    Send emoji as bot

    Parameters
    ----------
    emoji: Emoji here
    '''
    await inter.response.send_message(emoji.url)

  #someone command
  @commands.slash_command(name = "someone", description = "Ping random person (Just like @someone back in 2018)")
  @commands.has_permissions(administrator = True)
  async def someone(inter):
    while True:
      member = random.choice(inter.guild.members)
      if member.bot:
        continue
      else:
        break
    await inter.send(member.mention)

  #qrcode group
  @commands.slash_command()
  async def qrcode(self, inter):
    pass

  #create
  @qrcode.sub_command()
  async def create(self, inter, content: str):
    '''
    Create a qrcode i guess

    Parameters
    ----------
    content: Qrcode will contain content written here
    '''
    await inter.send(f"https://api.qrserver.com/v1/create-qr-code/?data={content[0:899].replace(' ', '%20').replace('/', '%2F').replace(':', '%3A').replace('=', '%3D').replace('?', '%3F')}&qzone=2&size=350x350")
    
  #read
  @qrcode.sub_command()
  async def read(self, inter, qrcode: str):
    '''
    Read a qrcode i guess
    
    Parameters
    ----------
    qrcode: Qrcode here (MUST BE A LINK)
    '''
    await inter.response.defer()
    json = rq.get(f"http://api.qrserver.com/v1/read-qr-code/?fileurl={qrcode.replace(' ', '%20').replace('/', '%2F').replace(':', '%3A').replace('=', '%3D').replace('?', '%3F')}").json()
    await inter.edit_original_message(content = f"Contents: {json[0]['symbol'][0]['data']}")

  #tupper group
  @commands.slash_command()
  async def tupper(self, inter):
    with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
      if str(inter.author.id) not in db["tupper"]:
        db["tupper"][str(inter.author.id)] = {}

  #create tupper
  @tupper.sub_command()
  async def create(self, inter, name, avatar):
    '''
    Create a tupper!

    Parameters
    ----------
    name: Name for tupper
    avatar: Avatar for tupper (MUST BE A LINK)
    '''
    with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
      await inter.response.defer(ephemeral = True)
      if name not in db["tupper"][str(inter.author.id)]:
        db["tupper"][str(inter.author.id)].update({str(name): str(avatar)})
        e = discord.Embed(title = "Success", description = f"Tupper named: `{name}` is created!", color = random.randint(0, 16777215))
        e.set_image(url = avatar)
        await inter.send(embed = e)
      else:
        e = discord.Embed(title = "Error", description = f"Tupper named: `{name}` already exists!", color = random.randint(0, 16777215))
        await inter.send(embed = e)

  #use tupper
  @tupper.sub_command()
  @commands.bot_has_permissions(manage_webhooks = True)
  async def say(self, inter, *, tupper: str = commands.Param(autocomplete = suggest_tupper), content):
    '''
    Use tupper to say something!

    Parameters
    ----------
    tupper: Tupper you want to use
    content: Text here
    '''
    with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
      await inter.response.defer(ephemeral = True)
      if tupper in db["tupper"][str(inter.author.id)]:
        e = discord.Embed(title = "Success", description = f"Successfully sent `{content}` as `{tupper}`", color = random.randint(0, 16777215))
        await inter.send(embed = e)
        channel_webhooks = await inter.channel.webhooks()
        webhook_count = 0

        for webhook in channel_webhooks:
          if webhook.user.id == inter.bot.user.id and webhook.name == "PythonBot Webhook":
              await webhook.send(
                  content = content, username = tupper, avatar_url = db["tupper"][str(inter.author.id)].get(tupper), allowed_mentions=discord.AllowedMentions.none()
              )
              return

        new_webhook = await inter.channel.create_webhook(name="PythonBot Webhook", reason="PythonBot webhook usage in commands")
        await new_webhook.send(content = content, username = tupper, avatar_url = db["tupper"][str(inter.author.id)].get(tupper), allowed_mentions=discord.AllowedMentions.none())
      else:
        e = discord.Embed(title = "Error", description = f"Tupper named: `{tupper}` doesn't exist!", color = random.randint(0, 16777215))
        await inter.send(embed = e)

  #delete tupper
  @tupper.sub_command()
  async def delete(self, inter, tupper: str = commands.Param(autocomplete = suggest_tupper)):
    '''
    Delete existing tupper

    Parameters
    ----------
    tupper: Tupper you want to delete
    '''
    with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
      await inter.response.defer(ephemeral = True)
      if tupper in db["tupper"][str(inter.author.id)]:
        del db["tupper"][str(inter.author.id)][tupper]
        e = discord.Embed(title = "Success", description = f"Tupper named: `{tupper}` is deleted!", color = random.randint(0, 16777215))
        await inter.send(embed = e)
      else:
        e = discord.Embed(title = "Error", description = f"Tupper named: `{tupper}` doesn't exist!", color = random.randint(0, 16777215))
        await inter.send(embed = e)

  #edit tupper
  @tupper.sub_command()
  async def edit(self, inter, *, tupper: str = commands.Param(autocomplete = suggest_tupper), new_name, avatar):
    '''
    Edit a tupper!

    Parameters
    ----------
    tupper: Tupper you want to edit
    new_name: New name for tupper
    avatar: New avatar for tupper (MUST BE A LINK)
    '''
    with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
      if tupper in db["tupper"][str(inter.author.id)]:
        del db["tupper"][str(inter.author.id)][tupper]
        db["tupper"][str(inter.author.id)].update({str(new_name): str(avatar)})
        e = discord.Embed(title = "Success", description = f"Tupper's name: `{tupper}` is now edited to `{new_name}`!", color = random.randint(0, 16777215))
        e.set_image(url = avatar)
        await inter.send(embed = e, ephemeral = True)
      else:
        e = discord.Embed(title = "Error", description = f"Tupper named: `{tupper}` doesn't exist!", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)

  @commands.slash_command()
  async def screenshot(inter, site: str):
    '''
    Screenshot a website

    Parameters
    ----------
    site: Site URL
    '''
    if any([site.startswith("https://"), site.startswith("http://")]):
      e = discord.Embed(title = site, description = "If you don't see image then url doesn't work", color = random.randint(0, 16777215))
      e.set_image(popcat.screenshot(site))
      await inter.send(embed = e, ephemeral = True)
    else:
      e = discord.Embed(title = "Error", description = "Invalid URL", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

  @commands.slash_command()
  async def cc(self, inter):
    with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
      if str(inter.author.id) not in db["customcmd"]:
        db["customcmd"][str(inter.author.id)] = {}
                        
  @cc.sub_command()
  async def info(inter):
    '''
    Expression info here
    '''
    table = {"{author}": inter.author.name, "{author.mention}": f"<@{inter.author.id}>",
           "{server}": inter.guild.name, "{server.id}": str(inter.guild.id),
           "{channel}": inter.channel.name, "{channel.id}": str(inter.channel.id)}
    e = discord.Embed(title = "Expression info", description = '\n'.join((key + ': ' + value) for key, value in zip(table.keys(), table.values())), color = random.randint(0, 16777215))
    await inter.send(embed = e, ephemeral = True)

  @cc.sub_command()
  async def eval(inter, expr, ephemeral: Required1 = Required1.You):
    '''
    Eval Custom Command expressions

    Parameters
    ----------
    expr: Expressions here
    ephemeral: True or False
    '''
    e = discord.Embed(title = "CC Eval", description = f"this is ultra beta alpha version\n```{expr}```\nResults:\n{express(inter, expr)}", color = random.randint(0, 16777215))
    await inter.send(embed = e , ephemeral = ephemeral)

  @cc.sub_command()
  async def create(inter, cmd_name, expr):
    '''
    Create a Custom Command for yourself

    Parameters
    ----------
    cmd_name: Command name
    expr: Expressions here
    '''
    with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
      if cmd_name not in db["customcmd"][str(inter.author.id)]:
        db["customcmd"][str(inter.author.id)].update({cmd_name: expr})
        e = discord.Embed(title = "Successful", description = f"Successfully added `{cmd_name}`", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)
      else:
        e = discord.Embed(title = "Error", description = "A command with this name already exists", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)

  @cc.sub_command()
  async def use(inter, cmd_name: str = commands.Param(autocomplete = suggest_command)):
    '''
    Use an exising command

    Parameters
    ----------
    cmd_name: Command name
    '''
    with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
      if cmd_name in db["customcmd"][str(inter.author.id)]:
        await inter.send(express(inter, db["customcmd"][str(inter.author.id)][cmd_name]))
      else:
        e = discord.Embed(title = "Error", description = "This command doesn't exist", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)

  @cc.sub_command()
  async def delete(inter, cmd_name: str = commands.Param(autocomplete = suggest_command)):
    '''
    Delete an existing command

    Parameters
    ----------
    cmd_name: Command name
    '''
    with RedisManager(host = os.environ["REDISHOST"], port = os.environ["REDISPORT"], password = os.environ["REDISPASSWORD"], client_name = os.environ["REDISUSER"]) as db:
      if cmd_name in db["customcmd"][str(inter.author.id)]:
        db["customcmd"][str(inter.author.id)].pop(cmd_name)
        e = discord.Embed(title = "Successful", description = f"Successfully removed `{cmd_name}`", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)
      else:
        e = discord.Embed(title = "Error", description = "This command doesn't exist", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)
  
def setup(bot):
  bot.add_cog(Nonsense(bot))