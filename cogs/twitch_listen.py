from discord.ext import commands, tasks
from discord import app_commands
from discord import Interaction
from discord import TextChannel
import os
from pathlib import Path
from datetime import date
from dotenv import load_dotenv
from utils.config import get_config
from utils.twitch_online import is_twitch_online
from utils.channel_data import get_channel_from_name

class TwitchListen(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.is_live = False
        self.last_seen_live = False

        # twitch channel info
        load_dotenv()
        self.client = os.getenv("TWITCH_CLIENT")
        self.secret = os.getenv("TWITCH_SECRET")
        self.user = os.getenv("TWITCH_USER")

    def cog_unload(self):
        try:
            self.twitch.cancel()
        except Exception as e:
            print(f'Stopping the twitch listener failed - error: {e}')
    
    def cog_load(self):
        try:
            self.twitch.start()
        except Exception as e:
            print(f'Starting the twitch listener failed - error: {e}')

    
    @tasks.loop(seconds=5.0)
    async def twitch(self):
        '''
        Announces to channels in config when twitch account becomes online.

        Parameters (None)

        Interfaces with
        ----------
            List of discord channels pulled from config

        Returns
        ----------
            None, but sends message in each discord channel when live.
        '''
        self.is_live = is_twitch_online(self.client, self.secret, self.user)

        #send message only if currently live and not previously
        if self.is_live:
            if not self.last_seen_live:
                twitch_channels = get_config('twitch_announcement_channels')
                for channel_name in twitch_channels:
                    channel = get_channel_from_name(self.bot, channel_name)
                    if(channel is None):
                        print("Fetching channel from ID failed. Perhaps wrong server.")
                    else:
                        await channel.send(f"Splatoon Stronghold is now live! https://twitch.tv/SplatoonStronghold")
                    

            self.last_seen_live = True
        else:
            self.last_seen_live = False