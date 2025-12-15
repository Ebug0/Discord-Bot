import Responses
import discord
from Client import client
from discord.commands import *
from discord.ui import *
from discord.ext import commands, tasks
from ButtonClasses import MyView
from Token import TOKEN #Hides the bot token from github
import Config
import Scoreboard
import os
import asyncio
import time
from datetime import datetime, time as dt_time, timedelta

async def send_message(message, usermessage, isprivate):
    try:
        response = Responses.handle_response(usermessage, str(message.channel), str(message.author.id), str(message.author)) #send the message channle and who the author is to the Responses py file to process
        await message.author.send(response) if isprivate else await message.channel.send(response)      #once the responses py file process the message and gives an out put the bot send the message
    except Exception as e:                                                                              #if there is an error instead of stopping the code it just prints it out
        print(e)

def run_discord_bot():
     
    @client.slash_command(name='print', description='print whats given')
    @option("print here1", description="Enter in a thing to print",required=False,default = None)
    @option("print here2", description="Enter in a thing to print",required=False,default = None)
    async def printthing(ctx: discord.ApplicationContext, printhere1: str, printhere2: str):
        await ctx.respond(f"{printhere1}{printhere2}") 

    @client.slash_command(name='greet', description='Greet someone!')
    @option("name", description="Enter your friend's name",required=False,default = None)
    async def greet(ctx: discord.ApplicationContext,name: str):
        await ctx.respond(f"Hello {name}!") 
    
    @client.slash_command(name='leaderboard', description='View the 67 leaderboard (restricted)', guild_ids=Config.GUILD_IDS if Config.GUILD_IDS else None)
    async def leaderboard(ctx: discord.ApplicationContext):
        # Check if user is authorized
        user_id_str = str(ctx.author.id)
        if user_id_str not in Config.ALLOWED_LEADERBOARD_USERS:
            await ctx.respond("Error: You don't have permission to use this command.", ephemeral=True)
            return
        
        # Get leaderboard data
        leaderboard_data = Scoreboard.get_leaderboard(limit=20)
        
        if not leaderboard_data:
            await ctx.respond("No one has said '67' yet!")
            return
        
        # Format leaderboard message
        leaderboard_text = "🏆 67 Leaderboard:\n"
        for i, (user_id, count, username) in enumerate(leaderboard_data, 1):
            # Use username if available, otherwise use user ID
            display_name = username if username else f"User {user_id}"
            leaderboard_text += f"{i}. {display_name} - {count} time{'s' if count != 1 else ''}\n"
        
        await ctx.respond(leaderboard_text)
    
#    @client.command()
#    async def start_mafia_game (ctx):
#        view = MyView(ctx)
#        await ctx.send("Game started click below to join!", view = view)

    @client.event
    async def on_ready():                                                                               #when the bot is started up it shows us a message in console
        print(f"{client.user} is now running")
        # Load scoreboard data
        Scoreboard.load_data()
        # Sync slash commands to make them appear immediately
        # This helps ensure commands are registered even if guild_ids wasn't set
        try:
            if Config.GUILD_IDS:
                # Sync to specific guilds
                for guild_id in Config.GUILD_IDS:
                    await client.sync_commands(guild_ids=[guild_id])
                print(f"Synced commands to {len(Config.GUILD_IDS)} guild(s)")
            else:
                # Sync globally (can take up to 1 hour to appear)
                await client.sync_commands()
                print("Synced commands globally (may take up to 1 hour to appear)")
        except Exception as e:
            print(f"Error syncing commands: {e}")
        # Start daily leaderboard task
        if not daily_leaderboard_task.is_running():
            daily_leaderboard_task.start()
     
    @tasks.loop(hours=24)
    async def daily_leaderboard_task():
        """Post daily leaderboard at 8am"""
        # Get channel
        channel = None
        if Config.LEADERBOARD_CHANNEL_ID:
            channel = client.get_channel(Config.LEADERBOARD_CHANNEL_ID)
        else:
            # Find channel by name
            for guild in client.guilds:
                for ch in guild.channels:
                    if str(ch) == Config.LEADERBOARD_CHANNEL_NAME:
                        channel = ch
                        break
                if channel:
                    break
        
        if not channel:
            print(f"Error: Could not find channel for daily leaderboard")
            return
        
        # Get leaderboard data (top 10)
        leaderboard_data = Scoreboard.get_leaderboard(limit=10)
        
        if not leaderboard_data:
            return  # No one has said 67 yet
        
        # Format leaderboard with pings
        leaderboard_text = "🏆 Daily 67 Leaderboard (Top 10):\n"
        for i, (user_id, count, username) in enumerate(leaderboard_data, 1):
            ping_format = f"<@{user_id}>"
            leaderboard_text += f"{i}. {ping_format} - {count} time{'s' if count != 1 else ''}\n"
        
        try:
            await channel.send(leaderboard_text)
        except Exception as e:
            print(f"Error posting daily leaderboard: {e}")
    
    @daily_leaderboard_task.before_loop
    async def before_daily_leaderboard():
        """Wait until bot is ready and then wait until 8am"""
        await client.wait_until_ready()
        # Calculate time until next 8am
        now = datetime.now()
        target_time = dt_time(Config.LEADERBOARD_TIME[0], Config.LEADERBOARD_TIME[1])
        target_datetime = datetime.combine(now.date(), target_time)
        
        # If 8am has already passed today, schedule for tomorrow
        if now.time() >= target_time:
            target_datetime += timedelta(days=1)
        
        # Wait until 8am
        wait_seconds = (target_datetime - now).total_seconds()
        if wait_seconds > 0:
            print(f"Daily leaderboard task will start at 8am (waiting {wait_seconds/3600:.2f} hours)")
            await asyncio.sleep(wait_seconds)
    
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