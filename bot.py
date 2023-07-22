import discord
import os
from dotenv import load_dotenv
import json
from cogs.publish import Publish
from cogs.twitchlisten import TwitchListen
from cogs.yt_listen import YtListener

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUID_ID'))

def run_discord_bot():
    # Initializing the intents of the bot
    intent = discord.Intents.default()
    intent.message_content = True
    bot = discord.ext.commands.Bot(command_prefix = '!', intents=intent)
    
    
    my_guild = None
    # Message when running
    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running')
        bot.tree.clear_commands(guild=None)
        await bot.add_cog(Publish(bot))
        #await bot.add_cog(TwitchListen(bot))
        await bot.add_cog(YtListener(bot))

        await bot.tree.sync()
        print('All commands set up!')
        print(type(GUILD_ID))
        my_guild = bot.get_guild(GUILD_ID)
        print(my_guild)
        
        for guild in bot.guilds:
            if guild != my_guild:
                print('Not my guild!')
                await guild.leave()

    @bot.event
    async def on_guild_join(guild):
        if guild != my_guild:
            print('Not my guild!')
            await guild.leave()


    bot.run(DISCORD_TOKEN)

