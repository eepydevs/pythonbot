#cog by Number1#4325
import disnake as discord
from disnake.ext import commands
import random
import asyncio
from replit import db

whitelist = [439788095483936768, 826509766893371392]

if "balance" not in db:
  db["balance"] = {}

if "passive" not in db:
  db["passive"] = {}

if "shop" not in db:
  db["shop"] = {
    "Discount card": 20000,
    "Computer": 6500,
    "Laptop": 2000,
    "Smartphone": 500
  }

if "inventory" not in db:
  db["inventory"] = {}

def iteminfo(name):
  if name == "Computer":
    return "Usable: hack Command/False\nType: Item\nInfo: You can hack people's data on this"
  if name == "Laptop":
    return "Usable: postmeme Command/False\nType: Item\nInfo: You can post memes on this"
  if name == "Smartphone":
    return "Usable: mail Command/False\nType: Item\nInfo: You can mail someone with this"
  if name == "Discount card":
    return "Usable: False\nType: Item\nInfo: Gives 25% sale on every item in the shop!"


class Economy(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  #item group
  @commands.group(help = "See what you can do with selected item")
  async def item(self, ctx):
    if ctx.invoked_subcommand == None:
      e = discord.Embed(title = "This is the item command", description = "Use pb!help item to see the subcommands", color = random.randint(0, 16777215))
      await ctx.send(embed = e)
  
  #info command
  @item.command(help = "See selected item info")
  async def info(self, ctx, itemname = None):
    if str(ctx.author.id) in db["inventory"]:
      item = itemname.lower().capitalize()
      if item != None:
        if item in db["inventory"][str(ctx.author.id)]:
          e = discord.Embed(title = f"Item: {item}", description = f"{iteminfo(item)}", color = random.randint(0, 16777215))
          await ctx.send(embed = e)
        else:
          e = discord.Embed(title = "Error", description = f"You don't have `{itemname}` in your inventory...", color = random.randint(0, 16777215))
          await ctx.send(embed = e)
      else:
        e = discord.Embed(title = "Error", description = "You can't see info of nothing!", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
    else:
      e = discord.Embed(title = "Error", description = "You have nothing right now!", color = random.randint(0, 16777215))
      await ctx.send(embed = e)

  #use command
  @item.command(help = "Use an item")
  async def use(self, ctx, itemname = None):
    if str(ctx.author.id) in db["inventory"]:
      item = itemname.lower().capitalize()
      if item != None:
        if item in db["inventory"][str(ctx.author.id)]:
          if item in []:
            pass
          else:
            e = discord.Embed(title = "Error", description = f"Item `{itemname}` can't be used", color = random.randint(0, 16777215))
            await ctx.send(embed = e)
        else:
          e = discord.Embed(title = "Error", description = f"You don't have `{itemname}` in your inventory...", color = random.randint(0, 16777215))
          await ctx.send(embed = e)
      else:
        e = discord.Embed(title = "Error", description = "You can't use nothing!", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
    else:
      e = discord.Embed(title = "Error", description = "You have nothing right now!", color = random.randint(0, 16777215))
      await ctx.send(embed = e)

  #balance command
  @commands.command(aliases = ["bal", "cash", "money"], help = "Look how much cash you have", description = "Youre poor")
  async def balance(self, ctx, member: discord.Member = None):
    if member is None:
      if str(ctx.author.id) not in db["balance"]:
        db["balance"][str(ctx.author.id)] = 0
        e = discord.Embed(title = f"{ctx.author}'s Balance", description = f"Wallet: {db['balance'][str(ctx.author.id)]} 💵", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
      else:
        wallet = db["balance"][str(ctx.author.id)]
        e = discord.Embed(title = f"{ctx.author}'s Balance", description = f"Wallet: {wallet} 💵", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
    else:
      if str(member.id) not in db["balance"]:
        db["balance"][str(member.id)] = 0
        wallet = db["balance"][str(member.id)]
        e = discord.Embed(title = f"{member}'s Balance", description = f"Wallet: {wallet} 💵", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
      else:
        wallet = db["balance"][str(member.id)]
        e = discord.Embed(title = f"{member}'s Balance", description = f"Wallet: {wallet} 💵", color = random.randint(0, 16777215))
        await ctx.send(embed = e)

  #beg command
  @commands.command(help = "Beg random people to give you some cash", description = "Beg people to them give you nothing lol\nHas cooldown of 10 seconds")
  @commands.cooldown(rate = 1, per = 10, type = commands.BucketType.user)
  async def beg(self, ctx):
    if str(ctx.author.id) not in db["balance"]:
      db["balance"][str(ctx.author.id)] = 0
      if random.randint(0, 100) < 35:
        e = discord.Embed(title = "Fail", description = "You failed!", color = random.randint(0 , 16777215))
        await ctx.send(embed = e)
      else:
        rng = random.randint(50, 150)
        db["balance"][str(ctx.author.id)] += rng
        e = discord.Embed(title = "Success", description = f"You got {rng} 💵 !", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
    else:
      if random.randint(0, 100) < 35:
        e = discord.Embed(title = "Fail", description = "You failed!", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
      else:
        rng = random.randint(50, 150)
        db["balance"][str(ctx.author.id)] += rng
        e = discord.Embed(title = "Success", description = f"You got {rng} 💵 !", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
      

  #work command
  @commands.command(help = "Work and get some cash", description = "Work to get some cash\nHas cooldown of 30 minutes")
  @commands.cooldown(rate = 1, per = 60 * 30, type = commands.BucketType.user)
  async def work(self, ctx):
    if str(ctx.author.id) in db["balance"]:
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
      await ctx.send(embed = e)
      try:
        message = await self.bot.wait_for("message", check = lambda message: message.author == ctx.author and message.channel == ctx.channel, timeout = 60)
        if int(message.content) == answer:
          rng = random.randint(250, 1000)
          db["balance"][str(ctx.author.id)] += rng
          e = discord.Embed(title = "Success", description = f"You got {rng} 💵 !", color = random.randint(0, 1677215))
          await ctx.send(embed = e)
        else:
          rng = random.randint(50, 250)
          db["balance"][str(ctx.author.id)] += rng
          e = discord.Embed(title = "Failed", description = f"You got {rng} 💵 !", color = random.randint(0, 1677215))
          e.set_footer(text = f"The right answer was {answer}")
          await ctx.send(embed = e)
      except asyncio.TimeoutError:
        rng = random.randint(50, 250)
        db["balance"][str(ctx.author.id)] += rng
        e = discord.Embed(title = "Failed", description = f"You got {rng} 💵 !", color = random.randint(0, 1677215))
        e.set_footer(text = f"The right answer was {answer}")
        await ctx.send(embed = e)
      except ValueError:
        rng = random.randint(50, 250)
        db["balance"][str(ctx.author.id)] += rng
        e = discord.Embed(title = "Failed", description = f"You got {rng} 💵 !", color = random.randint(0, 1677215))
        e.set_footer(text = f"The right answer was {answer}")
        await ctx.send(embed = e)
    else:
      db["balance"][str(ctx.author.id)] = 0
      rng = random.randint(250, 1000)
      db["balance"][str(ctx.author.id)] += rng
      e = discord.Embed(title = "Success", description = f"You got {rng} 💵 !", color = random.randint(0, 16777215))
      await ctx.send(embed = e)

  #give command
  @commands.command(aliases = ["share", "pay"], help = "Share some money with mentioned member", description = "Give money to members\nUsage: pb!give (@mention) (money)")
  @commands.guild_only()
  async def give(self, ctx, member: discord.Member, payment: int):
    if str(ctx.author.id) in db["balance"]:
      money = db["balance"][str(ctx.author.id)]
      if member.id != ctx.author.id:
        if payment <= money:
          if payment >= 1:
            if str(ctx.author.id) not in db["passive"]:
              if str(member.id) not in db["passive"]:
                if str(member.id) in db["balance"]:
                  db["balance"][str(ctx.author.id)] -= payment
                  db["balance"][str(member.id)] += payment
                  e = discord.Embed(title = "Success", description = f"{member} got {payment} 💵 !", color = random.randint(0, 16777215))
                  await ctx.send(embed = e)
                else:
                  db["balance"][str(member.id)] = 0
                  db["balance"][str(ctx.author.id)] -= payment
                  db["balance"][str(member.id)] += payment
                  e = discord.Embed(title = "Success", description = f"{member} got {payment} 💵 !", color = random.randint(0, 16777215))
                  await ctx.send(embed = e)
              else:
                e = discord.Embed(title = "Error", description = "Leave peaceful person alone!", color = random.randint(0, 16777215))
                await ctx.send(embed = e)
            else:
              e = discord.Embed(title = "Error", description = "You can't give money in passive mode!", color = random.randint(0, 16777215))
              await ctx.send(embed = e)
          else:
            e = discord.Embed(title = "Error", description = "You can't give negative amount of money (aka take them)", color = random.randint(0, 16777215))
            await ctx.send(embed = e)
        else:
          e = discord.Embed(title = "Error", description = "You can't give more than you have!", color = random.randint(0, 16777215))
          await ctx.send(embed = e)
      else:
        e = discord.Embed(title = "Error", description = "You can't give cash to yourself", color = random.randint(0, 1677215))
        await ctx.send(embed = e)
    else:
      db["balance"][str(ctx.author.id)] = 0
      e = discord.Embed(title = "Error", description = "You have 0 💵", color = random.randint(0, 16777215))
      await ctx.send(embed = e)
      
  #credit command (FOR WHITELISTED PEOPLE ONLY)
  @commands.command(aliases = ["darewin"], help = "Give money to person that won an event", description = "FOR WHITELISTED PEOPLE ONLY\ndare win command for event makers", hidden = True)
  @commands.check(lambda ctx: ctx.author.id in whitelist)
  @commands.guild_only()
  async def credit(self, ctx, member: discord.Member, payment: int):
    if str(member.id) in db["balance"]:
      db["balance"][str(member.id)] += payment
      e = discord.Embed(title = "Success", description = f"{member} got {payment} 💵 !", color = random.randint(0, 16777215))
      await ctx.send(embed = e)
    else:
      db["balance"][str(member.id)] = 0
      db["balance"][str(member.id)] += payment
      e = discord.Embed(title = "Success", description = f"{member} got {payment} 💵 !", color = random.randint(0, 16777215))
      await ctx.send(embed = e)

  #gamble command
  @commands.command(aliases = ["gam"], help = "Go to casino (casino is bad) and get some money", description = "Lose every dollar you have lol\nUsage: pb!gamble (money)")
  async def gamble(self, ctx, payment: int):
    rng = random.randint(0, 12)
    dice = random.randint(0, 12)
    if str(ctx.author.id) in db["balance"]:
      money = db["balance"][str(ctx.author.id)]
      if payment <= money:
        if payment >= 1:
          if rng < dice:
            db["balance"][str(ctx.author.id)] += payment
            e = discord.Embed(title = "You win", description = f"You got {payment} 💵 !", color = random.randint(0, 16777215))
            e.set_footer(text = f"You won: {dice} to {rng}")
            await ctx.send(embed = e)
          elif rng == dice:
            e = discord.Embed(title = "Tie", description = "You didn't lose or win anything", color = random.randint(0 , 16777215))
            e.set_footer(text = f"Tie: {dice} to {rng}")
            await ctx.send(embed = e)
          else:
            db["balance"][str(ctx.author.id)] -= payment
            e = discord.Embed(title = "You lose", description = f"You lost {payment} 💵 !", color = random.randint(0, 16777215))
            e.set_footer(text = f"You lost: {dice} to {rng}")
            await ctx.send(embed = e)
        else:
          e = discord.Embed(title = "Error", description = "You can't put negative amount of money on gamble", color = random.randint(0, 16777215))
          await ctx.send(embed = e)
      else:
        e = discord.Embed(title = "Error", description = "You can't put more than you have cash on gamble", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
    else:
      e = discord.Embed(title = "Error", description = "Go get some money first!", color = random.randint(0, 16777215))
      await ctx.send(embed = e)

  #daily commmand
  @commands.command(aliases = ["day"], help = "Get 1000 cash per day", description = "Will give you 1000 cash")
  @commands.cooldown(rate = 1, per = 86400, type = commands.BucketType.user)
  async def daily(self, ctx):
    if str(ctx.author.id) in db["balance"]:
      db["balance"][str(ctx.author.id)] += 1000
    else:
      db["balance"][str(ctx.author.id)] = 0
      db["balance"][str(ctx.author.id)] += 1000
    e = discord.Embed(title = "Daily", description = "You got 1000 💵 !", color = random.randint(0, 16777215))
    await ctx.send(embed = e)

  #leaderboard command
  @commands.command(aliases = ["lb"], help = "Richest people here", description = "See other rich people in leaderboard")
  @commands.guild_only()
  async def leaderboard(self, ctx):
    await ctx.trigger_typing()
    leaderboard = "\n".join(f"{index}. `{member}`: {amount} 💵" for index, (member, amount) in enumerate(sorted(filter(lambda i: i[0] != None, ((ctx.guild.get_member(int(i[0])), i[1]) for i in db["balance"].items())), key = lambda i: i[1], reverse = True), start = 1))
    e = discord.Embed(title = "Leaderboard", description = leaderboard, color = random.randint(0, 16777215))
    await ctx.send(embed = e)

  #rob command
  @commands.command(help = "Rob people and get money", description = "Get jailed\nHas cooldown of 30 seconds\nUsage: pb!rob (@mention)")
  @commands.cooldown(rate = 1, per = 30, type = commands.BucketType.user)
  async def rob(self, ctx, member: discord.Member = None):
    if member.id != ctx.author.id:
      if member != None:
        if str(member.id) in db["balance"]:
          if db["balance"][str(member.id)] != 0 and db["balance"][str(member.id)] > 150:
            if str(ctx.author.id) not in db["passive"]:
              if str(member.id) not in db["passive"]:
                if str(ctx.author.id) in db["balance"]:
                  chance = random.randint(0, 100)
                  if chance < 50:
                    try:
                      max = db["balance"][str(member.id)]
                      rng = random.randint(100, max)
                      db["balance"][str(member.id)] -= rng
                      db["balance"][str(ctx.author.id)] += rng
                      e = discord.Embed(title = "Success", description = f"You stole {rng} 💵 from {member}!",  color = random.randint(0, 16777215))
                      await ctx.send(embed = e)
                    except ValueError:
                      e = discord.Embed(title = "Error", description = "This person is too poor to be robbed!",  color = random.randint(0, 16777215))
                      await ctx.send(embed =e)
                      ctx.command.reset_cooldown(ctx)
                  else:
                    rng = random.randint(250, 1000)
                    db["balance"][str(member.id)] += rng
                    db["balance"][str(ctx.author.id)] -= rng
                    e = discord.Embed(title = "Fail", description = f"You got caught and lost {rng} 💵 !",  color = random.randint(0, 16777215))
                    await ctx.send(embed = e)
                else:
                  chance = random.randint(0, 100)
                  if chance < 50:
                    try:
                      db["balance"][str(ctx.author.id)] = 0
                      max = db["balance"][str(member.id)]
                      rng = random.randint(100, max)
                      db["balance"][str(member.id)] -= rng
                      db["balance"][str(ctx.author.id)] += rng
                      e = discord.Embed(title = "Success", description = f"You stole {rng} 💵 from {member.name}!",  color = random.randint(0, 16777215))
                      await ctx.send(embed = e)
                    except ValueError:
                      e = discord.Embed(title = "Error", description = "This person is too poor to be robbed!",  color = random.randint(0, 16777215))
                      await ctx.send(embed = e)
                  else:
                    db["balance"][str(ctx.author.id)] = 0
                    rng = random.randint(250, 1000)
                    db["balance"][str(member.id)] += rng
                    db["balance"][str(ctx.author.id)] -= rng
                    e = discord.Embed(title = "Fail", description = f"You got caught and lost {rng} 💵 !",  color = random.randint(0, 16777215))
                    await ctx.send(embed = e)
              else:
                e = discord.Embed(title = "Error", description = "Leave peaceful person alone!", color = random.randint(0, 16777215))
                await ctx.send(embed = e)
                ctx.command.reset_cooldown(ctx)
            else:
              e = discord.Embed(title = "Error", description = "You can't rob people in passive mode!", color = random.randint(0, 16777215))
              await ctx.send(embed = e)
              ctx.command.reset_cooldown(ctx)
          else:
            e = discord.Embed(title = "Error", description = "The person doesn't have any money!", color = random.randint(0, 16777215))
            await ctx.send(embed = e)
            ctx.command.reset_cooldown(ctx)
        else:
          e = discord.Embed(title = "Error", description = "The person doesn't have any money!", color = random.randint(0, 16777215))
          await ctx.send(embed = e)
          ctx.command.reset_cooldown(ctx)
      else:
        e = discord.Embed(title = "Error", description = "Choose someone to rob!", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
        ctx.command.reset_cooldown(ctx)
    else:
      e = discord.Embed(title = "Error", description = "You can't rob yourself!", color = random.randint(0, 16777215))
      await ctx.send(embed = e)
      ctx.command.reset_cooldown(ctx)

  #passive setting command
  @commands.command(aliases = ["pass"], help = "For people who don't want to get robbed", description = "Passive is for noobs\nHas cooldown of 30 minutes")
  @commands.cooldown(rate = 1, per = 1800, type = commands.BucketType.user)
  async def passive(self, ctx):
    if str(ctx.author.id) in db["passive"]:
      del db["passive"][str(ctx.author.id)]
      e = discord.Embed(title = "Success", description = "Youre now a normal person", color = random.randint(0, 16777215))
      await ctx.send(embed = e)
    else:
      db["passive"][str(ctx.author.id)] = True
      e = discord.Embed(title = "Success", description = "Youre now a passive person!", color = random.randint(0, 16777215))
      await ctx.send(embed = e)

  #search command
  @commands.command(aliases = ["find"], help = "Search for lost cash in places", description = "Some people may lost some of their cash like it fell out of pocket or something\nHas cooldown of 30 seconds")
  @commands.cooldown(rate = 1, per = 30, type = commands.BucketType.user)
  async def search(self, ctx):
    place = ["Car", "Forest", "House", "Grass", "Bushes", "Pocket", "Space", "Discord", "Castle", "Basement", "Street"]
    place1 = place.pop(random.randint(0, int(len(place) - 1)))
    place2 = place.pop(random.randint(0, int(len(place) - 1)))
    place3 = place.pop(random.randint(0, int(len(place) - 1)))
    view = discord.ui.View(timeout = 30)
    view.add_item(discord.ui.Select(placeholder = "Select an option", options = [discord.SelectOption(label = place1, emoji = "1️⃣", value = place1), discord.SelectOption(label = place2, emoji = "2️⃣", value = place2), discord.SelectOption(label = place3, emoji = "3️⃣", value = place3)]))
    e = discord.Embed(title = "Search", description = "Search one of places below to get some cash!", color = random.randint(0, 16777215))
    message = await ctx.send(embed = e, view = view)
    while True:
      try:
        interaction = await self.bot.wait_for("interaction", check = lambda interaction: interaction.message == message, timeout = 60)
        if interaction.user.id == ctx.author.id:
          if str(ctx.author.id) in db["balance"]:
            chance = random.randint(0, 100)
            if chance > 25:
              rng = random.randint(100, 500)
              db["balance"][str(ctx.author.id)] += rng
              e = discord.Embed(title = f"{ctx.author.name} searched: {view.children[0].values[0]}", description = f"You got {rng} 💵 !", color = random.randint(0, 16777215))
              await message.edit(embed = e, view = None)
              view.stop()
              break
            else:
              e = discord.Embed(title = f"{ctx.author.name} searched: {view.children[0].values[0]}", description = f"You failed...", color = random.randint(0, 16777215))
              await message.edit(embed = e, view = None)
              view.stop()
              break
          else:
            db["balance"][str(ctx.author.id)] = 0
            rng = random.randint(100, 500)
            db["balance"][str(ctx.author.id)] += rng
            e = discord.Embed(title = f"{ctx.author.name} searched: {view.children[0].values[0]}", description = f"You got {rng} 💵 !", color = random.randint(0, 16777215))
            await message.edit(embed = e, view = None)
            view.stop()
            break
        else:
          await interaction.send(content = "Sorry you can't use this menu!", ephemeral = True)
      except asyncio.TimeoutError:
        e = discord.Embed(title = f"{ctx.author.name} Didn't search anywhere", description = f"Oh okay.", color = random.randint(0, 16777215))
        await message.edit(embed = e, view = None)
        view.stop()
        break

  #shop command
  @commands.command(help = "See what you can buy with your cash", description = "Buy something (spoiler: youre poor)")
  async def shop(self, ctx):
    if str(ctx.author.id) in db["inventory"]:
      shop = '\n'.join(f'`{i+1}.` {item}: {price if "Discount card" not in db["inventory"][str(ctx.author.id)] else int(price * 0.75)}' for i, (price,item) in enumerate(sorted(((price,item) for item,price in db['shop'].items()),reverse=True)))
      e = discord.Embed(title = "Shop", description = shop, color = random.randint(0, 16777215))
      await ctx.send(embed = e)
    else:
      shop = '\n'.join(f'`{i+1}.` {item}: {price}' for i, (price,item) in enumerate(sorted(((price,item) for item,price in db['shop'].items()),reverse=True)))
      e = discord.Embed(title = "Shop", description = shop, color = random.randint(0, 16777215))
      await ctx.send(embed = e)

  #buy command
  @commands.command(help = "Buy a thing (that is useless)", description = "Youre poor")
  async def buy(self, ctx, *, itemnametext = None):
    if itemnametext != None:
      modtext = itemnametext.lower()
      itemname = modtext.capitalize()
      if itemname in db["shop"]:
        if str(ctx.author.id) in db["balance"]:
          if db["shop"].get(itemname) < db["balance"][str(ctx.author.id)] or int(db["shop"].get(itemname) * 0.75) < db["balance"][str(ctx.author.id)]:
            if str(ctx.author.id) in db["inventory"]:
              if itemname not in db["inventory"][str(ctx.author.id)]:
                if "Discount card" in db["inventory"][str(ctx.author.id)]:
                  db["balance"][str(ctx.author.id)] -= int(db["shop"].get(itemname) * 0.75)
                else:
                  db["balance"][str(ctx.author.id)] -= db["shop"].get(itemname)
                updateinv = db["inventory"][str(ctx.author.id)]
                updateinv[itemname] = 1
                db["inventory"][str(ctx.author.id)] = updateinv
                e = discord.Embed(title = "Shop", description = f"You got {itemname}!", color = random.randint(0, 16777215))
                await ctx.send(embed = e)
              else:
                db["balance"][str(ctx.author.id)] -= db["shop"].get(itemname)
                updateinv = db["inventory"][str(ctx.author.id)]
                updateinv[itemname] += 1
                db["inventory"][str(ctx.author.id)] = updateinv
                itemammount = db["inventory"][str(ctx.author.id)].get(itemname)
                e = discord.Embed(title = "Shop", description = f"You got {itemname}!", color = random.randint(0, 16777215))
                e.set_footer(text = f"Now you have {itemammount} {itemname}'s")
                await ctx.send(embed = e)
            else:
              db["inventory"][str(ctx.author.id)] = {}
              db["balance"][str(ctx.author.id)] -= db["shop"].get(itemname)
              updateinv = db["inventory"][str(ctx.author.id)]
              updateinv[itemname] = 1
              db["inventory"][str(ctx.author.id)] = updateinv
              e = discord.Embed(title = "Shop", description = f"You got {itemname}!", color = random.randint(0, 16777215))
              await ctx.send(embed = e)
          else:
            await ctx.send("You have not enough money")
        else:
          db["balance"][str(ctx.author.id)] = 0
          await ctx.send("Error: Get some money first!")
      else:
        await ctx.send("Error: You can't buy nothing!")
    else:
      await ctx.send("Error: You can't buy nothing!")

  #sell command
  @commands.command(help = "Sell any item you have", description = "Usage: pb!sell (item name)")
  async def sell(self, ctx, *, itemname = None):
    if itemname != None:
      modtext = itemname.lower()
      itemname = modtext.capitalize()
      if itemname in db["shop"]:
        if str(ctx.author.id) in db["balance"]:
          if str(ctx.author.id) in db["inventory"]:
            if itemname not in db["inventory"][str(ctx.author.id)]:
              e = discord.Embed(title = "Shop", description = "You can't sell nothing!", color = random.randint(0, 16777215))
              await ctx.send(embed = e)
            else:
              if db["inventory"][str(ctx.author.id)].get(itemname) >= 2:
                db["balance"][str(ctx.author.id)] += int(db["shop"].get(itemname) // 2)
                updateinv = db["inventory"][str(ctx.author.id)]
                updateinv[itemname] -= 1
                db["inventory"][str(ctx.author.id)] = updateinv
                itemammount = db["inventory"][str(ctx.author.id)].get(itemname)
                e = discord.Embed(title = "Shop", description = f"You sold {itemname}!", color = random.randint(0, 16777215))
                e.set_footer(text = f"Now you have {itemammount} {itemname}'s")
                await ctx.send(embed = e)
              else:
                db["balance"][str(ctx.author.id)] += int(db["shop"].get(itemname) // 2)
                updateinv = db["inventory"][str(ctx.author.id)]
                updateinv.pop(itemname)
                db["inventory"][str(ctx.author.id)] = updateinv
                itemammount = db["inventory"][str(ctx.author.id)].get(itemname)
                e = discord.Embed(title = "Shop", description = f"You sold {itemname}!", color = random.randint(0, 16777215))
                await ctx.send(embed = e)
          else:
            e = discord.Embed(title = "Shop", description = f"You can't sell nothing!", color = random.randint(0, 16777215))
            await ctx.send(embed = e)
        else:
          db["balance"][str(ctx.author.id)] = 0
          await ctx.send("Try again!")
      else:
        await ctx.send("Error: You can't selll nothing!")
    else:
      await ctx.send("Error: You can't sell nothing!")

  #inventory command
  @commands.command(aliases = ["storage", "backpack", "inv"], help = "See what do you have", description = "You can see what you have in your inventory (spoiler: youre poor)\nUsage: pb!inventory (@mention)")
  async def inventory(self, ctx, member: discord.Member = None):
    if member is None:
      if str(ctx.author.id) in db["inventory"] and db["inventory"][str(ctx.author.id)] != {}:
        inventory = "\n".join(f"{index}. `{name}`: {amount}" for index, (name, amount) in enumerate(db["inventory"][str(ctx.author.id)].items(), start = 1))
        e = discord.Embed(title = f"Inventory: {ctx.author}", description = inventory, color = random.randint(0, 16777215))
        await ctx.send(embed = e)
      else:
        e = discord.Embed(title = f"Inventory: {ctx.author}", description = "You have nothing right now", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
    else:
      if str(member.id) in db["inventory"] and db["inventory"][str(member.id)] != {}:
        inventory = "\n".join(f"{index}. `{name}`: {amount}" for index, (name, amount) in enumerate(db["inventory"][str(member.id)].items(), start = 1))
        e = discord.Embed(title = f"Inventory: {member}", description = inventory, color = random.randint(0, 16777215))
        await ctx.send(embed = e)
      else:
        e = discord.Embed(title = f"Inventory: {member}", description = "They have nothing right now", color = random.randint(0, 16777215))
        await ctx.send(embed = e)

  #hack command
  @commands.command(help = "Get data and sell it for money!", description = "Hacks random pepple\nRequirement: 1 Computer\nHas cooldown of 1 hour")
  @commands.cooldown(rate = 1, per = 3600, type = commands.BucketType.user)
  async def hack(self, ctx):
    if str(ctx.author.id) in db["balance"]:
      if str(ctx.author.id) in db["inventory"]:
        if "Computer" in db["inventory"][str(ctx.author.id)]:
          chance = random.randint(0, 1000)
          if chance > 350:
            rng = random.randint(250, 1500)
            db["balance"][str(ctx.author.id)] += rng
            e = discord.Embed(title = "Success", description = f"You hacked people and sold the data\nYou got {rng} 💵 !", color = random.randint(0, 16777215))
            await ctx.send(embed = e)
          else:
            db["balance"][str(ctx.author.id)] -= 2500
            e = discord.Embed(title = "You got caught by police", description = "You lost 2500 💵 !", color = random.randint(0, 16777215))
            await ctx.send(embed = e)
        else:
          e = discord.Embed(title = "Error", description = "Buy a computer!", color = random.randint(0, 16777215))
          await ctx.send(embed = e)
          ctx.command.reset_cooldown(ctx)
      else:
        db["inventory"][str(ctx.author.id)] = {}
        e = discord.Embed(title = "Error", description = "Buy a computer!", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
        ctx.command.reset_cooldown(ctx)
    else:
      e = discord.Embed(title = "Error", description = "Get some money and buy a computer!", color = random.randint(0, 16777215))
      await ctx.send(embed = e)
      ctx.command.reset_cooldown(ctx)

  #post meme command
  @commands.command(aliases = ["pm"], help = "Post memes and get money!", description = "Post memes and get money from it (spoiler: youre unfunny)\nRequirement: 1 Laptop")
  @commands.cooldown(rate = 1, per = 30, type = commands.BucketType.user)
  async def postmeme(self, ctx):
    if str(ctx.author.id) in db["balance"]:
      if str(ctx.author.id) in db["inventory"]:
        if "Laptop" in db["inventory"][str(ctx.author.id)]:
          view = discord.ui.View(timeout = 30)
          view.add_item(discord.ui.Select(placeholder = "Select an option", options = [discord.SelectOption(label = "Fresh", emoji = "1️⃣", value = "Fresh"), discord.SelectOption(label = "Repost", emoji = "2️⃣", value = "Repost"), discord.SelectOption(label = "Intellectual", emoji = "3️⃣", value = "Intellectual"), discord.SelectOption(label = "Copypasta", emoji = "4️⃣", value = "Copypasta"), discord.SelectOption(label = "Kind", emoji = "5️⃣", value = "Kind")]))
          e = discord.Embed(title = "Post meme", description = "Post one of meme types below to get some cash!", color = random.randint(0, 16777215))
          message = await ctx.send(embed = e, view = view)
          while True:
            try:
              interaction = await self.bot.wait_for("interaction", check = lambda interaction: interaction.message == message, timeout = 60)
              if interaction.user.id == ctx.author.id:
                if str(ctx.author.id) in db["balance"]:
                  chance = random.randint(0, 100)
                  if chance > 45:
                    rng = random.randint(250, 1000)
                    db["balance"][str(ctx.author.id)] += rng
                    e = discord.Embed(title = f"{ctx.author.name} posted: {view.children[0].values[0]}", description = f"You got {rng} 💵 !", color = random.randint(0, 16777215))
                    await message.edit(embed = e, view = None)
                    view.stop()
                    break
                  else:
                    e = discord.Embed(title = f"{ctx.author.name} searched: {view.children[0].values[0]}", description = f"You failed...", color = random.randint(0, 16777215))
                    await message.edit(embed = e, view = None)
                    view.stop()
                    break
                else:
                  db["balance"][str(ctx.author.id)] = 0
                  rng = random.randint(250, 1000)
                  db["balance"][str(ctx.author.id)] += rng
                  e = discord.Embed(title = f"{ctx.author.name} posted: {view.children[0].values[0]}", description = f"You got {rng} 💵 !", color = random.randint(0, 16777215))
                  await message.edit(embed = e, view = None)
                  view.stop()
                  break
              else:
                await interaction.send(content = "Sorry you can't use this menu!", ephemeral = True)
            except asyncio.TimeoutError:
              e = discord.Embed(title = f"{ctx.author.name} Didn't post anything", description = f"Oh okay.", color = random.randint(0, 16777215))
              await message.edit(embed = e, view = None)
              view.stop()
              break

        else:
          e = discord.Embed(title = "Error", description = "Buy a laptop!", color = random.randint(0, 16777215))
          await ctx.send(embed = e)
          ctx.command.reset_cooldown(ctx)
      else:
        db["inventory"][str(ctx.author.id)] = {}
        e = discord.Embed(title = "Error", description = "Buy a laptop!", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
        ctx.command.reset_cooldown(ctx)
    else:
      e = discord.Embed(title = "Error", description = "Get some money and buy a laptop!", color = random.randint(0, 16777215))
      await ctx.send(embed = e)
      ctx.command.reset_cooldown(ctx)

  #mail command
  @commands.command(aliases = ["send", "dm", "text"], help = "Mail someone with the bot", description = "You can mail someone with this command\nRequirement: Both you and mentioned member must have atleast 1 smartphone\nExample: pb!mail @Number1#4325 oh hi")
  async def mail(self, ctx, member: discord.Member, *, text = ""):
    if str(ctx.author.id) in db["inventory"]:
      if "Smartphone" in db["inventory"][str(ctx.author.id)]:
        if str(member.id) in db["inventory"]:
          if "Smartphone" in db["inventory"][str(member.id)]:
            e = discord.Embed(title = "New mail", description = text, color = random.randint(0, 16777215))
            e.set_author(name = str(ctx.author), icon_url = str(ctx.author.avatar)[:-10])
            e.set_footer(text = "You have 5 minutes to respond")
            if ctx.message.attachments:
              e.set_image(url = str(ctx.message.attachments).split(" ")[3][5:-1])
            await member.send(embed = e)
            await ctx.message.add_reaction("✅")
            e = discord.Embed(title = "Success", description = f"Sent `{text}` to `{member}`!", color = random.randint(0, 16777215))
            await ctx.send(embed = e)
            try:
              message = await self.bot.wait_for("message", check = lambda message: message.author == member and message.channel == member.dm_channel, timeout = 300)
              await message.add_reaction("✅")
              e = discord.Embed(title = f"Response from mailed user ({member})", description = message.content, color = random.randint(0, 16777215))
              if message.attachments:
                e.set_image(message.attachments[0].url)
              await ctx.reply(embed = e)
            except asyncio.TimeoutError:
              e = discord.Embed(title = f"No response from mailed user ({member})", color = random.randint(0, 16777215))
              await ctx.reply(embed = e, mention_author = False)
          else:
            e = discord.Embed(title = "Error", description = f"Sorry you can't message {member}\n{member.name} has no smartphone!", color = random.randint(0, 16777215))
            await ctx.send(embed = e)
        else: 
          e = discord.Embed(title = "Error", description = f"Sorry you can't message {member}\n{member.name} has no smartphone!", color = random.randint(0, 16777215))
          await ctx.send(embed = e)
      else: 
        e = discord.Embed(title = "Error", description = f"Sorry you can't message {member}\nYou have no smartphone!", color = random.randint(0, 16777215))
        await ctx.send(embed = e)
    else: 
      e = discord.Embed(title = "Error", description = f"Sorry you can't message {member}\nYou have no smartphone!", color = random.randint(0, 16777215))
      await ctx.send(embed = e)

  #profile command
  @commands.command(aliases = ["prof"], help = "See user's economical info!", description = "You can see their inventory and balance!\nUsage: pb!profile @mention")
  async def profile(self, ctx, member: discord.Member = None):
    money = 0
    inventory = "Nothing here"
    passive = "False"
    if member == None:
      if str(ctx.author.id) in db["balance"]:
        money = db["balance"][str(ctx.author.id)]
      if str(ctx.author.id) in db["inventory"]:
        inventory = "\n".join(f"{index}. `{name}`: {amount}" for index, (name, amount) in enumerate(db["inventory"][str(ctx.author.id)].items(), start = 1))
      if str(ctx.author.id) in db["passive"]:
        passive = "True"

      e = discord.Embed(title = f"{ctx.author.name}'s profile", description = f"Balance: {money} 💵\nPassive: {passive}", color = random.randint(0, 16777215))
      e.set_thumbnail(url = ctx.author.avatar)
      e.add_field(name = "Inventory", value = inventory, inline = False)
      await ctx.send(embed = e)
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
      await ctx.send(embed = e)


def setup(bot):
  bot.add_cog(Economy(bot))