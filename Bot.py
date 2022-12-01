import Responses
import discord
from Client import client
from discord.commands import *
from discord.ui import *
from discord.ext import commands
from ButtonClasses import MyView
from Token import TOKEN #Hides the bot token from github
import os
import asyncio
import youtube_dl
import time

async def send_message(message, usermessage, isprivate):
    try:
        response = Responses.handle_response(usermessage, str(message.channel), str(message.author.id)) #send the message channle and who the author is to the Responses py file to process
        await message.author.send(response) if isprivate else await message.channel.send(response)      #once the responses py file process the message and gives an out put the bot send the message
    except Exception as e:                                                                              #if there is an error instead of stopping the code it just prints it out
        print(e)

def run_discord_bot():
    voice_clients = {}

    yt_dl_opts = {'format': 'bestaudio/best'}
    ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

    ffmpeg_options = {'options': "-vn"}

     
    @client.slash_command(name='print', description='print whats given')
    @option("print here1", description="Enter in a thing to print",required=False,default = None)
    @option("print here2", description="Enter in a thing to print",required=False,default = None)
    async def printthing(ctx: discord.ApplicationContext, printhere1: str, printhere2: str):
        await ctx.respond(f"{printhere1}{printhere2}") 

    @client.slash_command(name='greet', description='Greet someone!')
    @option("name", description="Enter your friend's name",required=False,default = None)
    async def greet(ctx: discord.ApplicationContext,name: str):
        test = client.get_user(name)
        await ctx.respond(f"Hello {test}!") 
    
    @client.command()
    async def start_mafia_game (ctx):
        view = MyView(ctx)
        await ctx.send("Game started click below to join!", view = view)

    @client.event
    async def on_ready():                                                                               #when the bot is started up it shows us a message in console
        print(f"{client.user} is now running")

    @client.event
    async def on_message(msg):
            if msg.content.startswith("?play"):

                try:
                    voice_client = await msg.author.voice.channel.connect()
                    voice_clients[voice_client.guild.id] = voice_client
                except:
                    print("error")

                try:
                    url = msg.content.split()[1]

                    loop = asyncio.get_event_loop()
                    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

                    song = data['url']
                    player = discord.FFmpegPCMAudio(song, **ffmpeg_options)

                    voice_clients[msg.guild.id].play(player)

                except Exception as err:
                    print(err)


            if msg.content.startswith("?pause"):
                try:
                    voice_clients[msg.guild.id].pause()
                except Exception as err:
                    print(err)

        # This resumes the current song playing if it's been paused
            if msg.content.startswith("?resume"):
                try:
                    voice_clients[msg.guild.id].resume()
                except Exception as err:
                    print(err)

        # This stops the current playing song
            if msg.content.startswith("?stop"):
                try:
                    voice_clients[msg.guild.id].stop()
                    await voice_clients[msg.guild.id].disconnect()
                except Exception as err:
                    print(err)     

    @client.event
    async def on_message(message):                                                                      #triggers this function when a message is sent
        if message.author == client.user:                                                               #makes it so the bot doesnt try to respond to its own message
            return
        
        username = str(message.author)                                                                  #breaks down the message object into its parts
        usermessage = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: {usermessage} in {channel}: Bot file")                                           #used for debugging purposes to show what the bot is getting
        
        if usermessage[0] == "!":                                                                       #Checks to see if the bot should DM the answer to the author
            usermessage = usermessage[1:]
            await send_message(message, usermessage, isprivate=True)
        else:
            await send_message(message, usermessage, isprivate=False)
            
    client.run(TOKEN)


""" 
    @commands.command()
    async def ga(self, ctx):
        channel = self.bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        users = set()
        for reaction in message.reactions:
            async for user in reaction.users():
                users.add(user)
        await ctx.send(f"users: {', '.join(user.name for user in users)}") """