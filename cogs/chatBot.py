#chatBot.py

from chatterbot import ChatBot
import discord
from discord.ext import commands

class chatBot(commands.Cog):

    def __init__(self, bot): 
        self.bot = bot
        self.chatbot = ChatBot("Chatpot")
        self.exit_conditions = (":q", "quit", "exit","shut up")
        self.enter_conditions = (":s", "start", "enter","talk","start learning")
        self.responding = False
        self.messageCount = 0

    @commands.Cog.listener()
    async def on_message(self,message):

        

        if message.author == self.bot.user:
            return

        if message.content in self.exit_conditions:
            self.responding = False
            print("responding off")
            return

        if message.content in self.enter_conditions:
            self.responding = True
            print("responding activated")
            return

        if not self.responding:
            print("not learning right now")
            return

    
        print(f"🪴 {self.chatbot.get_response(message.content)}") 
        self.messageCount += 1
        if(self.messageCount == 100):
            self.messageCount = 0
            self.chatbot = ChatBot("Learning")



def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(chatBot(bot)) # add the cog to the bot