from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

import discord

# Modal to take 
class responseFeedbackForm(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label = "response"))
 

    async def callback(self, interaction: discord.Interaction):

        #on press of the button create a chatBot to record and learn the returned new response
        bot = ChatBot("Learning")
        trainer = ListTrainer(bot)

        global messageToLearn
        convo = [messageToLearn ,self.children[0].value]

        #Can make it learn multiple times 
        for i in range(1):
            trainer.train(convo)
        print(f"trained response \"{self.children[0].value}\" for message \"{messageToLearn}\"")
        
        await interaction.response.send_message("Thanks for the feedback!")