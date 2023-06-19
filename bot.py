import discord
import os
from dotenv import load_dotenv
import json
from cogs.publish import Publish

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

def run_discord_bot():
    # Initializing the intents of the bot
    intent = discord.Intents.default()
    intent.message_content = True
    bot = discord.ext.commands.Bot(command_prefix = '!', intents=intent)
    

    # Message when running
    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running')
        bot.tree.clear_commands(guild=None)
        await bot.add_cog(Publish(bot))
        await bot.tree.sync()
        print('All commands set up!')
    

    bot.run(DISCORD_TOKEN)