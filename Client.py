import os
import ssl
import asyncio

# Configure SSL certificates BEFORE importing discord
# This fixes SSL certificate verification errors on Windows servers
# Must be done before discord import because discord.py initializes aiohttp during import
try:
    import certifi
    # Set environment variables so aiohttp (used by discord.py) uses certifi certificates
    cert_path = certifi.where()
    os.environ['SSL_CERT_FILE'] = cert_path
    os.environ['REQUESTS_CA_BUNDLE'] = cert_path
    # Also configure default SSL context to use certifi
    ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=cert_path)
except ImportError:
    # If certifi is not installed, the bot will try to use system certificates
    # Install certifi with: pip install certifi
    pass

import discord

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
