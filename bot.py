import sys

import discord
from discord import Guild
from discord.ext import commands

from cogs.config_data import ConfigData
from cogs.config_display import ConfigDisplay
from cogs.logging import Logging
from cogs.moderation import Moderation
from cogs.publish import Publish
from cogs.server_info import ServerInfo
from cogs.twitch_config import TwitchConfig
from cogs.twitch_listen import TwitchListen
from cogs.uptime import Uptime
from core.config import get_bot_config

# from cogs.yt_listen import YtListener
from utils import env
from utils.start_time import save_start_time


def get_guild(bot_ins):
    _bot_id = env.get_force_guild_id()
    my_guild = bot_ins.get_guild(_bot_id)
    if not my_guild:
        my_guild = bot_ins.get_guild(env.get_guild_id())
    return my_guild


def run_discord_bot():
    # Initializing the intents of the bot
    intents = discord.Intents.default()
    intents.message_content = True  # for publish
    intents.messages = True  # for logging
    intents.moderation = True  # for logging
    intents.members = True  # for logging
    bot = commands.Bot(command_prefix="!", intents=intents)
    _my_guild = get_guild(bot)

    bot = commands.Bot(command_prefix="!", intents=intents)
    my_guild = None

    # Message when running
    @bot.event
    async def on_ready() -> None:
        my_guild = _my_guild
        print(f"{bot.user} is now running in {my_guild}")

        bot.tree.clear_commands(guild=my_guild)

        await bot.add_cog(Publish(bot))
        await bot.add_cog(TwitchListen(bot))
        await bot.add_cog(TwitchConfig(bot))
        # await bot.add_cog(YtListener(bot)) --> if you want to use this, uncomment it
        await bot.add_cog(Uptime(bot))
        await bot.add_cog(ServerInfo(bot))
        await bot.add_cog(Logging(bot))
        await bot.add_cog(ConfigData(bot, bot_config=get_bot_config(file_path=env.get_bot_config_path())))
        await bot.add_cog(Moderation(bot))
        await bot.add_cog(ConfigDisplay(bot))

        all_guild_commands = bot.tree.get_commands(guild=my_guild)
        all_global_commands = bot.tree.get_commands(guild=None)
        print(f"Configured {len(all_guild_commands)} guild command(s), {len(all_global_commands)} global command(s)")
        if len(all_global_commands) > 0:
            print("Do not use global commands! Exiting")
            sys.exit(1)

        set_up_commands = await bot.tree.sync(guild=my_guild)
        print(f"Synced {len(set_up_commands)} guild command(s) to Discord")

        save_start_time()  # for /uptime

        for guild in bot.guilds:
            if guild != my_guild:
                print("Not my guild!")
                await guild.leave()

    @bot.event
    async def on_guild_join(guild: Guild) -> None:
        if guild != my_guild:
            print("Not my guild!")
            await guild.leave()

    bot.run(env.get_discord_token())
