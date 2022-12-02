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

loopmusic = False

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
        await ctx.respond(f"Hello {name}!") 
    
    @client.command()
    async def start_mafia_game (ctx):
        view = MyView(ctx)
        await ctx.send("Game started click below to join!", view = view)

    @client.event
    async def on_ready():                                                                               #when the bot is started up it shows us a message in console
        print(f"{client.user} is now running")

    @client.slash_command(name = "start_music", description = "Starts the music bot with the given youtube URL")
    @option("url", description = "Enter in the videos url here", required = True)
    async def start_music(ctx: discord.ApplicationContext, url: str):
        global loopmusic
        try:
            voice_client = await ctx.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except Exception as err:
            print(err)

        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options, executable = "C:\\FFMPEG\\ffmpeg.exe")

            voice_clients[ctx.guild.id].play(player)

            while loopmusic == True:
                voice_clients[ctx.guild.id].play(player)

            await ctx.respond(f"{ctx.author} started playing {url}")
        except Exception as err:
            print(err)
    
    @client.slash_command(name = "looptoggle", description = "toggles between looping and not looping current song")
    async def loop_music(ctx):
        global loopmusic
        if loopmusic == False:
            loopmusic = True
            await ctx.respond(f"{ctx.author} started looping the current song")
        else: 
            loopmusic = False
            await ctx.respond(f"{ctx.author} stopped looping the current song")
    
    @client.slash_command(name = "pause", description = "Pauses the current song")
    async def pause_music(ctx: discord.ApplicationContext):
        try:
            voice_clients[ctx.guild.id].pause()
            await ctx.respond(f"{ctx.author} paused the music")
        except Exception as err:
            await ctx.respond("No music playing")
            print(err)

    @client.slash_command(name = "resume", description = "resumes the current music")
    async def resume_music(ctx):
        try:
            voice_clients[ctx.guild.id].resume()
            await ctx.respond(f"{ctx.author} resumed the music")
        except Exception as err:
            await ctx.resond("No music playing")
            print(err)
        
    @client.slash_command(name = "stop", description = "Stops the music and make the bot leave the call")
    async def stop_music(ctx):
        global loopmusic
        try:
            loopmusic = False
            voice_clients[ctx.guild.id].resume()
            await voice_clients[ctx.guild.id].disconnect()
            await ctx.respond(f"{ctx.author} stopped the music") 
        except Exception as err:
            await ctx.resond("No music playing")
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