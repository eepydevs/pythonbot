#cog by @maxy_dev (maxy#2866)
import disnake as discord
from disnake.ext import commands
from enum import Enum
import random
import asyncio
import os
from utils import db

item_info = {
	"Computer": "Usable: hack Command/False\nType: Item\nInfo: You can hack people's data on this",
	"Laptop": "Usable: postmeme Command/False\nType: Item\nInfo: You can post memes on this",
  "Golden coin": "Usable: False\nType: Collection\nInfo: Just buy a ton of those coins and flex to your friends",
	"Discount card": "Usable: False\nType: Item\nInfo: Gives 25% sale on every item in the shop!",
	"Smartphone": "Usable: mail Command/False\nType: Item\nInfo: You can mail someone with this",
	"Lottery": "Usable: True\nType: Item\nInfo: Gives random amount of cash... Sometimes huge amount of cash"
}

if "balance" not in db:
  db["balance"] = {}

if "passive" not in db:
  db["passive"] = {}

if "shop" not in db:
  db["shop"] = {
    "Discount card": 20000,
    "Computer": 6500,
    "Golden coin": 5000,
    "Laptop": 2000,
    "Smartphone": 500,
    "Lottery": 100
  }

if "inventory" not in db:
  db["inventory"] = {}

def iteminfo(name):
  if name in item_info:
    return item_info[name]
  return "No info"

async def suggest_buyitem(inter, input):
  return [item for item in list(db['shop'].keys()) if input.lower() in item.lower()][0:24]

async def suggest_item(inter, input):
  return [item for item in list(db['inventory'][str(inter.author.id)].keys()) if input.lower() in item.lower()][0:24] if db['inventory'][str(inter.author.id)] and [item for item in list(db['inventory'][str(inter.author.id)].keys()) if input.lower() in item.lower()][0:24] else ["You have nothing!"]

async def suggest_usableitem(inter, input):
  return [item for item in list(db['inventory'][str(inter.author.id)].keys()) if input.lower() in item.lower() and item.lower() in ["lottery"]][0:24] if db['inventory'][str(inter.author.id)] and [item for item in list(db['inventory'][str(inter.author.id)].keys()) if input.lower() in item.lower() and item.lower() in ["lottery"]][0:24] else ["You have nothing to use!"]
  
def lottery():
  win = None
  while True:
    chance = random.randint(0, 100)
    if 25 <= chance <= 50:
      win = random.randint(5, 50)
    elif chance >= 25:
      win = random.randint(25, 125)

    else:
      continue
    break
  return win

