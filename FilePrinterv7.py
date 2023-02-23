import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import html
import re

TOKEN = 'NTkxMjQxODU3ODUwNDA4OTYw.G9FU7e.uvbHgZB0A2rAxMqqEokjLJoR327ufZXmV-30zU'

load_dotenv()

intents = discord.Intents.default()  
intents.message_content = True

  
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
token = os.getenv('TOKEN')

########################BODY#########################

#Startup Message
@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))

#Main code- Begin acting when messaged
@client.event
async def on_message(message):
    #Identify and separate message sender, channel, and content
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)
    #return for confirmation
    print('Message/n' + user_message + '/n' + username + '/nin/n' + channel)
    
    #stuffed all the html replacement into a singular function
    def clean(post):
        post = post.replace("</div>", "")
        post = post.replace("<s>", "~~")
        post = post.replace("</s>", "~~")
        post = post.replace("<em>", "*")
        post = post.replace("</em>", "*")
        post = post.replace("<strong>", "**")
        post = post.replace("</strong>", "**")
        post = post.replace("<div class=\"quote\">", "> ")
        post = re.sub("\A<img loading=\"lazy\" class=\"emoji.*title=\"", ":", post)
        post = re.sub("\B<img loading=\"lazy\" class=\"emoji.*title=\"", ":", post)
        post = re.sub("\" src=\".*png\">", ":", post)
        post = re.sub("\" src=\".*svg\">", ":", post)
        return post

    #Bot begins posting after you send some form of 'hi' or 'hello'   
    #NOTE: replace with the name of your own bot
    
    if (user_message.lower() == "hello" or user_message.lower() == "hi") and username != "Testing": 
        
        #Variable initialization
        post = ""
        kormade = ""
        continuePost = False
        startLine = 0
        print('Enter the line number you want to begin from. The first line is line 1.')
        startLine = int(input()) #asks user for line number to begin from
        
        #List of User Tags-
        # NOTE: My computer is able to recognize the ascii in key's username 
        # so the nonsense is not there
        
        kormadeTags = ['lavenderdawn69#6517', '✬key!! ❀#1826', 'Skysong#9274', 'Hyperbole#4602', 
                       'TermlessFir#4555', 'Croissantunism#6736', 'scuttlefishe#2153' , 'SongOfStorms#2705', 
                       'dreaming-in-turquoise#0339', 'fizzybee#0581', 'Evergreen#3058', 'Eternity#4249', ] 
        
        #List of Corresponding Names-
        
        kormadeNames = ["Richie", "Key", "Star", "Hyper", "Screecht", "Crystal", "Kat", "Thunderstorm", "Turquoise", "Kris", "Richie", "Eternity"]
        
        #open and read txt file
        with open('interrogation.txt', 'r', errors='ignore') as f:
            lines = f.readlines()
            #after an input is given
            while startLine > 0: 
                #iterate through each line
                for line in lines[startLine:]:
                    if continuePost==True: #If a message is being continued from the last line
                            if '</span>' in line: #if it also ends in this line
                                for letter in range(0, line.index('</span>')): #take the content before the end label
                                    post += line[letter]
                                post=clean(post)
                                await message.channel.send(html.unescape(post)) #send it
                                post = ""
                                continuePost = False # the message has ended
                            else:
                                for letter in range(0, len(line)): #take the whole line as content
                                     post += line[letter]
                                post=clean(post) 
                                if line != "\n":
                                    await message.channel.send(html.unescape(post)) #send it
                                post = ""
                    else: #otherwise
                        for i in range(len(kormadeTags)): #detect if this line contains a name
                            if kormadeTags[i] in line and kormade != kormadeNames[i]:
                                kormade = kormadeNames[i]
                                await message.channel.send("```arm\n" + kormade + "\n```\n") #if so, send the name
                        if '<span class="preserve-whitespace">' in line: #if a message begins on this line
                            continuePost=True #a message has begun
                            if 'spoiler-text' in line: #if there is a spoiler
                                line = line.replace('<span class="spoiler-text spoiler-text--hidden" onclick="showSpoiler(event, this)">', "||") #send spoiler tags
                                line = line.replace('</span>', "||", 1)
                            if '</span>' in line: #if the message also ends in this line
                                for letter in range(line.index('<span class="preserve-whitespace">') + 34, line.index('</span>')): #send everything up until the end of the message
                                    post += line[letter]
                                post=clean(post)
                                await message.channel.send(html.unescape(post))
                                continuePost=False #the message has ended
                            else: #if the message doesnt end in this line
                                for letter in range(line.index('<span class="preserve-whitespace">') + 34, len(line)): #send everything in this line
                                    post += line[letter]
                                post=clean(post)
                                await message.channel.send(html.unescape(post))
                            post = "" #reset post variable after message detection loop
                    print('line\n' + str(startLine) + '\nsent')
                    startLine=startLine+1
              

client.run(TOKEN)