#cog by Number1#4325
import asyncio
import disnake as discord
import random
import os
import datetime, time
from replit import db
from disnake.ext import commands

class Errors(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  #when error event
  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.CommandNotFound):
      return
    e = discord.Embed(title = "Error", description = f"Triggered by: `{ctx.message.content}` from {ctx.author}\n```{error}```", color = random.randint(0, 16777215))
    await ctx.send(embed = e)

def setup(bot):
  bot.add_cog(Errors(bot))