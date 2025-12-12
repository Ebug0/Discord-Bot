import discord
import asyncio

# Enable all intents including message_content for on_message event
intents = discord.Intents.all()
intents.message_content = True  # Required for on_message event to receive message content

# Ensure an event loop exists for Python 3.12+ compatibility
# This fixes the RuntimeError: There is no current event loop
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

client = discord.Bot(intents=intents)
