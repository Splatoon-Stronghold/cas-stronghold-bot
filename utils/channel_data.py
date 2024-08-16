from discord.ext import commands, tasks
from discord import app_commands
from discord import Interaction
from discord import TextChannel
from discord import utils
import os
from pathlib import Path
from datetime import date
from dotenv import load_dotenv

def get_channel_from_name(bot, channel_name):
    '''
        Gets the TextChannel of a specific discord channel in the bot's working server.

        Parameters
        ----------
        bot : discord.bot
        Discord bot client.

        channel_name : String
        Discord channel to find ID of.

        Returns
        ----------
            TextChannel: channel ID of the channel. If not found, returns None.
    '''
    try:
        all_guilds = bot.guilds
        first_listed_guild = all_guilds[0]
        # TODO check the edge case for multiple servers having same channel name
        # TODO check case for multiple servers. Currently this assumes we have one server
        
        channel = utils.get(first_listed_guild.channels, name=channel_name)
        return channel

        return utils.get(bot.guilds.channels, name=channel_name)
    except Exception as e:
        print(e)
        return None