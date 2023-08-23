#cog by @maxy_dev (maxy#2866)
import disnake as discord
from disnake.ext import commands
from enum import Enum
import random
import asyncio
import os
from utils import db

if "balance" not in db:
  db["balance"] = {}

if "bank" not in db:
  db["bank"] = {}

if "passive" not in db:
  db["passive"] = {}

item_info = {
	"Computer": "Usable: hack Command/False\nType: Item\nInfo: You can hack people's data on this",
	"Laptop": "Usable: postmeme Command/False\nType: Item\nInfo: You can post memes on this",
  "Golden coin": "Usable: False\nType: Collection\nInfo: Just buy a ton of those coins and flex to your friends",
	"Discount card": "Usable: False\nType: Item\nInfo: Gives 25% sale on every item in the shop!",
	"Smartphone": "Usable: mail Command/False\nType: Item\nInfo: You can mail someone with this",
	"Lottery": "Usable: True\nType: Item\nInfo: Gives random amount of cash... Sometimes huge amount of cash"
}

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

def lottery():
  win = None
  while True:
    chance = random.randint(0, 100)
    if 30 <= chance <= 50:
      win = random.randint(5, 50)
    elif chance >= 30:
      win = random.randint(50, 200)

    else:
      continue
    break
  return win

async def suggest_buyitem(inter, input):
  return [item for item in list(db['shop'].keys()) if input.lower() in item.lower()][0:24]

async def suggest_item(inter, input):
  if str(inter.author.id) not in db["inventory"]:
    db["inventory"][str(inter.author.id)] = {}
  return [item for item in list(db['inventory'][str(inter.author.id)].keys()) if input.lower() in item.lower()][0:24] if db['inventory'][str(inter.author.id)] and [item for item in list(db['inventory'][str(inter.author.id)].keys()) if input.lower() in item.lower()][0:24] else ["You have nothing!"]

async def suggest_usableitem(inter, input):
  if str(inter.author.id) not in db["inventory"]:
    db["inventory"][str(inter.author.id)] = {}
  return [item for item in list(db['inventory'][str(inter.author.id)].keys()) if input.lower() in item.lower() and item.lower() in ["lottery"]][0:24] if db['inventory'][str(inter.author.id)] and [item for item in list(db['inventory'][str(inter.author.id)].keys()) if input.lower() in item.lower() and item.lower() in ["lottery"]][0:24] else ["You have nothing to use!"]

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

