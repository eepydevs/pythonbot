#cog by DancingSmurf#0444
# Auto format this as much as you want!
import disnake as discord
from disnake.ext import commands
import asyncio
import random
from replit import db

def textSM(text):
	wordlist = text.lower().split(" ")
	for i in range(len(wordlist)):
		if not wordlist[i].endswith("s"):
			continue
		else:
			return f"{text} are good"
	return f"{text} is good"

class TestingCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(help="I do not know!", description="Usage: pb!test")
    async def test(self, ctx):
        await ctx.send("Testing command! My first ever command.")
        
    @commands.command(help="Second command! This time, with a text paramater! Still do not know what it does though.", description="Usage: pb!texttest (text)")
    async def texttest(self, ctx, *, text = None):
        if text == None:
            await ctx.send("No text found! Please add text for it to work.")
        else:
            await ctx.send(f"Testing command! My second ever command.\nAlso {textSM(text)}!")
            
    @commands.command(help="I do not know! Now with a number and text parameter.", description="Usage: pb!nwpttest")
    async def nwpttest(self, ctx, number, *, text):
        await ctx.send(f"Testing command! My third ever command. {number}, {text}. What do they have in common? They are all typed by {ctx.author.name}!")
        
    @commands.command(help="Calculator, but wrong. Addition only supported right now.", description="Usage: pb!calcwrong number1 number2")
    async def calcwrong(self, ctx, number1, number2):
        try:
            await ctx.send(f"{number1} + {number2} = {random.randint(-int(number1), int(number2))}")
        except ValueError:
            await ctx.send("Something went wrong...")

def setup(bot):
    bot.add_cog(TestingCommands(bot))
