from discord.ext import commands, tasks
from discord import app_commands
from discord import Interaction
from discord import TextChannel
import os
import requests
import json
from pathlib import Path
from datetime import date
from dotenv import load_dotenv

class TwitchListen(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.is_live = False
        self.last_seen_live = False

        # channels to send to
        base_path = (Path(os.path.abspath(__file__)) /'..' /'..').resolve()
        self.config_path = base_path / 'config_data.json'
        with open(self.config_path) as json_file: # add path thing
            config_data = json.load(json_file)
            self.channels = config_data['twitch_announcement_channels']


        
        # twitch and discord channel info 
        load_dotenv()
        self.client = os.getenv("TWITCH_CLIENT")
        self.secret = os.getenv("TWITCH_SECRET")
        self.user = os.getenv("TWITCH_USER")
        self.channel = int(os.getenv("TWITCH_DISCORD_CHANNEL"))


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

    
    @app_commands.command(name = "add-twitch-config", description = "Configures the youtube listener")
    @app_commands.checks.has_any_role('Staff', 'Admin')
    async def add_twitch_announce(self, interaction: Interaction, channel : TextChannel):
        # Get channel name
        # if channel name is new: 
            # add to list of announce channels & channel IDs internally
            # write to json file
            # give confirmation
        # else:
            # write error msg to discord channel
        pass

    @app_commands.command(name = "del-twitch-config", description = "Configures the youtube listener")
    @app_commands.checks.has_any_role('Staff', 'Admin')
    async def del_twitch_announce(self, interaction: Interaction, channel : TextChannel):
        # Get channel name
        # if channel name is available: 
            # remove from list of announce channels & channel IDs internally
            # write to json file
            # give confirmation
        # else:
            # write error msg to discord channel "we dont have that channel"

        
        pass


    ### youtube listener: use as a base.
    # @app_commands.command(name = "config-youtube", description = "Configures the youtube listener")
    # @app_commands.checks.has_any_role('Staff', 'Admin')
    # async def set_yt_announce(self, interaction: Interaction, channel : TextChannel):
    #     self.channel = channel

        

    #     with open(str(self.config_path), "r") as outfile:
    #         config_data = json.load(outfile)
                
    #     config_data['yt_text_channel_id'] = self.channel.id
    #     with open(str(self.config_path), "w")  as outfile:
    #         json.dump(config_data, outfile)

    #     await interaction.response.send_message(content=f'The Youtube Listener has been set to {self.channel}!')


    #checks every 5 seconds if Twitch is online
    @tasks.loop(seconds=5.0)
    async def twitch(self):
        self.is_live = is_TwitchOnline(self.client, self.secret, self.user)

        channel = self.bot.get_channel(self.channel)

        #send message only if currently live and not previously
        if self.is_live:
            if not self.last_seen_live:
                await channel.send(f"Splatoon Stronghold is now live! https://twitch.tv/SplatoonStronghold")

            self.last_seen_live = True
        else:
            self.last_seen_live = False



# Function that checks whether stream is online
def is_TwitchOnline(client, secret, user):
    try:
        
        #twitch api parameters
        TWITCHCLIENT_ID = client
        TWITCHSECRET = secret

        #twitch username, e.g. https://twitch.tv/Kiver would be Kiver
        USERSTREAM = user


        # URL to request OAuth Token
        tokenurl = 'https://id.twitch.tv/oauth2/token?client_id=' + TWITCHCLIENT_ID + \
                   '&client_secret=' + TWITCHSECRET+'&grant_type=client_credentials'


        response = requests.post(tokenurl)
        response.raise_for_status()
        OAuth_Token = response.json()["access_token"]

        # Connection to Twitch
        response = requests.get('https://api.twitch.tv/helix/streams?user_login=' + \
                   USERSTREAM, headers={'Authorization': 'Bearer ' + \
                   OAuth_Token,'Client-Id': TWITCHCLIENT_ID})
        var=json.loads(response.content)

        return var['data']

    except Exception as e: 
        print(e)
    
    return "Done"