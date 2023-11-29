import discord
import os
from dotenv import load_dotenv

#Setup
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = discord.Bot(intents=discord.Intents.all(), activity=discord.Game(name='Ape Sex Leg Leg'))
cogs_list = [
    #'autoResponse',
    'messageLogging',
    'myTexts',
    'stalking',
    'misc',
    'chatBot',
    'guessWhoSaidIt'
]

#Load Cogs
for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')

@bot.user_command(name="Say Hello")
async def hi(ctx, user):
    await ctx.respond(f"{ctx.author.mention} says hello to {user.name}!")

bot.run("MTA1NDYyNTgyNzY5NTg4NjQzNw.GJiM5y.42U9TDZkh1i9f4cV3xhtxuk-pOxRvgpZjQ2cfg")


