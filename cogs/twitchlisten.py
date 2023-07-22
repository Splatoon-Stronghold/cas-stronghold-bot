from discord.ext import commands, tasks
from discord import app_commands
from discord import Interaction
import json
import os
import os
import requests
import json
from datetime import date
from dotenv import load_dotenv



# these are global variables so that they only run once throughout the loop.

#the cog itself

class TwitchListen(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.is_live = False
        self.last_seen_live = False
        
        # twitch and discord channel info 
        load_dotenv()
        self.client = os.getenv("TWITCH_CLIENT")
        self.secret = os.getenv("TWITCH_SECRET")
        self.user = os.getenv("TWITCH_USER")
        self.channel = int(os.getenv("TWITCH_DISCORD_CHANNEL"))


    def cog_unload(self):
        self.twitch.cancel()

    def cog_load(self):
        self.twitch.start()

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