#autoResponse.py

#Ability to add a trigger word that will ellict a response from bot
#Stored in a csv file that is loaded into dictionary

import csv
import discord
from discord.ext import commands

#from embedTemplates import standardEmbed

def createEmbed():

    standardEmbed = discord.Embed(color=discord.Colour.blurple())

    standardEmbed.add_field(name = "test", value = "")
    standardEmbed.set_footer(text="Have a nice day!", icon_url="https://media.discordapp.net/attachments/940448492785123409/1056009958614908928/ABGlogoC.png")

    return standardEmbed

standardEmbed = createEmbed()

class autoResponse(commands.Cog):

    def __init__(self, bot): 
        self.bot = bot
        self.responses : dict = {}
        
    #setup
    @commands.Cog.listener()
    async def on_ready(self):
        #Load up the responses from text file
        print(f'autoResponse setup complete')
        self.responses = readCSV()
        await self.bot.guilds[0].channels[3].send("MAN IS A BITCH")
        #set up standard Embed

    #check for trigger in message
    @commands.Cog.listener()
    async def on_message(self,message):
        #So bot doesn't echo its own responses
        if message.author == self.bot.user:
            return

        #checks each word in the message
        wordsInMessage = message.content.split()

        #for each word in the message checks if it needs a response
        for content in wordsInMessage:
            if content in self.responses:
                await message.channel.send(self.responses[content])

    async def add_trigger_override(self,ctx,trigger,response):

        standardEmbed.set_field_at(0,name = f"The trigger \"{trigger}\" already has the response \"{self.responses[trigger]}\" would you like to override it? ",value = "You have 60 seconds to respond" )
        
        await ctx.respond(embed = discord.Embed(description="Override"))
        question = await ctx.send(embed = standardEmbed)

        await question.add_reaction('✅')
        await question.add_reaction('❌')
        
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '✅' and reaction.message == question 

        try:
            await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except discord.asyncio.TimeoutError:
            return
        else:
            removeNewTrigger(trigger, self.responses)

        writeNewTrigger(trigger, response, self.responses)

        standardEmbed.set_field_at(0,name = f"The trigger \"{trigger}\" with response \"{response}\" have been added!",value = "Success!")
        await question.delete()
        await ctx.edit(embed = standardEmbed)

        
        
    #allows user to adds triggers
    @discord.slash_command()
    async def add_trigger(self,ctx, trigger, response):

        #if the trigger already exists
        if trigger in self.responses:
            if (self.responses[trigger] == response):
                standardEmbed.set_field_at(0,name = f"The trigger \"{trigger}\" with response \"{response}\" already existed",value = "Success?")
                await ctx.respond(embed = standardEmbed)
                return 
            
            #check if the user wants to override old response
            await self.add_trigger_override(ctx,trigger,response)
            return
            
        
        #writes to the csv file
        writeNewTrigger(trigger, response, self.responses)

        standardEmbed.set_field_at(0,name = f"The trigger \"{trigger}\" with response \"{response}\" have been added!",value = "Success!")
        await ctx.respond(embed = standardEmbed)

    #removal of triggers
    @discord.slash_command()
    async def remove_trigger(self, ctx, trigger):

        if not trigger in self.responses:
            standardEmbed.set_field_at(0,name = "Error",value = f"The trigger: \"{trigger}\" is not in the registry of valid triggers")
            await ctx.respond(embed = standardEmbed)
            return 

        response = self.responses[trigger]
        
        #writes to the csv file
        removeNewTrigger(trigger, self.responses)

        standardEmbed.set_field_at(0,name = "Success",value = f"The trigger: {trigger} and response: {response} have been succesfully removed!")
        await ctx.respond(embed = standardEmbed)

#Utility functions

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(autoResponse(bot)) # add the cog to the bot

#reads the triggers csv and adds it to a dictionary
def readCSV() -> dict:

    #dictionary to return with processed triggers and responses
    responses = {}

    # opening the CSV file
    with open('triggerResponses.csv', mode ='r')as file:
        #reading the CSV file
        csvFile = csv.reader(file)
        # adding the contents of the CSV file to the dict
        for lines in csvFile:
            #adds to a dictionary
            responses[lines[0]] = lines[1]

    return responses

def removeNewTrigger(trigger: str, responses: dict):
    
    # opening the CSV file for appending
    with open('triggerResponses.csv', mode ='w')as file:
        #appending to the CSV file
        csvFile = csv.writer(file)
    
        #removes from dictionary
        responses.pop(trigger)

        #adds to csv file
        buildCSV(responses, csvFile)
       
def buildCSV(responses: dict, csvFile: csv.writer):

    for trigger, response in responses.items():
        csvFile.writerow([trigger,response])

def writeNewTrigger(trigger: str, response: str, responses: dict):
    
    # opening the CSV file for appending
    with open('triggerResponses.csv', mode ='a')as file:
        #appending to the CSV file
        csvFile = csv.writer(file)
    
        #adds to a dictionary
        responses[trigger] = response
        #adds to csv file
        csvFile.writerow([trigger,response])