class Economy2(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

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
    if item not in db["inventory"][str(inter.author.id)]:
      e = discord.Embed(title = "Error", description = f"You don't have `{itemname}` in your inventory...", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    if item != "Lottery":
      e = discord.Embed(title = "Error", description = f"Item `{itemname}` can't be used", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    win = lottery()
    if db["inventory"][str(inter.author.id)].get(item) >= 2:
      db["inventory"][str(inter.author.id)][item] -= 1
    else:
      db["inventory"][str(inter.author.id)].pop(item)
    e = discord.Embed(title = f"You won {win} 💵!", description = "congratulations i guess...", color = random.randint(0, 16777215))
    db["balance"][str(inter.author.id)] += win
    await inter.send(embed = e)

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
    if item not in db["inventory"][str(inter.author.id)]:
      e = discord.Embed(title = "Error", description = f"You don't have `{itemname}` in your inventory...", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    e = discord.Embed(title = f"Item: {item}", description = f"{iteminfo(item)}", color = random.randint(0, 16777215))
    await inter.send(embed = e)

  @commands.slash_command()
  async def balance(self, inter, member: discord.Member = None):
    '''
    See yours or someone else's balance

    Parameters
    ----------
    member: Mention member
    '''
    await inter.response.defer()
    if member is None:
      member = inter.author
    if str(member.id) not in db["balance"]:
      db["balance"][str(member.id)] = 0
    if str(member.id) not in db["bank"]:
      db["bank"][str(member.id)] = 0
    e = discord.Embed(title = f"@{member.name}'s Balance", description = f"Wallet: `{db['balance'][str(member.id)]}` 💵\nBank: `{db['bank'][str(member.id)]}` 🏦", color = random.randint(0, 16777215))
    await inter.send(embed = e)

  @commands.slash_command(rate = 1, per = 60 * 30, type = commands.BucketType.user)
  async def work(self, inter):
    '''
    Get money from work
    '''
    if str(inter.author.id) not in db["balance"]:
      db["balance"][str(inter.author.id)] = 0
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
    await inter.send(embed = e)
    try:
      message = await inter.bot.wait_for("message", check = lambda message: message.author == inter.author and message.channel == inter.channel, timeout = 60)
      rng = random.randint(50, 250)
      e = discord.Embed(title = "Failed", description = f"You got {rng} 💵 !", color = random.randint(0, 1677215))
      if int(message.content) == answer:
        rng = random.randint(250, 1000)
        e = discord.Embed(title = "Success", description = f"You got {rng} 💵 !", color = random.randint(0, 1677215))
      db["balance"][str(inter.author.id)] += rng
      await inter.send(embed = e)
    except (asyncio.TimeoutError, ValueError):
      rng = random.randint(50, 250)
      db["balance"][str(inter.author.id)] += rng
      e = discord.Embed(title = "Failed", description = f"You got {rng} 💵 !", color = random.randint(0, 1677215))
      e.set_footer(text = f"The right answer was {answer}")
      await inter.send(embed = e)

  @commands.slash_command(rate = 1, per = 10, type = commands.BucketType.user)
  async def beg(self, inter):
    '''
    Beg for money
    '''
    if str(inter.author.id) not in db["balance"]:
      db["balance"][str(inter.author.id)] = 0
    if random.randint(0, 100) < 35:
      e = discord.Embed(title = "Fail", description = "You failed!", color = random.randint(0 , 16777215))
      await inter.send(embed = e)
      return
    rng = random.randint(50, 150)
    db["balance"][str(inter.author.id)] += rng
    e = discord.Embed(title = "Success", description = f"You got {rng} 💵 !", color = random.randint(0, 16777215))
    await inter.send(embed = e)

  @commands.slash_command()
  async def give(self, inter, member: discord.Member, cash: str):
    '''
    Give your money to other users!

    Parameters
    ----------
    member: Mention member
    cash: Money to give
    '''
    if cash.isnumeric():
      cash = int(amount)
    elif cash in ["max", "all", "half", "quarter"]:
      cash = int(db["balance"][str(inter.author.id)] / (4 if cash == "quarter" else 2 if cash == "half" else 1))
    if str(inter.author.id) not in db["balance"]:
      db["balance"][str(inter.author.id)] = 0
    if str(member.id) not in db["balance"]:
      db["balance"][str(member.id)] = 0
    if str(inter.author.id) == str(member.id):
      e = discord.Embed(title = "Error", description = "You can't give money to yourself", color = random.randint(0, 1677215))
      await inter.send(embed = e, ephemeral = True)
      return
    if cash > db["balance"][str(inter.author.id)]:
      e = discord.Embed(title = "Error", description = "You can't give more than you have!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    if cash <= 0:
      e = discord.Embed(title = "Error", description = "You can't give negative amount of money (aka take them)", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    if str(inter.author.id) in db["passive"]:
      e = discord.Embed(title = "Error", description = "You can't give money in passive mode!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    if str(member.id) in db["passive"]:
      e = discord.Embed(title = "Error", description = "Leave peaceful person alone!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
    db["balance"][str(inter.author.id)] -= cash
    db["balance"][str(member.id)] += cash
    e = discord.Embed(title = "Success", description = f"`@{member.name}` got `{cash}` 💵 !", color = random.randint(0, 16777215))
    await inter.send(embed = e)

  @commands.slash_command(rate = 1, per = 60, type = commands.BucketType.user)
  async def rob(self, inter, member: discord.Member):
    '''
    Rob people and get all their money! but you have a chance to get caught

    Parameters
    ----------
    member: Mention member
    '''
    if str(inter.author.id) not in db["balance"]:
      db["balance"][str(inter.author.id)] = 0
    if str(member.id) not in db["balance"]:
      db["balance"][str(member.id)] = 0
    if inter.author == member:
      e = discord.Embed(title = "Error", description = "You can't rob yourself!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      inter.application_command.reset_cooldown(inter.application_command)
      return
    if str(inter.author.id) in db["passive"]:
      e = discord.Embed(title = "Error", description = "You can't rob in passive mode!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      inter.application_command.reset_cooldown(inter.application_command)
      return
    if str(member.id) in db["passive"]:
      e = discord.Embed(title = "Error", description = "Leave peaceful person alone!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      inter.application_command.reset_cooldown(inter.application_command)
      return
    if db["balance"][str(member.id)] < 500:
      e = discord.Embed(title = "Error", description = "You can't rob people with less than 500 💵!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      inter.application_command.reset_cooldown(inter.application_command)
      return
    chance = random.randint(0, 100)
    if chance < 25:
      rng = random.randint(250, db["balance"][str(member.id)])
      db["balance"][str(member.id)] -= rng
      db["balance"][str(inter.author.id)] += rng
      e = discord.Embed(title = "Success", description = f"You just robbed `@{member.name}` for {rng} 💵!", color = random.randint(0, 16777215))
      await inter.send(embed = e)
    else:
      fine = 2500
      if db["balance"][str(inter.author.id)] < 2500:
        fine = db["balance"][str(inter.author.id)]
      db["balance"][str(inter.author.id)] -= fine
      e = discord.Embed(title = "Failed", description = f"You failed and police fined you for `{fine}` 💵", color = random.randint(0, 16777215))
      await inter.send(embed = e)
      return

  @commands.slash_command()
  async def gamble(self, inter, money: int):
    '''
    Gamble and lose all of your money to RNJesus

    Parameters
    ----------
    money: Your bet
    '''
    if str(inter.author.id) not in db["balance"]:
      db["balance"][str(inter.author.id)] = 0
    if money > db["balance"][str(inter.author.id)]:
      e = discord.Embed(title = "Error", description = "You can't gamble more than you have!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    if money <= 0:
      e = discord.Embed(title = "Error", description = "You can't gamble negative amount of money (aka take them)", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    rng = random.randint(0, 12)
    dice = random.randint(0, 12)
    if rng < dice:
      db["balance"][str(inter.author.id)] += payment
      e = discord.Embed(title = "You win", description = f"You got {payment} 💵 !", color = random.randint(0, 16777215))
      e.set_footer(text = f"You won: {dice} to {rng}")
    elif rng == dice:
      e = discord.Embed(title = "Tie", description = "You didn't lose or win anything", color = random.randint(0 , 16777215))
      e.set_footer(text = f"Tie: {dice} to {rng}")
    else:
      db["balance"][str(inter.author.id)] -= payment
      e = discord.Embed(title = "You lose", description = f"You lost {payment} 💵 !", color = random.randint(0, 16777215))
      e.set_footer(text = f"You lost: {dice} to {rng}")
    await inter.send(embed = e)

  @commands.slash_command(rate = 1, per = 86400, type = commands.BucketType.user)
  async def daily(self, inter):
    '''
    Get 1000 cash every day
    '''
    if str(inter.author.id) not in db["balance"]:
      db["balance"][str(inter.author.id)] = 0
    db["balance"][str(inter.author.id)] += 1000
    e = discord.Embed(title = "Daily", description = "You got 1000 💵 !", color = random.randint(0, 16777215))
    await inter.send(embed = e)

  @commands.slash_command(rate = 1, per = 1800, type = commands.BucketType.user)
  async def passive(self, inter, option: bool):
    '''
    Be passive so your money won't be stolen

    Parameters
    ----------
    option: True or False
    '''
    if option:
      if str(inter.author.id) not in db["passive"]:
        db["passive"][str(inter.author.id)] = True
        e = discord.Embed(title = "Success", description = "Youre now a passive person!", color = random.randint(0, 16777215))
        await inter.send(embed = e)
        return
      else:
        e = discord.Embed(title = "Error", description = "Youre already a passive person!", color = random.randint(0, 16777215))
        await inter.send(embed = e)
        inter.application_command.reset_cooldown(inter.application_command)
        return
    else:
      if str(inter.author.id) in db["passive"]:
        del db["passive"][str(inter.author.id)]
        e = discord.Embed(title = "Success", description = "Youre now a normal person!", color = random.randint(0, 16777215))
        await inter.send(embed = e)
        return
      else:
        e = discord.Embed(title = "Error", description = "Youre already a normal person!", color = random.randint(0, 16777215))
        await inter.send(embed = e)
        inter.application_command.reset_cooldown(inter.application_command)
        return

  @commands.slash_command()
  async def mail(self, inter, member: discord.Member, message: str, imagelink: str = None, attachment: discord.Attachment = None):
    '''
    Mail someone with the bot. Requirement: Both You and Mentioned member must have atleast 1 smartphone

    Parameters
    ----------
    member: Mention member here
    message: Text to send
    imagelink: Image to send (link)
    attachment: An attachment
    '''
    if str(inter.author.id) not in db["inventory"]:
      db["inventory"][str(inter.author.id)] = {}
    if str(member.id) not in db["inventory"]:
      db["inventory"][str(member.id)] = {}
    if member == inter.author:
      e = discord.Embed(title = "Error", description = "You can't message yourself!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    if "Smartphone" not in db["inventory"][str(inter.author.id)]:
      e = discord.Embed(title = "Error", description = f"You have no smartphone!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    if "Smartphone" not in db["inventory"][str(member.id)]:
      e = discord.Embed(title = "Error", description = f"Sorry you can't message @{member.name}\n@{member.name} has no smartphone!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    await inter.response.defer(ephemeral = True)
    e = discord.Embed(title = "New mail", description = message, color = random.randint(0, 16777215))
    e.set_author(name = f"@{inter.author.name}", icon_url = str(inter.author.avatar)[:-10])
    e.set_footer(text = "You have 5 minutes to respond")
    if imagelink != "":
      e.set_image(url = imagelink)
    await member.send(embed = e, file = attachment)
    e = discord.Embed(title = "Success", description = f"Sent `{message}` to `@{member.name}`!", color = random.randint(0, 16777215))
    await inter.send(embed = e)
    try:
      message = await inter.bot.wait_for("message", check = lambda message: message.author == member and message.channel == member.dm_channel, timeout = 300)
      e = discord.Embed(title = f"Response from mailed user", description = message.content, color = random.randint(0, 16777215))
      e.set_author(name = f"@{member.name}", icon_url = str(member.avatar)[:-10])
      if message.attachments:
        e.set_image(message.attachments[0].url)
      await inter.send(embed = e)
    except asyncio.TimeoutError:
      e = discord.Embed(title = f"No response from mailed user (@{member.name})", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)

  @commands.slash_command()
  async def profile(self, inter, member: discord.Member = None):
    '''
    See member's economical info!

    Parameters
    ----------
    member: Mentioned member
    '''
    inventory = "Nothing here"
    passive = "False"
    if member is None:
      member = inter.author
    if str(member.id) not in db["balance"]:
      db["balance"][str(member.id)] = 0
    if str(member.id) not in db["bank"]:
      db["bank"][str(member.id)] = 0
    if str(member.id) in db["inventory"]:
      inventory = "\n".join(f"{index}. `{name}`: {amount}" for index, (name, amount) in enumerate(db["inventory"][str(member.id)].items(), start = 1))
    if str(member.id) in db["passive"]:
      passive = "True"

    e = discord.Embed(title = f"@{member.name}'s profile", description = f"Wallet: `{db['balance'][str(member.id)]}` 💵\nBank: `{db['bank'][str(member.id)]}` 🏦\n\nPassive: {passive}", color = random.randint(0, 16777215))
    e.set_thumbnail(url = member.avatar)
    e.add_field(name = "Inventory", value = inventory, inline = False)
    await inter.send(embed = e)

  @commands.slash_command()
  async def bank(self, inter):
    if str(inter.author.id) not in db["bank"]:
      db["bank"][str(inter.author.id)] = 0
    if str(inter.author.id) not in db["balance"]:
      db["balance"][str(inter.author.id)] = 0

  @bank.sub_command()
  async def withdraw(self, inter, amount: str):
    '''
    Withdraw money from your bank

    Parameters
    ----------
    amount: Money to withdraw, keywords: max, all, half, quarter
    '''
    if amount.isnumeric():
      amount = int(amount)
    elif amount in ["max", "all", "half", "quarter"]:
      amount = int(db["bank"][str(inter.author.id)] / (4 if amount == "quarter" else 2 if amount == "half" else 1))
    else:
      e = discord.Embed(title = "Error", description = "Invalid amount", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    if amount > db["bank"][str(inter.author.id)]:
      e = discord.Embed(title = "Error", description = "You don't have enough money to withdraw", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    if amount <= 0:
      e = discord.Embed(title = "Error", description = "Invalid amount", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    db["bank"][str(inter.author.id)] -= amount
    db["balance"][str(inter.author.id)] += amount
    e = discord.Embed(title = "Success", description = f"You withdrew `{amount}` 💵!", color = random.randint(0, 16777215))
    await inter.send(embed = e)


  @bank.sub_command()
  async def deposit(self, inter, amount: str):
    '''
    Deposit money to your bank

    Parameters
    ----------
    amount: Money to deposit, keywords: max, all, half, quarter
    '''
    if amount.isnumeric():
      amount = int(amount)
    elif amount in ["max", "all", "half", "quarter"]:
      amount = int(db["balance"][str(inter.author.id)] / (4 if amount == "quarter" else 2 if amount == "half" else 1))
    else:
      e = discord.Embed(title = "Error", description = "Invalid amount", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    if amount > db["balance"][str(inter.author.id)]:
      e = discord.Embed(title = "Error", description = "You don't have enough money to deposit", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    if amount <= 0:
      e = discord.Embed(title = "Error", description = "Invalid amount", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    db["bank"][str(inter.author.id)] += amount
    db["balance"][str(inter.author.id)] -= amount
    e = discord.Embed(title = "Success", description = f"You deposited `{amount}` 💵!", color = random.randint(0, 16777215))
    await inter.send(embed = e)

  @commands.slash_command()
  async def inventory(self, inter, member: discord.Member = None):
    '''
    Check someones inventory

    Parameters
    ----------
    member: Mentioned member
    '''
    noun = "They"
    if member is None:
      member = inter.author
      noun = "You"
    if str(member.id) not in db["inventory"]:
      db["inventory"][str(member.id)] = {}
    inventory = f"{noun} have nothing right now"
    if db["inventory"][str(member.id)] != {}:
      inventory = "\n".join(f"{index}. `{name}`: {amount}" for index, (name, amount) in enumerate(db["inventory"][str(member.id)].items(), start = 1))
    e = discord.Embed(title = f"@{member.name}'s inventory", description = inventory, color = random.randint(0, 16777215))
    await inter.send(embed = e)

  @commands.slash_command()
  async def item(self, inter):
    if str(inter.author.id) not in db["inventory"]:
      db["inventory"][str(inter.author.id)] = {}

  @item.sub_command()
  async def use(self, inter, item: str = commands.Param(autocomplete = suggest_usableitem)):
    '''
    Use an item

    Parameters
    ----------
    item: Item name
    '''
    item = item.lower().capitalize()
    if item not in db["inventory"][str(inter.author.id)]:
      e = discord.Embed(title = "Error", description = f"You don't have `{item}`!", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    if item not in ["Lottery"]:
      e = discord.Embed(title = "Error", description = f"This item is not usable...", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    win = lottery()
    if db["inventory"][str(inter.author.id)].get(item) >= 2:
      db["inventory"][str(inter.author.id)][item] -= 1
    else:
      db["inventory"][str(inter.author.id)].pop(item)
    e = discord.Embed(title = f"You won {win} 💵!", description = "congratulations i guess...", color = random.randint(0, 16777215))
    db["balance"][str(inter.author.id)] += win
    await inter.send(embed = e)

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

  @commands.slash_command()
  async def shop(self, inter):
    if str(inter.author.id) not in db["inventory"]:
      db["inventory"][str(inter.author.id)] = {}

  #items sub command
  @shop.sub_command()
  async def items(self, inter):
    '''
    See prices of items here
    '''
    shop = '\n'.join(f'`{i+1}.` {item}: {price if "Discount card" not in db["inventory"][str(inter.author.id)] else int(price * 0.75)}' for i, (price,item) in enumerate(sorted(((price,item) for item,price in db['shop'].items()),reverse=True)))
    e = discord.Embed(title = "Shop", description = shop, color = random.randint(0, 16777215))
    await inter.send(embed = e)

  @shop.sub_command()
  async def buy(self, inter, item: str = commands.Param(autocomplete = suggest_buyitem), quantity: int = 1):
    '''
    Buy an item

    Parameters
    ----------
    item: Item name
    '''
    item = item.lower().capitalize()
    if str(inter.author.id) not in db["balance"]:
      db["balance"][str(inter.author.id)] = 0

    if quantity < 0:
      e = discord.Embed(title = "Error", description = "Invalid quantity", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    if item not in db["shop"]:
      e = discord.Embed(title = "Error", description = f"Invalid item", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    totalprice = int(db["shop"].get(item) * (0.75 if "Discount card" in db["inventory"][str(inter.author.id)] else 1)) * quantity
    if db["balance"][str(inter.author.id)] < totalprice:
      e = discord.Embed(title = "Error", description = "You don't have enough money", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    db["balance"][str(inter.author.id)] -= totalprice
    e = discord.Embed(title = "Shop", description = f"You got {quantity} {item}'s!", color = random.randint(0, 16777215))
    if item not in db["inventory"][str(inter.author.id)]:
      db["inventory"][str(inter.author.id)][item] = quantity
    else:
      db["inventory"][str(inter.author.id)][item] += quantity
      amount = quantity + db["inventory"][str(inter.author.id)][item]
      e.set_footer(text = f"Now you have {amount} {item}'s")
    await inter.send(embed = e)

  @shop.sub_command()
  async def sell(self, inter, item: str = commands.Param(autocomplete = suggest_item), quantity: int = 1):
    '''
    Sell an item
    '''
    if str(inter.author.id) not in db["balance"]:
      db["balance"][str(inter.author.id)] = 0
    if quantity < 0:
      e = discord.Embed(title = "Error", description = "Invalid quantity", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    if quantity > db["inventory"][str(inter.author.id)][item]:
      e = discord.Embed(title = "Error", description = "You can't sell more than you have", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    itme = item.lower().capitalize()
    if item not in db["shop"]:
      e = discord.Embed(title = "Error", description = f"Invalid item", color = random.randint(0, 16777215))
      await inter.send(embed = e, ephemeral = True)
      return
    db["balance"][str(inter.author.id)] += int(db["shop"].get(item) // 2) * quantity
    e = discord.Embed(title = "Shop", description = f"You sold {quantity} {item}'s!", color = random.randint(0, 16777215))
    if quantity == db["inventory"][str(inter.author.id)][item]:
      db["inventory"][str(inter.author.id)].pop(item)
    else:
      db["inventory"][str(inter.author.id)][item] -= quantity
      e.set_footer(text = f"Now you have {db['inventory'][str(inter.author.id)][item]} {item}'s")
    await inter.send(embed = e)

  @commands.slash_command()
  @commands.cooldown(rate = 1, per = 30, type = commands.BucketType.user)
  async def postmeme(self, inter):
    '''
    Post memes and get upvotes (and money), requires a laptop
    '''
    if str(inter.author.id) not in db["balance"]:
      db["balance"][str(inter.author.id)] = 0
    if str(inter.author.id) not in db["inventory"]:
      db["inventory"][str(inter.author.id)] = {}
    if "Laptop" not in db["inventory"][str(inter.author.id)]:
      db["inventory"][str(inter.author.id)] = {}
      e = discord.Embed(title = "Error", description = "Buy a laptop!", color = random.randint(0, 16777215))
      await inter.send(embed = e)
      inter.command.reset_cooldown(inter)
      return
    e = discord.Embed(title = "Post meme", description = "Post one of meme types below to get some cash!", color = random.randint(0, 16777215))
    await inter.send(embed = e, view = pmview(inter))

def setup(bot):
  bot.add_cog(Economy2(bot))