class lbbuttons(discord.ui.View):
  def __init__(self, inter: discord.Interaction, color, lb):
    super().__init__(timeout = 60)
    self.inter = inter
    self.page = 0
    self.color = color
    self.leaderboard = lb
    
  async def interaction_check(self, inter: discord.MessageInteraction):
    if inter.author != self.inter.author:
      await inter.send("Those buttons are not for you", ephemeral = True)
      return False
    return True

  '''@discord.ui.button(label = "Primary", custom_id = "Primary", emoji = "1️⃣", style = discord.ButtonStyle.blurple)
  async def primary_button(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
    await interaction.send("You clicked Primary", ephemeral = True)'''

  @discord.ui.button(label = "", custom_id = "-10", emoji = "⬅️")
  async def arrowleft(self, button: discord.ui.Button, interaction = discord.MessageInteraction):
    self.page += int(interaction.data.custom_id)
    self.page = min(max(self.page, 0), len(self.leaderboard) // 10 * 10)
    e = discord.Embed(
      title = "Leaderboard",
      description = "\n".join(self.leaderboard[self.page:self.page + 10]),
      color = self.color
    )
    if str(interaction.author.id) in db["debug"]:
      e.add_field(name = "Debug", value = f"Variables value:\n{self.page}")
    await interaction.response.edit_message(embed = e)

  @discord.ui.button(label = "", custom_id = "10", emoji = "➡️")
  async def arrowright(self, button: discord.ui.Button, interaction = discord.MessageInteraction):
    self.page += int(interaction.data.custom_id)
    self.page = min(max(self.page, 0), len(self.leaderboard) // 10 * 10)
    e = discord.Embed(
      title = "Leaderboard",
      description = "\n".join(self.leaderboard[self.page:self.page + 10]),
      color = self.color
    )
    if str(interaction.author.id) in db["debug"]:
      e.add_field(name = "Debug", value = f"Variables value:\n{self.page}")
    await interaction.response.edit_message(embed = e)

class menusearch(discord.ui.Select):
  def __init__(self, inter: discord.Interaction):
    self.inter = inter
    places = ["Car", "Forest", "House", "Grass", "Bushes", "Pocket", "Space", "Discord", "Castle", "Basement", "Street", "Backpack", "Drawer", "Closet", "Couch"]
    p1 = places.pop(random.randint(0, int(len(places) - 1)))
    p2 = places.pop(random.randint(0, int(len(places) - 1)))
    p3 = places.pop(random.randint(0, int(len(places) - 1)))
    options = [
      discord.SelectOption(label = p1, emoji = "1️⃣", value = p1),
      discord.SelectOption(label = p2, emoji = "2️⃣", value = p2),
      discord.SelectOption(label = p3, emoji = "3️⃣", value = p3)
    ]

    super().__init__(
      placeholder="Select a place",
      min_values=1,
      max_values=1,
      options=options
    )
  async def interaction_check(self, inter: discord.MessageInteraction):
        if inter.author != self.inter.author:
            await inter.send("This selection menu is not for you", ephemeral = True)
            return False
        return True
    
  async def callback(self, inter: discord.MessageInteraction):
    if str(inter.author.id) in db["balance"]:
      chance = random.randint(0, 100)
      if chance > 25:
        rng = random.randint(100, 500)
        db["balance"][str(inter.author.id)] += rng
        e = discord.Embed(title = f"{inter.author.name} searched: {self.values[0]}", description = f"You got {rng} 💵 !", color = random.randint(0, 16777215))
        if str(inter.author.id) in db["debug"]:
          e.add_field(name = "Debug", value = f"Variables value:\n{rng}, {db['balance'][str(inter.author.id)]}, {self.values[0]}")
        await inter.response.edit_message(embed = e, view = None)
        return
      else:
        e = discord.Embed(title = f"{inter.author.name} searched: {self.values[0]}", description = f"You failed...", color = random.randint(0, 16777215))
        if str(inter.author.id) in db["debug"]:
          e.add_field(name = "Debug", value = f"Variables value:\n{db['balance'][str(inter.author.id)]}")
        await inter.response.edit_message(embed = e, view = None)
        return
    else:
      db["balance"][str(inter.author.id)] = 0
      rng = random.randint(100, 500)
      db["balance"][str(inter.author.id)] += rng
      e = discord.Embed(title = f"{inter.author.name} searched: {self.values[0]}", description = f"You got {rng} 💵 !", color = random.randint(0, 16777215))
      if str(inter.author.id) in db["debug"]:
        e.add_field(name = "Debug", value = f"Variables value:\n{rng}, {db['balance'][str(inter.author.id)]}, {self.values[0]}")
      await inter.response.edit_message(embed = e, view = None)
      return

class searchview(discord.ui.View):
  def __init__(self, inter: discord.Interaction):
      super().__init__(timeout = 30)
      self.add_item(menusearch(inter))

class menupm(discord.ui.Select):
  def __init__(self, inter: discord.Interaction):
    self.inter = inter
    options = [
      discord.SelectOption(label = "Fresh", emoji = "🍋", value = "Fresh"),
      discord.SelectOption(label = "Repost", emoji = "🔁", value = "Repost"),
      discord.SelectOption(label = "Intellectual", emoji = "🧠", value = "Intellectual"),
      discord.SelectOption(label = "Copypasta", emoji = "📄", value = "Copypasta"),
      discord.SelectOption(label = "Kind", emoji = "😄", value = "Kind")
    ]

    super().__init__(
      placeholder="Select an option",
      min_values=1,
      max_values=1,
      options=options
    )
  async def interaction_check(self, inter: discord.MessageInteraction):
        if inter.author != self.inter.author:
            await inter.send("This selection menu is not for you", ephemeral = True)
            return False
        return True
    
  async def callback(self, inter: discord.MessageInteraction):
    chance = random.randint(0, 100)
    if chance > 45:
      rng = random.randint(250, 1000)
      db["balance"][str(inter.author.id)] += rng
      e = discord.Embed(title = f"{inter.author.name} posted: {self.values[0]}", description = f"You got {rng} 💵 !", color = random.randint(0, 16777215))
      if str(inter.author.id) in db["debug"]:
        e.add_field(name = "Debug", value = f"Variables value:\n{rng}, {db['balance'][str(inter.author.id)]}, {self.values[0]}")
      await inter.response.edit_message(embed = e, view = None)
      return
    else:
      e = discord.Embed(title = f"{inter.author.name} posted: {self.values[0]}", description = f"You failed...", color = random.randint(0, 16777215))
      await inter.response.edit_message(embed = e, view = None)
      return

class pmview(discord.ui.View):
  def __init__(self, inter: discord.Interaction):
      super().__init__(timeout = 30)
      self.add_item(menupm(inter))

class Economy(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  #item group
  @commands.slash_command()
  async def item(self, inter):
    if str(inter.author.id) not in db["inventory"]:
      db["inventory"][str(inter.author.id)] = {}
      
  #use sub command
  @item.sub_command()
  async def use(self, inter, itemname: str = commands.Param(autocomplete = suggest_usableitem)):
    '''
    Use an item with this command
    
    Parameters
    ----------
    itemname: Item name
    '''
    item = itemname.lower().capitalize()
    if item in db["inventory"][str(inter.author.id)]:
      if item == "Lottery":
        win = lottery()
        if db["inventory"][str(inter.author.id)].get(item) >= 2:
          updateinv = db["inventory"][str(inter.author.id)]
          updateinv[item] -= 1
          db["inventory"][str(inter.author.id)] = updateinv
          e = discord.Embed(title = f"You won {win} 💵!", description = "congratulations i guess...", color = random.randint(0, 16777215))
          db["balance"][str(inter.author.id)] += win
          await inter.send(embed = e)
        else:
          updateinv = db["inventory"][str(inter.author.id)]
          updateinv.pop(item)
          db["inventory"][str(inter.author.id)] = updateinv
          e = discord.Embed(title = f"You won {win} 💵!", description = "congratulations i guess...", color = random.randint(0, 16777215))
          db["balance"][str(inter.author.id)] += win
          await inter.send(embed = e)
      else:
        e = discord.Embed(title = "Error", description = f"Item `{itemname}` can't be used", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)
    else:
      e = discord.Embed(title = "Error", description = f"You don't have `{itemname}` in your inventory...", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

  #info sub command
  @item.sub_command()
  async def info(self, inter, itemname: str = commands.Param(autocomplete = suggest_item)):
    '''
    See info about items you have with this command
    
    Parameters
    ----------
    itemname: Item name
    '''
    item = itemname.lower().capitalize()
    if item in db["inventory"][str(inter.author.id)]:
      e = discord.Embed(title = f"Item: {item}", description = f"{iteminfo(item)}", color = random.randint(0, 16777215))
      await inter.send(embed = e)
    else:
      e = discord.Embed(title = "Error", description = f"You don't have `{itemname}` in your inventory...", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      
  #balance command
  @commands.slash_command(name = "balance", description = "Look how much cash you have")
  async def slashbalance(inter, member: discord.Member = None):
    '''
    Look how much cash you have

    Parameters
    ----------
    member: Mention member
    '''
    if member is None:
      if not str(inter.author.id) in db["balance"]:
        upd = db["balance"]
        upd[str(inter.author.id)] = 0
        db["balance"] = upd
        e = discord.Embed(title = f"@{inter.author.name}'s Balance", description = f"Wallet: {db['balance'][str(inter.author.id)]} 💵", color = random.randint(0, 16777215))
        await inter.send(embed = e)
      else:
        wallet = db["balance"][str(inter.author.id)]
        e = discord.Embed(title = f"@{inter.author.name}'s Balance", description = f"Wallet: {wallet} 💵", color = random.randint(0, 16777215))
        await inter.send(embed = e)
    else:
      if not str(member.id) in db["balance"]:
        db["balance"][str(member.id)] = 0
        wallet = db["balance"][str(member.id)]
        e = discord.Embed(title = f"@{member.name}'s Balance", description = f"Wallet: {wallet} 💵", color = random.randint(0, 16777215))
        await inter.send(embed = e)
      else:
        wallet = db["balance"][str(member.id)]
        e = discord.Embed(title = f"@{member.name}'s Balance", description = f"Wallet: {wallet} 💵", color = random.randint(0, 16777215))
        await inter.send(embed = e)

  #beg command
  @commands.slash_command(name = "beg", description = "Beg people to them give you nothing lol. Has cooldown of 10 seconds")
  @commands.cooldown(rate = 1, per = 10, type = commands.BucketType.user)
  async def slashbeg(inter):
    if str(inter.author.id) not in db["balance"]:
      db["balance"][str(inter.author.id)] = 0
      if random.randint(0, 100) < 35:
        e = discord.Embed(title = "Fail", description = "You failed!", color = random.randint(0 , 16777215))
        if str(inter.author.id) in db["debug"]:
          e.add_field(name = "Debug", value = f"Variables value:\n{db['balance'][str(inter.author.id)]}")
        await inter.send(embed = e)
      else:
        rng = random.randint(50, 150)
        db["balance"][str(inter.author.id)] += rng
        e = discord.Embed(title = "Success", description = f"You got {rng} 💵 !", color = random.randint(0, 16777215))
        if str(inter.author.id) in db["debug"]:
          e.add_field(name = "Debug", value = f"Variables value:\n{rng}, {db['balance'][str(inter.author.id)]}")
        await inter.send(embed = e)
    else:
      if random.randint(0, 100) < 35:
        e = discord.Embed(title = "Fail", description = "You failed!", color = random.randint(0, 16777215))
        if str(inter.author.id) in db["debug"]:
          e.add_field(name = "Debug", value = f"Variables value:\n{db['balance'][str(inter.author.id)]}")
        await inter.send(embed = e)
      else:
        rng = random.randint(50, 150)
        db["balance"][str(inter.author.id)] += rng
        e = discord.Embed(title = "Success", description = f"You got {rng} 💵 !", color = random.randint(0, 16777215))
        if str(inter.author.id) in db["debug"]:
          e.add_field(name = "Debug", value = f"Variables value:\n{rng}, {db['balance'][str(inter.author.id)]}")
        await inter.send(embed = e)

  #work command
  @commands.slash_command(name = "work", description = "Work to get some cash. Has cooldown of 30 minutes")
  @commands.cooldown(rate = 1, per = 60 * 30, type = commands.BucketType.user)
  async def slashwork(inter):
    if str(inter.author.id) in db["balance"]:
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
        e.add_field(name = "Debug", value = f"Variables value:\n{db['balance'][str(inter.author.id)]}, {answer}")
      await inter.send(embed = e)
      try:
        message = await inter.bot.wait_for("message", check = lambda message: message.author == inter.author and message.channel == inter.channel, timeout = 60)
        if int(message.content) == answer:
          rng = random.randint(250, 1000)
          db["balance"][str(inter.author.id)] += rng
          e = discord.Embed(title = "Success", description = f"You got {rng} 💵 !", color = random.randint(0, 1677215))
          if str(inter.author.id) in db["debug"]:
            e.add_field(name = "Debug", value = f"Variables value:\n{rng}, {db['balance'][str(inter.author.id)]}")
          await inter.send(embed = e)
        else:
          rng = random.randint(50, 250)
          db["balance"][str(inter.author.id)] += rng
          e = discord.Embed(title = "Failed", description = f"You got {rng} 💵 !", color = random.randint(0, 1677215))
          e.set_footer(text = f"The right answer was {answer}")
          if str(inter.author.id) in db["debug"]:
            e.add_field(name = "Debug", value = f"Variables value:\n{rng}, {db['balance'][str(inter.author.id)]}")
          await inter.send(embed = e)
      except asyncio.TimeoutError:
        rng = random.randint(50, 250)
        db["balance"][str(inter.author.id)] += rng
        e = discord.Embed(title = "Failed", description = f"You got {rng} 💵 !", color = random.randint(0, 1677215))
        e.set_footer(text = f"The right answer was {answer}")
        if str(inter.author.id) in db["debug"]:
          e.add_field(name = "Debug", value = f"Variables value:\n{rng}, {db['balance'][str(inter.author.id)]}")
        await inter.send(embed = e)
      except ValueError:
        rng = random.randint(50, 250)
        db["balance"][str(inter.author.id)] += rng
        e = discord.Embed(title = "Failed", description = f"You got {rng} 💵 !", color = random.randint(0, 1677215))
        e.set_footer(text = f"The right answer was {answer}")
        if str(inter.author.id) in db["debug"]:
          e.add_field(name = "Debug", value = f"Variables value:\n{rng}, {db['balance'][str(inter.author.id)]}")
        await inter.send(embed = e)
    else:
      db["balance"][str(inter.author.id)] = 0
      rng = random.randint(250, 1000)
      db["balance"][str(inter.author.id)] += rng
      e = discord.Embed(title = "Success", description = f"You got {rng} 💵 !", color = random.randint(0, 16777215))
      if str(inter.author.id) in db["debug"]:
        e.add_field(name = "Debug", value = f"Variables value:\n{rng}, {db['balance'][str(inter.author.id)]}")
      await inter.send(embed = e)

  #give command
  @commands.slash_command(name = "give", description = "Share some money with mentioned member")
  @commands.guild_only()
  async def slashgive(inter, member: discord.Member, payment: int):
    '''
    Share some money with mentioned member

    Parameters
    ----------
    member: Mention member
    payment: Amount of cash
    '''
    if str(inter.author.id) in db["balance"]:
      money = db["balance"][str(inter.author.id)]
      if member.id != inter.author.id:
        if payment <= money:
          if payment >= 1:
            if str(inter.author.id) not in db["passive"]:
              if str(member.id) not in db["passive"]:
                if str(member.id) in db["balance"]:
                  db["balance"][str(inter.author.id)] -= payment
                  db["balance"][str(member.id)] += payment
                  e = discord.Embed(title = "Success", description = f"@{member.name} got {payment} 💵 !", color = random.randint(0, 16777215))
                  if str(inter.author.id) in db["debug"]:
                    e.add_field(name = "Debug", value = f"Variables value:\n{db['balance'][str(inter.author.id)]}, {db['balance'][str(member.id)]}")
                  await inter.send(embed = e)
                else:
                  db["balance"][str(member.id)] = 0
                  db["balance"][str(inter.author.id)] -= payment
                  db["balance"][str(member.id)] += payment
                  e = discord.Embed(title = "Success", description = f"@{member.name} got {payment} 💵 !", color = random.randint(0, 16777215))
                  if str(inter.author.id) in db["debug"]:
                    e.add_field(name = "Debug", value = f"Variables value:\n{db['balance'][str(inter.author.id)]}, {db['balance'][str(member.id)]}")
                  await inter.send(embed = e)
              else:
                e = discord.Embed(title = "Error", description = "Leave peaceful person alone!", color = random.randint(0, 16777215))
                await inter.send(embed = e, ephemeral = True)
            else:
              e = discord.Embed(title = "Error", description = "You can't give money in passive mode!", color = random.randint(0, 16777215))
              await inter.send(embed = e, ephemeral = True)
          else:
            e = discord.Embed(title = "Error", description = "You can't give negative amount of money (aka take them)", color = random.randint(0, 16777215))
            await inter.send(embed = e, ephemeral = True)
        else:
          e = discord.Embed(title = "Error", description = "You can't give more than you have!", color = random.randint(0, 16777215))
          await inter.send(embed = e, ephemeral = True)
      else:
        e = discord.Embed(title = "Error", description = "You can't give cash to yourself", color = random.randint(0, 1677215))
        await inter.send(embed = e, ephemeral = True)
    else:
      db["balance"][str(inter.author.id)] = 0
      e = discord.Embed(title = "Error", description = "You have 0 💵", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
  
  #gamble command
  @commands.slash_command(name = "gamble", description = "Lose every dollar you have lol")
  async def gamble(inter, payment: int):
    '''
    Lose every dollar you have lol

    Parameters
    ----------
    payment: Amount of cash
    '''
    rng = random.randint(0, 12)
    dice = random.randint(0, 12)
    if str(inter.author.id) in db["balance"]:
      money = db["balance"][str(inter.author.id)]
      if payment <= money:
        if payment >= 1:
          if rng < dice:
            db["balance"][str(inter.author.id)] += payment
            e = discord.Embed(title = "You win", description = f"You got {payment} 💵 !", color = random.randint(0, 16777215))
            e.set_footer(text = f"You won: {dice} to {rng}")
            await inter.send(embed = e)
          elif rng == dice:
            e = discord.Embed(title = "Tie", description = "You didn't lose or win anything", color = random.randint(0 , 16777215))
            e.set_footer(text = f"Tie: {dice} to {rng}")
            await inter.send(embed = e)
          else:
            db["balance"][str(inter.author.id)] -= payment
            e = discord.Embed(title = "You lose", description = f"You lost {payment} 💵 !", color = random.randint(0, 16777215))
            e.set_footer(text = f"You lost: {dice} to {rng}")
            await inter.send(embed = e)
        else:
          e = discord.Embed(title = "Error", description = "You can't put negative amount of money on gamble", color = random.randint(0, 16777215))
          await inter.send(embed = e, ephemeral = True)
      else:
        e = discord.Embed(title = "Error", description = "You can't put more than you have cash on gamble", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)
    else:
      e = discord.Embed(title = "Error", description = "Go get some money first!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

  #daily commmand
  @commands.slash_command(name = "daily", description = "Get 1000 cash per day")
  @commands.cooldown(rate = 1, per = 86400, type = commands.BucketType.user)
  async def slashdaily(inter):
    if str(inter.author.id) in db["balance"]:
      db["balance"][str(inter.author.id)] += 1000
    else:
      db["balance"][str(inter.author.id)] = 0
      db["balance"][str(inter.author.id)] += 1000
    e = discord.Embed(title = "Daily", description = "You got 1000 💵 !", color = random.randint(0, 16777215))
    await inter.send(embed = e)

  #leaderboard command
  @commands.slash_command(description = "See other rich people in leaderboard")
  @commands.guild_only()
  async def leaderboard(self, inter):
    leaderboard = tuple(f"{index}. `@{member.name}`: {amount} 💵" for index, (member, amount) in enumerate(sorted(filter(lambda i: i[0] != None, ((inter.guild.get_member(int(i[0])), i[1]) for i in db["balance"].items())), key = lambda i: i[1], reverse = True), start = 1))
    color = random.randint(0, 16777215)
    e = discord.Embed(title = "Leaderboard", description = "\n".join(leaderboard[0:9]), color = color)
    await inter.send(embed = e, view = lbbuttons(inter, color, leaderboard))
  
  #global leaderboard command
  @commands.slash_command(description = "See other rich people in leaderboard")
  @commands.guild_only()
  async def globalleaderboard(self, inter):
    leaderboard = tuple(f"{index}. `@{user.name}`: {amount} 💵" for index, (user, amount) in enumerate(sorted(filter(lambda i: i[0] != None, ((inter.bot.get_user(int(i[0])), i[1]) for i in db["balance"].items())), key = lambda i: i[1], reverse = True), start = 1))
    color = random.randint(0, 16777215)
    e = discord.Embed(title = "Leaderboard", description = "\n".join(leaderboard[0:9]), color = color)
    await inter.send(embed = e, view = lbbuttons(inter, color, leaderboard))

  #rob command
  @commands.slash_command(name = "rob", description = "Get jailed, Has cooldown of 30 seconds")
  @commands.cooldown(rate = 1, per = 30, type = commands.BucketType.user)
  async def slashrob(inter, member: discord.Member):
    '''
    Get jailed, Has cooldown of 30 seconds

    Parameters
    ----------
    member: Mention member
    '''
    if member.id != inter.author.id:
      if str(member.id) in db["balance"]:
        if db["balance"][str(member.id)] != 0 and db["balance"][str(member.id)] > 150:
          if str(inter.author.id) not in db["passive"]:
            if str(member.id) not in db["passive"]:
              if str(inter.author.id) in db["balance"]:
                chance = random.randint(0, 100)
                if chance < 50:
                  try:
                    max = db["balance"][str(member.id)]
                    rng = random.randint(100, max)
                    db["balance"][str(member.id)] -= rng
                    db["balance"][str(inter.author.id)] += rng
                    e = discord.Embed(title = "Success", description = f"You stole {rng} 💵 from @{member.name}!", color = random.randint(0, 16777215))
                    await inter.send(embed = e)
                  except ValueError:
                    e = discord.Embed(title = "Error", description = "This person is too poor to be robbed!", color = random.randint(0, 16777215))
                    await inter.send(embed = e)
                else:
                  rng = random.randint(250, 1000)
                  db["balance"][str(member.id)] += rng
                  db["balance"][str(inter.author.id)] -= rng
                  e = discord.Embed(title = "Fail", description = f"You got caught and lost {rng} 💵 !", color = random.randint(0, 16777215))
                  await inter.send(embed = e)
              else:
                chance = random.randint(0, 100)
                if chance < 50:
                  try:
                    db["balance"][str(inter.author.id)] = 0
                    max = db["balance"][str(member.id)]
                    rng = random.randint(100, max)
                    db["balance"][str(member.id)] -= rng
                    db["balance"][str(inter.author.id)] += rng
                    e = discord.Embed(title = "Success", description = f"You stole {rng} 💵 from {member.name}!", color = random.randint(0, 16777215))
                    await inter.send(embed = e)
                  except ValueError:
                    e = discord.Embed(title = "Error", description = "This person is too poor to be robbed!", color = random.randint(0, 16777215))
                    await inter.send(embed = e)
                else:
                  db["balance"][str(inter.author.id)] = 0
                  rng = random.randint(250, 1000)
                  db["balance"][str(member.id)] += rng
                  db["balance"][str(inter.author.id)] -= rng
                  e = discord.Embed(title = "Fail", description = f"You got caught and lost {rng} 💵 !", color = random.randint(0, 16777215))
                  await inter.send(embed = e)
            else:
              e = discord.Embed(title = "Error", description = "Leave peaceful person alone!", color = random.randint(0, 16777215))
              await inter.send(embed = e, ephemeral = True)
          else:
            e = discord.Embed(title = "Error", description = "You can't rob people in passive mode!", color = random.randint(0, 16777215))
            await inter.send(embed = e, ephemeral = True)
        else:
          e = discord.Embed(title = "Error", description = "The person doesn't have any money!", color = random.randint(0, 16777215))
          await inter.send(embed = e, ephemeral = True)
      else:
        e = discord.Embed(title = "Error", description = "The person doesn't have any money!", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)
    else:
      e = discord.Embed(title = "Error", description = "You can't rob yourself!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
        

  #passive setting command
  @commands.slash_command(name = "passive", description = "For people who don't want to get robbed, Has cooldown of 30 minutes")
  @commands.cooldown(rate = 1, per = 1800, type = commands.BucketType.user)
  async def slashpassive(inter):
    if str(inter.author.id) in db["passive"] and db["passive"][str(inter.author.id)]:
      db["passive"][str(inter.author.id)] = None
      e = discord.Embed(title = "Success", description = "Youre now a normal person", color = random.randint(0, 16777215))
      await inter.send(embed = e)
    else:
      db["passive"][str(inter.author.id)] = True
      e = discord.Embed(title = "Success", description = "Youre now a passive person!", color = random.randint(0, 16777215))
      await inter.send(embed = e)

  #search command
  @commands.slash_command(description = "Just find something already, Has cooldown of 30 seconds")
  @commands.cooldown(rate = 1, per = 30, type = commands.BucketType.user)
  async def search(self, inter):
    e = discord.Embed(title = "Search", description = "Search one of places below to get some cash!", color = random.randint(0, 16777215))
    await inter.send(embed = e, view = searchview(inter))

  #shop group
  @commands.slash_command()
  async def shop(self, inter):
    if str(inter.author.id) not in db["inventory"]:
      db["inventory"][str(inter.author.id)] = {}
      
  #items sub command
  @shop.sub_command()
  async def items(inter):
    '''
    See prices of items here
    '''
    if str(inter.author.id) not in db["inventory"]:
      db["inventory"][str(inter.author.id)] = {}
    shop = '\n'.join(f'`{i+1}.` {item}: {price if "Discount card" not in db["inventory"][str(inter.author.id)] else int(price * 0.75)}' for i, (price,item) in enumerate(sorted(((price,item) for item,price in db['shop'].items()),reverse=True)))
    e = discord.Embed(title = "Shop", description = shop, color = random.randint(0, 16777215))
    await inter.send(embed = e)

  #buy sub command
  @shop.sub_command()
  async def buy(inter, item_name: str = commands.Param(autocomplete = suggest_buyitem), quantity: int = 1):
      '''
      Buy a thing in shop
  
      Parameters
      ----------
      item_name: Item name here
      quantity: Self-explanatory
      '''
      modtext = item_name.lower()
      itemname = modtext.capitalize()
      if quantity > 0:
        if itemname in db["shop"]:
          if str(inter.author.id) in db["balance"]:
            if db["shop"].get(itemname) * quantity < db["balance"][str(inter.author.id)] or int(db["shop"].get(itemname) * 0.75) * quantity < db["balance"][str(inter.author.id)]:
              if str(inter.author.id) in db["inventory"]:
                if itemname not in db["inventory"][str(inter.author.id)]:
                  if "Discount card" in db["inventory"][str(inter.author.id)]:
                    db["balance"][str(inter.author.id)] -= int(db["shop"].get(itemname) * 0.75) * quantity
                  else:
                    db["balance"][str(inter.author.id)] -= db["shop"].get(itemname) * quantity
                  updateinv = db["inventory"][str(inter.author.id)]
                  updateinv[itemname] = quantity
                  db["inventory"][str(inter.author.id)] = updateinv
                  e = discord.Embed(title = "Shop", description = f"You got {quantity} {itemname}'s!", color = random.randint(0, 16777215))
                  await inter.send(embed = e)
                else:
                  if "Discount card" in db["inventory"][str(inter.author.id)]:
                    db["balance"][str(inter.author.id)] -= int(db["shop"].get(itemname) * 0.75) * quantity
                  else:
                    db["balance"][str(inter.author.id)] -= db["shop"].get(itemname) * quantity
                  updateinv = db["inventory"][str(inter.author.id)]
                  updateinv[itemname] += quantity
                  db["inventory"][str(inter.author.id)] = updateinv
                  itemammount = db["inventory"][str(inter.author.id)].get(itemname)
                  e = discord.Embed(title = "Shop", description = f"You got {quantity} {itemname}'s!", color = random.randint(0, 16777215))
                  e.set_footer(text = f"Now you have {itemammount} {itemname}'s")
                  await inter.send(embed = e)
              else:
                db["inventory"][str(inter.author.id)] = {}
                db["balance"][str(inter.author.id)] -= db["shop"].get(itemname) * quantity
                updateinv = db["inventory"][str(inter.author.id)]
                updateinv[itemname] = quantity
                db["inventory"][str(inter.author.id)] = updateinv
                e = discord.Embed(title = "Shop", description = f"You got {itemname}!", color = random.randint(0, 16777215))
                await inter.send(embed = e)
            else:
              await inter.send(content = "Error: You have not enough money", ephemeral = True)
          else:
            db["balance"][str(inter.author.id)] = 0
            await inter.send(content = "Error: Get some money first!", ephemeral = True)
        else:
          await inter.send(content = "Error: You can't buy nothing!", ephemeral = True)
      else:
        await inter.send(content = "Error: You can't buy 0 or less items!", ephemeral = True)

  #sell sub command
  @shop.sub_command()
  async def sell(inter, itemname: str = commands.Param(autocomplete = suggest_item), quantity: int = 1):
    '''
    Sell any item you have
  
    Parameters
    ----------
    itemname: Item name here
    '''
    if quantity > 0:
      if quantity <= db["inventory"][str(inter.author.id)].get(itemname):
        if itemname != None:
          modtext = itemname.lower()
          itemname = modtext.capitalize()
          if itemname in db["shop"]:
            if str(inter.author.id) in db["balance"]:
              if str(inter.author.id) in db["inventory"]:
                if itemname not in db["inventory"][str(inter.author.id)]:
                  e = discord.Embed(title = "Shop", description = "You can't sell nothing!", color = random.randint(0, 16777215))
                  await inter.send(embed = e)
                  return
                else:
                  if db["inventory"][str(inter.author.id)].get(itemname) >= 2:
                    db["balance"][str(inter.author.id)] += int(db["shop"].get(itemname) // 2) * quantity
                    updateinv = db["inventory"][str(inter.author.id)]
                    if quantity == db["inventory"][str(inter.author.id)].get(itemname):
                      updateinv.pop(itemname)
                      itemammount = 0
                    else:
                      updateinv[itemname] -= quantity
                      itemammount = db["inventory"][str(inter.author.id)].get(itemname)
                    db["inventory"][str(inter.author.id)] = updateinv
                    e = discord.Embed(title = "Shop", description = f"You sold {quantity} {itemname}'s!", color = random.randint(0, 16777215))
                    e.set_footer(text = f"Now you have {itemammount} {itemname}'s")
                    await inter.send(embed = e)
                  else:
                    db["balance"][str(inter.author.id)] += int(db["shop"].get(itemname) // 2)
                    updateinv = db["inventory"][str(inter.author.id)]
                    updateinv.pop(itemname)
                    db["inventory"][str(inter.author.id)] = updateinv
                    itemammount = db["inventory"][str(inter.author.id)].get(itemname)
                    e = discord.Embed(title = "Shop", description = f"You sold {itemname}!", color = random.randint(0, 16777215))
                    await inter.send(embed = e)
              else:
                e = discord.Embed(title = "Shop", description = f"You can't sell nothing!", color = random.randint(0, 16777215))
                await inter.send(embed = e)
            else:
              db["balance"][str(inter.author.id)] = 0
              await inter.send(content = "Try again!", ephemeral = True)
          else:
            await inter.send(content = "Error: You can't sell nothing!", ephemeral = True)
        else:
          await inter.send(content = "Error: You can't sell nothing!", ephemeral = True)
      else:
        await inter.send(content = "Error: You can't sell more than you have", ephemeral = True)
    else:
      await inter.send(content = "Error: You can't sell 0 or less items", ephemeral = True)

  #inventory command
  @commands.slash_command(name = "inventory", description = "See what do you have")
  async def slashinventory(inter, member: discord.Member = None):
    '''
    See what do you have

    Parameters
    ----------
    member: Mentioned member
    '''
    if member is None:
      if str(inter.author.id) in db["inventory"] and db["inventory"][str(inter.author.id)] != {}:
        inventory = "\n".join(f"{index}. `{name}`: {amount}" for index, (name, amount) in enumerate(db["inventory"][str(inter.author.id)].items(), start = 1))
        e = discord.Embed(title = f"Inventory: @{inter.author.name}", description = inventory, color = random.randint(0, 16777215))
        await inter.send(embed = e)
      else:
        e = discord.Embed(title = f"Inventory: @{inter.author.name}", description = "You have nothing right now", color = random.randint(0, 16777215))
        await inter.send(embed = e)
    else:
      if str(member.id) in db["inventory"] and db["inventory"][str(member.id)] != {}:
        inventory = "\n".join(f"{index}. `{name}`: {amount}" for index, (name, amount) in enumerate(db["inventory"][str(member.id)].items(), start = 1))
        e = discord.Embed(title = f"Inventory: @{member.name}", description = inventory, color = random.randint(0, 16777215))
        await inter.send(embed = e)
      else:
        e = discord.Embed(title = f"Inventory: @{member.name}", description = "They have nothing right now", color = random.randint(0, 16777215))
        await inter.send(embed = e)

  #hack command
  @commands.slash_command(description = "Hacks random people. Requirement: 1 Computer. Has cooldown of 1 hour")
  @commands.cooldown(rate = 1, per = 3600, type = commands.BucketType.user)
  async def hack(inter):
    if str(inter.author.id) in db["balance"]:
      if str(inter.author.id) in db["inventory"]:
        if "Computer" in db["inventory"][str(inter.author.id)]:
          chance = random.randint(0, 1000)
          if chance > 350:
            rng = random.randint(250, 1500)
            db["balance"][str(inter.author.id)] += rng
            e = discord.Embed(title = "Success", description = f"You hacked people and sold the data\nYou got {rng} 💵 !", color = random.randint(0, 16777215))
            if str(inter.author.id) in db["debug"]:
              e.add_field(name = "Debug", value = f"Variables value:\n{rng}, {db['balance'][str(inter.author.id)]}")
            await inter.send(embed = e)
          else:
            db["balance"][str(inter.author.id)] -= 2500
            e = discord.Embed(title = "You got caught by police", description = "You lost 2500 💵 !", color = random.randint(0, 16777215))
            if str(inter.author.id) in db["debug"]:
              e.add_field(name = "Debug", value = f"Variables value:\n{db['balance'][str(inter.author.id)]}")
            await inter.send(embed = e)
        else:
          e = discord.Embed(title = "Error", description = "Buy a computer!", color = random.randint(0, 16777215))
          await inter.send(embed = e, ephemeral = True)
      else:
        db["inventory"][str(inter.author.id)] = {}
        e = discord.Embed(title = "Error", description = "Buy a computer!", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)
    else:
      e = discord.Embed(title = "Error", description = "Get some money and buy a computer!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

  #post meme command
  @commands.slash_command(description = "Post memes and get money from it, Requirement: a Laptop")
  @commands.cooldown(rate = 1, per = 30, type = commands.BucketType.user)
  async def postmeme(self, inter):
    if str(inter.author.id) in db["balance"]:
      if str(inter.author.id) in db["inventory"]:
        if "Laptop" in db["inventory"][str(inter.author.id)]:
          e = discord.Embed(title = "Post meme", description = "Post one of meme types below to get some cash!", color = random.randint(0, 16777215))
          await inter.send(embed = e, view = pmview(inter))
        else:
          e = discord.Embed(title = "Error", description = "Buy a laptop!", color = random.randint(0, 16777215))
          await inter.send(embed = e)
          inter.command.reset_cooldown(inter)
      else:
        db["inventory"][str(inter.author.id)] = {}
        e = discord.Embed(title = "Error", description = "Buy a laptop!", color = random.randint(0, 16777215))
        await inter.send(embed = e)
        inter.command.reset_cooldown(inter)
    else:
      e = discord.Embed(title = "Error", description = "Get some money and buy a laptop!", color = random.randint(0, 16777215))
      await inter.send(embed = e)
      inter.command.reset_cooldown(inter)

  #mail command
  @commands.slash_command(name = "mail", description = "Mail someone with the bot. Requirement: Both you and mentioned member must have atleast 1 smartphone")
  async def slashmail(inter, member: discord.Member, text, imagelink = ""):
    '''
    Mail someone with the bot. Requirement: Both You and Mentioned member must have atleast 1 smartphone
  
    Parameters
    ----------
    member: Mention member here
    text: Text to send
    imagelink: Image to send (link)
    '''
    if str(inter.author.id) in db["inventory"]:
      if "Smartphone" in db["inventory"][str(inter.author.id)]:
        if str(member.id) in db["inventory"]:
          if "Smartphone" in db["inventory"][str(member.id)]:
            e = discord.Embed(title = "New mail", description = text, color = random.randint(0, 16777215))
            e.set_author(name = str(inter.author), icon_url = str(inter.author.avatar)[:-10])
            e.set_footer(text = "You have 5 minutes to respond")
            if imagelink != "":
              e.set_image(url = imagelink)
            await member.send(embed = e)
            e = discord.Embed(title = "Success", description = f"Sent `{text}` to `@{member.name}`!", color = random.randint(0, 16777215))
            await inter.send(embed = e)
            try:
              message = await inter.bot.wait_for("message", check = lambda message: message.author == member and message.channel == member.dm_channel, timeout = 300)
              e = discord.Embed(title = f"Response from mailed user (@{membername})", description = message.content, color = random.randint(0, 16777215))
              if message.attachments:
                e.set_image(message.attachments[0].url)
              await inter.send(embed = e)
            except asyncio.TimeoutError:
              e = discord.Embed(title = f"No response from mailed user (@{member.name})", color = random.randint(0, 16777215))
              await inter.send(embed = e, ephemeral = True)
          else:
            e = discord.Embed(title = "Error", description = f"Sorry you can't message @{member.name}\n{member.name} has no smartphone!", color = random.randint(0, 16777215))
            await inter.send(embed = e, ephemeral = True)
        else:
          e = discord.Embed(title = "Error", description = f"Sorry you can't message @{member.name}\n{member.name} has no smartphone!", color = random.randint(0, 16777215))
          await inter.send(embed = e, ephemeral = True)
      else:
        e = discord.Embed(title = "Error", description = f"Sorry you can't message @{member.name}\nYou have no smartphone!", color = random.randint(0, 16777215))
        await inter.send(embed = e, ephemeral = True)
    else:
      e = discord.Embed(title = "Error", description = f"Sorry you can't message {member.name}\nYou have no smartphone!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

  #profile command
  @commands.slash_command(name = "profile", description = "See user's economical info!")
  async def slashprofile(inter, member: discord.Member = None):
    '''
    See member's economical info!
  
    Parameters
    ----------
    member: Mentioned member
    '''
    money = 0
    inventory = "Nothing here"
    passive = "False"
    if member == None:
      if str(inter.author.id) in db["balance"]:
        money = db["balance"][str(inter.author.id)]
      if str(inter.author.id) in db["inventory"]:
        inventory = "\n".join(f"{index}. `{name}`: {amount}" for index, (name, amount) in enumerate(db["inventory"][str(inter.author.id)].items(), start = 1))
      if str(inter.author.id) in db["passive"]:
        passive = "True"

      e = discord.Embed(title = f"{inter.author.name}'s profile", description = f"Balance: {money} 💵\nPassive: {passive}", color = random.randint(0, 16777215))
      e.set_thumbnail(url = inter.author.avatar)
      e.add_field(name = "Inventory", value = inventory, inline = False)
      await inter.send(embed = e)
    else:
      if str(member.id) in db["balance"]:
        money = db["balance"][str(member.id)]
      if str(member.id) in db["inventory"]:
        inventory = "\n".join(f"{index}. `{name}`: {amount}" for index, (name, amount) in enumerate(db["inventory"][str(member.id)].items(), start = 1))
      if str(member.id) in db["passive"]:
        passive = "True"

      e = discord.Embed(title = f"{member.name}'s profile", description = f"Balance: {money} 💵\nPassive: {passive}", color = random.randint(0, 16777215))
      e.set_thumbnail(url = member.avatar)
      e.add_field(name = "Inventory", value = inventory, inline = False)
      await inter.send(embed = e)

def setup(bot):
  bot.add_cog(Economy(bot))