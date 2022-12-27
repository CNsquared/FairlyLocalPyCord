#guessWhoSaidIt.py

import csv
import discord
import random
from discord.ext import commands

class guessWhoSaidIt(commands.Cog):
    
    def __init__(self, bot): 
        self.bot = bot

    #check for trigger in message
    @discord.slash_command()
    async def set_up_guess_who_said_it(self,ctx: discord.ApplicationContext):

        await ctx.respond("setting up the game")
       
        messages = await ctx.channel.history(limit=5000000).flatten()
        for message in messages:
            if(not message.author.bot):
                writeNewMessage(message,ctx.channel.name)

        await ctx.respond("finished setting up the game")

    @discord.slash_command(description="Play the game with messages in a specified channel")
    async def play_guess_who_said_it(self,ctx: discord.ApplicationContext,channel = "google-hangouts", month_option = False):
        
        fileName = f"./cogs/guessWhoSaidIt/guessWhoSaidIt_{channel}.csv"
        entries = readCSV(fileName)
        if(len(entries) == 0):
            await ctx.respond(f"{channel} has not been setup to play. Please set it up or select another channel")
            return
        
        chosenMessage = "test"
        hintMessage = ""
        attempts = 0

        while(len(chosenMessage) < 10):
            chosenMessage, answerKey = random.choice(entries)

        hintMessage, hintAnswer = random.choice(entries)
        while(hintMessage == chosenMessage or hintAnswer[0] != answerKey[0]):
            hintMessage, hintAnswer = random.choice(entries)

        answerAlias = set()

        if(answerKey[0] == "KnEx"):
            alias = ["matt", "wong", "knex"]
            for name in alias:
                answerAlias.add(name)
        elif(answerKey[0] == "CNsquared"):
            alias = ["alex", "cnsquared"]
            for name in alias:
                answerAlias.add(name)
        elif(answerKey[0] == "Hyru"):
            alias = ["eric", "hyru"]
            for name in alias:
                answerAlias.add(name)
        elif(answerKey[0] == "Laeloria"):
            alias = ["aaron", "laeloria"]
            for name in alias:
                answerAlias.add(name)
        elif(answerKey[0] == "Thew"):
            alias = ["blake", "thew"]
            for name in alias:
                answerAlias.add(name)
        elif(answerKey[0] == "bellebuddy"):
            alias = ["man", "bellebuddy", "bitch"]
            for name in alias:
                answerAlias.add(name)
        elif(answerKey[0] == "its_ash"):
            alias = ["ashley", "ashpee","ashpee uwu","glodking2011","glod","glodking", "its_ash"]
            for name in alias:
                answerAlias.add(name)
        elif(answerKey[0] == "kp"):
            alias = ["kait", "kpissy", "mid", "kp"]
            for name in alias:
                answerAlias.add(name)

        
        author = False
        if(month_option):
            month = False
        else:
            month = True
        embed = discord.Embed(title="Guess Who Said It!",color=discord.Colour.blurple())
        embed.set_author(name= f"Number of tries left: {3 - attempts}")
        embed.add_field(name = "Message", value = f"{chosenMessage}", inline = False)
        embed.add_field(name = "Author", inline=True, value = "UNKOWN")
        if (month_option):
            embed.add_field(name = "Month", inline=True, value = "UNKOWN")
        embed.set_footer(text="Have a nice day!", icon_url="https://media.discordapp.net/attachments/940448492785123409/1056009958614908928/ABGlogoC.png")

        await ctx.respond(embed = discord.Embed(title= "Yay lets play"))
        game = await ctx.send(embed = embed)

        while((not author) or (not month)):
            if(attempts == 3):
                embed = discord.Embed(title="Guess Who Said It!",color=discord.Colour.blurple())
                embed.add_field(name = "YAY YOU LOST", value = f"{answerKey[0]} said \"{chosenMessage}\"", inline = False)
                await game.edit(embed=embed)
                return

            guess :str
            try:
                def check(message): 
                    nonlocal guess
                    nonlocal attempts
                    guess = message.content
                    return guess.startswith('guess: ') and message.channel == ctx.channel

                await self.bot.wait_for('message', timeout=30.0, check=check)
            except discord.asyncio.exceptions.TimeoutError:
                embed = discord.Embed(title="Guess Who Said It!",color=discord.Colour.blurple())
                embed.add_field(name = "YAY YOU LOST", value = f"{answerKey[0]} said \"{chosenMessage}\"", inline = False)
                await game.edit(embed=embed)
                await ctx.respond(embed = discord.Embed(title = "No one responded D:", description = "Timeout" ))
                return

            guess = guess[7:]
            attempts += 1

            if(guess.lower() in answerAlias):
                author = True
                embed.set_author(name= f"Number of tries left: {3 - attempts}")
                embed.set_field_at(1, name = "Author",value = answerKey[0])
                await game.edit(embed = embed)
                continue
                
            if(guess == answerKey[1][5:7]):
                month = True
                embed.set_author(name= f"Number of tries left: {3 - attempts}")
                embed.set_field_at(2, name = "Month", value = answerKey[1][5:7])
                await game.edit(embed = embed)
                continue
            
            embed.set_footer(text= f"{guess} is not corrrect!", icon_url="https://media.discordapp.net/attachments/940448492785123409/1056009958614908928/ABGlogoC.png")
            embed.set_author(name= f"Number of tries left: {3 - attempts}")
            if((3 - attempts) == 1):
                embed.add_field(name = "This person also said:", value = f"{hintMessage}", inline = False)
            await game.edit(embed = embed)

        embed = discord.Embed(title="Guess Who Said It!",color=discord.Colour.blurple())
        embed.add_field(name = "YAY YOU WON", value = f"{answerKey[0]} said \"{chosenMessage}\"", inline = False)
        await game.edit(embed=embed)
                

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(guessWhoSaidIt(bot)) # add the cog to the bot

def writeNewMessage(message : discord.message.Message, channel :str ):
    fileName = f"./cogs/guessWhoSaidIt/guessWhoSaidIt_{channel}.csv"
    with open(fileName, mode ='a')as file:
        #writing to the CSV file
        csvFile = csv.writer(file)

        #write to csv file
        csvFile.writerow([message.author.name, message.created_at.date(), message.channel, message.content])

#reads the triggers csv and adds it to a dictionary
def readCSV(fileName) -> list:

    #dictionary to return with processed triggers and responses
    responses = []

    # opening the CSV file
    try:
        with open(fileName, mode ='r')as file:
            #reading the CSV file
            csvFile = csv.reader(file)
            # adding the contents of the CSV file to the dict
            for lines in csvFile:
                #adds to a dictionary
                responses.append( (lines[3],(lines[0],lines[1],lines[2])) )              
    except FileNotFoundError:
        return responses

    return responses
       