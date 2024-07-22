import discord
import os
from dotenv import load_dotenv
import json
from utils import env
from cogs.publish import Publish
from cogs.twitchlisten import TwitchListen
from cogs.uptime import Uptime
from cogs.yt_listen import YtListener
from init_start_time import start_time_to_json

def run_discord_bot():
    GUILD_ID = env.get_guild_id()

    # Initializing the intents of the bot
    intent = discord.Intents.default()
    intent.message_content = True
    bot = discord.ext.commands.Bot(command_prefix = '!', intents=intent)
    
    
    my_guild = None
    # Message when running
    @bot.event
    async def on_ready():
        my_guild = bot.get_guild(GUILD_ID)
        print(f'{bot.user} is now running in {my_guild}')

        bot.tree.clear_commands(guild=my_guild)
        await bot.add_cog(Publish(bot))
        # await bot.add_cog(TwitchListen(bot)) --> if you want to use this, uncomment it
        # await bot.add_cog(YtListener(bot)) --> if you want to use this, uncomment it
        await bot.add_cog(Uptime(bot))


        set_up_commands = await bot.tree.sync(guild=my_guild)
        print(f'Synced {len(set_up_commands)} command(s) to Discord')

        await start_time_to_json() # for /uptime
        
        for guild in bot.guilds:
            if guild != my_guild:
                print('Not my guild!')
                await guild.leave()

    @bot.event
    async def on_guild_join(guild):
        if guild != my_guild:
            print('Not my guild!')
            await guild.leave()


    bot.run(env.get_discord_token())

