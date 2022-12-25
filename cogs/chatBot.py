#chatBot.py

from chatterbot import ChatBot
import discord
from discord.ext import commands

class chatBot(commands.Cog):

    def __init__(self, bot): 
        self.bot = bot
        self.chatbot : ChatBot
        self.exit_conditions = (":q", "quit", "exit","shut up")
        self.enter_conditions = (":s", "start", "enter","talk","start learning")
        self.responding = True

     #setup
    @commands.Cog.listener()
    async def on_ready(self):
        self.chatbot = ChatBot("Learning", logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                #'default_response': 'I am sorry, but I do not understand.',
                #'maximum_similarity_threshold': 0.5
            }
        ])
        print(f'ChatBot setup complete')

    @discord.slash_command()
    async def learn(self, ctx: discord.ApplicationContext):

        await ctx.respond("Learning")

        async for message in ctx.channel.history(limit=5000000):
            if message.author.bot:
                continue
            self.chatbot.get_response(message.content)
            print(message.content)
       

        await ctx.respond("Done Learning")


    @commands.Cog.listener()
    async def on_message(self,message):

        if message.author.bot:
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

        response = self.chatbot.get_response(message.content)

        if(str(response) == "I am sorry, but I do not understand."):
            print(f"Didnt come up with a response for {message.content}")
            return

        if(not str(response)):
            return
        
        await message.channel.send(response)
        




def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(chatBot(bot)) # add the cog to the bot