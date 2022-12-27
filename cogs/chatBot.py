#chatBot.py

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

import discord
from discord.ext import commands
import random

#Modal to take 
class responseFeedbackForm(discord.ui.Modal):
    def __init__(self, messageToLearn, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.messageToLearn = messageToLearn
        self.add_item(discord.ui.InputText(label = "response"))

    async def callback(self, interaction: discord.Interaction):

        #on press of the button create a chatBot to record and learn the returned new response
        bot = ChatBot("Learning")
        trainer = ListTrainer(bot)

        convo = [self.messageToLearn ,self.children[0].value]

        #Can make it learn multiple times 
        for i in range(1):
            trainer.train(convo)
        print(f"trained response \"{self.children[0].value}\" for message \"{self.messageToLearn}\"")
        
        await interaction.response.send_message("Thanks for the feedback!")

class responseFeedbackPrompt(discord.ui.View):

    def __init__(self, messageToLearn, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.messageToLearn = messageToLearn

    @discord.ui.button(label="Change Response")
    async def button_callback(self, button, interaction : discord.Interaction):
        await interaction.response.send_modal(responseFeedbackForm(messageToLearn=self.messageToLearn,title=f"Response"))

class chatbot(commands.Cog):

    def __init__(self, bot): 
        self.bot = bot
        self.chatbot : ChatBot
        self.exit_conditions = (":q", "quit", "exit","shut up")
        self.enter_conditions = [":s", "start", "enter","talk","start learning"]
        self.responding = False


    @discord.slash_command()
    async def modal_slash(self, ctx: discord.ApplicationContext):
        """Shows an example of a modal dialog being invoked from a slash command."""
        modal = responseFeedbackForm(title=f"Respond to bob")
        await ctx.send_modal(modal)

     #setup
    @commands.Cog.listener()
    async def on_ready(self):
        self.chatbot = ChatBot("Learning", logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
            }
        ])
        self.enter_conditions.append(self.bot.user.mention)
        print(f'ChatBot setup complete')

    @discord.slash_command()
    async def learn_english(self, ctx: discord.ApplicationContext):

        await ctx.respond("Learning English")
        trainer = ListTrainer(self.chatbot)

        responses = []

        # opening the CSV file
        with open('./cogs/training/greetings.txt', mode ='r')as file:
            
            for lines in file:
                #adds to a dictionary
                responses.append(lines)

        trainer.train(responses)

        await ctx.respond("Done Learning greetings")

    @discord.slash_command()
    async def refresh(self, ctx: discord.ApplicationContext):

        await ctx.respond("Refreshing chatbot")

        self.chatbot = ChatBot("Learning", logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
            }
        ])        


    @commands.Cog.listener()
    async def on_message(self,message : discord.Message):

        #only responds to text not images or embeds
        if not message.content:
            return

        #check that message is from human
        if message.author.bot:
            return

        if message.content in self.exit_conditions:
            self.responding = False
            await message.reply(f"I'll shut up now")
            return

        if message.content in self.enter_conditions:
            self.responding = True
            await message.reply(f"I'll be listening now")
            return

        if(not self.responding and (not message.channel.name == "train-ai")):
            return

        #get response
        response = self.chatbot.get_response(message.content)
        if(not str(response)):
            return
        
        #if the response is more than 30% confident then send response
        if(response.confidence > .30):
            sent = await message.channel.send(f"{response}")
            feedback = await self.feedbackOnResponse(sent,message)
            await self.learning(feedback, response, message)
        else:
            sent = await message.channel.send(f"I'm not sure how to respond to \"{message.content}\". Could you tell me?", view = responseFeedbackPrompt(messageToLearn=message.content), mention_author = False)

        print(f"I'm {response.confidence * 100}% confident to respond to {message.content } with {response}")
    
    async def feedbackOnResponse(self, sent : discord.Message, message: discord.Message):
        
        await sent.add_reaction('✅')
        await sent.add_reaction('❌')

        #determines if feedbakc was recieved and what it was
        #0 is no, 1 is yes and 3 is no feedback
        emojiResponse = 0

        def check(reaction, user) -> bool:

            reacted = ((str(reaction.emoji) == '✅') or (str(reaction.emoji) == '❌')) and reaction.message == sent 
            nonlocal emojiResponse
            if((str(reaction.emoji) == '✅')):
                emojiResponse = 1

            return reacted 

        print(f"waiting for feedback on {message.content}")
        try:
            await self.bot.wait_for('reaction_add', check=check, timeout= 30)
        except discord.asyncio.TimeoutError:
            print(f"No feedback on {message.content}")
            await sent.clear_reactions()
            return 3

        print(f"recieved for feedback on {message.content}")

        return emojiResponse
    
    async def learning(self,emojiResponse, response, message: discord.Message):
    
        if (emojiResponse == 1):
            self.train(message.content, str(response))
        else:
  
            await message.reply(view = responseFeedbackPrompt(messageToLearn= message.content), mention_author = False)


    def train(self, message, response):
        trainer = ListTrainer(self.chatbot)

        convo = [message,response]

        for i in range(1):
            trainer.train(convo)
        print(f"trained response \"{response}\" for message \"{message}\"")


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(chatbot(bot)) # add the cog to the bot

