import discord

def createEmbed():

    standardEmbed = discord.Embed(color=discord.Colour.blurple())

    standardEmbed.add_field(name = "test", value = "")
    standardEmbed.set_footer(text="Have a nice day!", icon_url="https://media.discordapp.net/attachments/940448492785123409/1056009958614908928/ABGlogoC.png")

    return standardEmbed

standardEmbed = createEmbed()