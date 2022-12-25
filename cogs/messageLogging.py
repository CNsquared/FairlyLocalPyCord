# messageLogging.py

#logs all messages sent in the server

import csv
import discord
from discord.ext import commands

class messageLogging(commands.Cog):
    
    def __init__(self, bot): 
        self.bot = bot

    #check for trigger in message
    @commands.Cog.listener()
    async def on_message(self,message):
        #Only looks for messages of humans
        if message.author.bot:
            return

        writeNewMessage(message)


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(messageLogging(bot)) # add the cog to the bot

def writeNewMessage(message : discord.message.Message ):
    with open('messageLog.csv', mode ='a')as file:
        #writing to the CSV file
        csvFile = csv.writer(file)

        time = f'{message.created_at.date()} {message.created_at.time().hour}:{message.created_at.time().minute}:{message.created_at.time().second}'

        #write to csv file
        csvFile.writerow([message.author.name, time, message.channel, message.content])
       


