import Responses
import discord
from Token import TOKEN #Hides the bot token from github

async def send_message(message, usermessage, isprivate):
    try:
        response = Responses.handle_response(usermessage, str(message.channel), str(message.author.id)) #send the message channle and who the author is to the Responses py file to process
        await message.author.send(response) if isprivate else await message.channel.send(response)      #once the responses py file process the message and gives an out put the bot send the message
    except Exception as e:                                                                              #if there is an error instead of stopping the code it just prints it out
        print(e)

def run_discord_bot():
    client = discord.Bot(intents = discord.Intents.all()) 

    @client.slash_command(name = "hello", description = "The bot responses with a hello")               #a simple slash command to see how slash commands worked invoked with /hello
    async def say_hello(ctx):
        await ctx.respond("Bitch")
    
    @client.event
    async def on_ready():                                                                               #when the bot is started up it shows us a message in console
        print(f"{client.user} is now running")

    @client.event
    async def on_message(message):                                                                      #triggers this function when a message is sent
        if message.author == client.user:                                                               #makes it so the bot doesnt try to respond to its own message
            return
        
        username = str(message.author)                                                                  #breaks downt he message object into its parts
        usermessage = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: {usermessage} in {channel}")                                           #used for debugging purposes to show what the bot is getting
        
        if usermessage[0] == "!":                                                                       #Checks to see if the bot should DM the answer to the author
            usermessage = usermessage[1:]
            await send_message(message, usermessage, isprivate=True)
        else:
            await send_message(message, usermessage, isprivate=False)
            
    client.run(TOKEN) 

    

