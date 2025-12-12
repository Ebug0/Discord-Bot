import discord

# Enable all intents including message_content for on_message event
intents = discord.Intents.all()
intents.message_content = True  # Required for on_message event to receive message content

client = discord.Bot(intents=intents)
