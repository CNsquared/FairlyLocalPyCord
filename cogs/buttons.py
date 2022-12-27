#buttons.py

import discord

class responseFeedbackPrompt(discord.ui.View):

    @discord.ui.button(label="Change Response")
    async def button_callback(self, button, interaction : discord.Interaction):
        #await interaction.response.send_modal(responseFeedbackForm(title=f"Response"))
        pass