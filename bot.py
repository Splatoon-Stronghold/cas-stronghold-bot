import discord
import os
from dotenv import load_dotenv
import json

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
print(DISCORD_TOKEN)

ANNOUNCEMENT_CHANNELS = str(os.getenv('ANNOUNCEMENT_CHANNELS').split(' ')) # Loads channels which should be auto-published from .env file


print(ANNOUNCEMENT_CHANNELS)

async def publish_message(message: discord.message):
    try: 
        await message.publish()
    except Exception as e:
        print(e)

def run_discord_bot():
    # Initializing the intents of the bot
    intent = discord.Intents.default()
    intent.message_content = True
    client = discord.Client(intents=intent)

    # Message when running
    @client.event
    async def on_ready():
        print(f'{client.user} is now running')

    # Runs when a message is sent
    @client.event
    async def on_message(message):
        # Converts important msg properties to strings
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        # Publishes msg if it's one of the channels which should be published
        if channel in ANNOUNCEMENT_CHANNELS:
            await publish_message(message)

    client.run(DISCORD_TOKEN)