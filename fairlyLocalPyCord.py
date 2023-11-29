import discord
import os

#Setup
bot = discord.Bot(intents=discord.Intents.all(), activity=discord.Game(name='Ape Sex Leg Leg'))
cogs_list = [
    #'autoResponse',
    'messageLogging',
    'myTexts',
    'stalking',
    'misc',
    #'chatBot',
    'guessWhoSaidIt'
]

#Load Cogs
for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')

@bot.user_command(name="Say Hello")
async def hi(ctx, user):
    await ctx.respond(f"{ctx.author.mention} says hello to {user.name}!")

bot.run("MTA1NDYyNTgyNzY5NTg4NjQzNw.GNNlSn.n2H3nsYLLLer7Oa8LKMcjS9ZB3mfAPgjeCYt_E")


