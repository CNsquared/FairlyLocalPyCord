#stalking.py

#watches user activity and comments on it

import discord
from discord.ext import commands

#from embedTemplates import standardEmbed

def createEmbed():

    standardEmbed = discord.Embed(color=discord.Colour.blurple())

    standardEmbed.add_field(name = "test", value = "")
    standardEmbed.set_footer(text="Have a nice day!", icon_url="https://media.discordapp.net/attachments/940448492785123409/1056009958614908928/ABGlogoC.png")

    return standardEmbed

standardEmbed = createEmbed()

class stalking(commands.Cog):
    
    def __init__(self, bot): 
        self.bot = bot
        self.relevantUsers = set()
        #starts of as string name of channel and is reassgined the channel object
        self.relevantChannel = "cse-12"

    def peopleListeningSpotify(self) -> set:
        peopleListening = set()
        for member in self.relevantUsers:
                for activity in member.activities:
                    if(type(activity) == discord.Spotify):
                        peopleListening.add(member)
        return peopleListening

    def relevantUsersOnline(self) -> set:

        peopleOnline = set()
        for member in self.relevantUsers:
            if not str(member.status) == "offline":
                peopleOnline.add(member)

        return peopleOnline

    #setup
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Stalking setup complete')

        #SPECIFIC TO ONLY IN 1 GUILD
        channels = self.bot.guilds[0].channels

        for channel in channels:
            if channel.name == self.relevantChannel:
                break
        for member in channel.members:
            if not member.bot:
                self.relevantUsers.add(member)
        self.relevantChannel = channel


    #give the option to reveal deleted messages
    @commands.Cog.listener()
    async def on_message_delete(self,message : discord.message.Message):

        #only cares if humans delete their messages
        if message.author.bot:
            return
        
        standardEmbed.set_field_at(0,value = "Message Deleted",name = f"{message.author.name}'s message was deleted would you like to see it?")
        question = await message.channel.send(embed = standardEmbed)
        await question.add_reaction('✅')
        await question.add_reaction('❌')
        
        def check(reaction, user):
            return (str(reaction.emoji) == '✅') and reaction.message == question 
    
        
        await self.bot.wait_for('reaction_add', check=check)

        standardEmbed.set_field_at(0,name = "Message Deleted",value = f"{message.author.name} said \"{message.content}\"")
        await question.edit(embed = standardEmbed)

    #give the option to reveal edited messages
    @commands.Cog.listener()
    async def on_message_edit(self,before : discord.message.Message, after:discord.message.Message):

        #only cares if humans delete their messages
        if before.author.bot:
            return
        
        standardEmbed.set_field_at(0,value = "Message Edited",name = f"{before.author.name}'s message was edited would you like to see the original?")
        question = await before.reply(embed = standardEmbed,mention_author = False)
        #await before.reply(embed = discord.Embed("This One"))
        await question.add_reaction('✅')
        await question.add_reaction('❌')
        
        def check(reaction, user):
            return (str(reaction.emoji) == '✅') and reaction.message == question 
    
        
        await self.bot.wait_for('reaction_add', check=check)

        standardEmbed.set_field_at(0,name = "Message Edited",value = f"{before.author.name} said \"{before.content}\"")
        await question.edit(embed = standardEmbed)


    #Checks if out of everyone online in a channel if only one person isnt listening to spotify
    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        
        #only care if it a relevant user
        if(not (after in self.relevantUsers)):
            return

        #check if it is a change in listening status on spotify
        listeningBefore, listeningAfter = False, False
        for activity in before.activities:
            if(type(activity) == discord.Spotify):
                listeningBefore = True
        for activity in after.activities:
            if(type(activity) == discord.Spotify):
                listeningAfter = True
        if(listeningBefore == listeningAfter):
            return
        

        relevantUsersOnline = self.relevantUsersOnline()
        peopleListening = self.peopleListeningSpotify()


        if(len(relevantUsersOnline) != len(self.relevantUsers)):
            return

        #if(not numPeopleListening):
            #await self.relevantChannel.send("No one is listening to spotify D:")

        if(len(relevantUsersOnline) - len(peopleListening) == 0):
            await self.relevantChannel.send("Everyone Listening to Spotify!!!!")

        if((len(relevantUsersOnline) - len(peopleListening) ) == 1):

            for loser in relevantUsersOnline:
                if not loser in peopleListening:
                    break
            await self.relevantChannel.send(f"While everyone else is enjoying their music {loser.mention} is being a party pooper and not listening to spotify. Bully them")

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(stalking(bot)) # add the cog to the bot



