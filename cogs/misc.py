import discord
from discord.ext import commands

class misc(commands.Cog):
    
    def __init__(self, bot): 
        self.bot = bot

    #Uppercase and lowercases message
    @discord.slash_command()
    async def mock(self, ctx, message):

        mocked = ""

        for idx, element in enumerate(message):
            if(idx % 2):
                mocked += (element.upper())
            else:
                mocked += (element.lower())
        
        await ctx.respond(mocked)

    #Give me my userID
    @discord.slash_command()
    async def user_id(self, ctx: discord.ApplicationContext):

        await ctx.respond(ctx.author.id)

    @discord.command(description="Sends the bot's latency.") # this decorator makes a slash command
    async def ping(self,ctx): # a slash command will be created with the name "ping"
        await ctx.respond(f"Pong! Latency is {self.bot.latency}")

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(misc(bot)) # add the cog to the bot