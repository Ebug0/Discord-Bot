import os
import ssl
import asyncio

# IMPORTANT: Configure SSL BEFORE importing aiohttp or discord
# This fixes SSL certificate verification errors on Windows servers

# Import aiohttp FIRST so we can patch it before discord.py uses it
import aiohttp

try:
    import certifi
    cert_path = certifi.where()
    
    # Patch aiohttp's TCPConnector to use certifi certificates by default
    original_connector_init = aiohttp.TCPConnector.__init__
    
    def patched_connector_init(self, *args, **kwargs):
        # If ssl is True (default) or not specified, use certifi certificates
        if kwargs.get('ssl') is True or 'ssl' not in kwargs:
            ssl_context = ssl.create_default_context(cafile=cert_path)
            kwargs['ssl'] = ssl_context
        # If ssl is False, keep it False
        elif kwargs.get('ssl') is False:
            pass
        # If ssl is already a context, use it as-is
        return original_connector_init(self, *args, **kwargs)
    
    aiohttp.TCPConnector.__init__ = patched_connector_init
    
    # Also set default SSL context for other libraries
    ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=cert_path)
    os.environ['SSL_CERT_FILE'] = cert_path
    os.environ['REQUESTS_CA_BUNDLE'] = cert_path
    
except ImportError:
    # If certifi is not installed, provide option to disable SSL verification
    # WARNING: Disabling SSL verification is insecure - only use as last resort
    print("WARNING: certifi not installed. SSL verification may fail.")
    print("Install certifi with: pip install certifi")
    print("If you're on a Windows server behind a corporate firewall,")
    print("you may need to disable SSL verification (INSECURE - see Client.py)")
    
    # FALLBACK: Uncomment the next 3 lines ONLY if certifi is installed but still fails
    # This disables SSL verification (INSECURE - use only as last resort on trusted networks)
    # import ssl
    # ssl._create_default_https_context = ssl._create_unverified_context
    # 
    # Also patch aiohttp to not verify SSL:
    # def patched_connector_init_no_ssl(self, *args, **kwargs):
    #     kwargs['ssl'] = False
    #     return original_connector_init(self, *args, **kwargs)
    # aiohttp.TCPConnector.__init__ = patched_connector_init_no_ssl

# Now import discord - it will use our patched aiohttp connector
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
