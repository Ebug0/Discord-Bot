import Responses
import discord

async def send_message(message, usermessage, isprivate):
    try:
        response = Responses.handle_response(usermessage)
        await message.author.send(response) if isprivate else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = "MTAzNTM5ODY0ODM3NDIzMTE0MQ.GWbXhN.trCUaQV087bPs1PjpFjNbKEktYtF_Wf-gMxSMc"
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} is now running")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        username = str(message.author)
        usermessage = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: {usermessage} in {channel}")

        if usermessage[0] == "!":
            usermessage = usermessage[1:]
            print(usermessage)
            await send_message(message, usermessage, isprivate=True)
        else:
            await send_message(message, usermessage, isprivate=False)
            
    client.run(TOKEN)
    
