import csv
import discord
import random
from discord.ext import commands

class myTexts(commands.Cog):
    
    def __init__(self, bot): 
        self.bot = bot
        
        
    #check for trigger in message
    @discord.slash_command()
    async def pull_messages_from_channel(self,ctx: discord.ApplicationContext):

        await ctx.respond("Reading")

        messages = await ctx.channel.history( ).flatten()
        await ctx.respond("Pulled Messages")
        for message in messages:
            if(not message.author.bot and message.author.name == "cn.squared" and message.content != "" and not message.content.startswith("```")):
                writeNewMessage(message)

        await ctx.respond("Messages saved in csv")
        
def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(myTexts(bot)) # add the cog to the bot        
    
def writeNewMessage(message : discord.message.Message):
    
        message.content = message.content.replace("\n"," ")
    
        fileName = f"./cogs/myTexts/alex.csv"
        with open(fileName, mode ='a')as file:
            #writing to the CSV file
            csvFile = csv.writer(file)
            #write to csv file
            csvFile.writerow([message.author.name, message.created_at.date(), message.content])
            
