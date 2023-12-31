from discord.ext import commands, tasks
from discord import app_commands
from discord import Interaction
from discord import TextChannel
import json
import os
from dotenv import load_dotenv
from pathlib import Path
from googleapiclient.discovery import build




# these are global variables so that they only run once throughout the loop.

#the cog itself

class YtListener(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
        # twitch and discord channel info 
        base_path = (Path(os.path.abspath(__file__)) /'..' /'..').resolve()
        self.config_path = base_path / 'config_data.json'
        load_dotenv()
        self.API_KEY = os.getenv("YT_API_KEY")
        self.YT_CHANNEL = os.getenv("YT_CHANNEL_ID")

        with open(self.config_path) as json_file: # add path thing
            config_data = json.load(json_file)
            self.vod_count = config_data['vod_count']
            self.channel = bot.get_channel(config_data['yt_text_channel_id'])
        
        self.youtube = build('youtube', 'v3', developerKey=self.API_KEY)
        self.playlist_id = self.youtube.channels().list(part='snippet,contentDetails,statistics,status',id = self.YT_CHANNEL).execute()['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    def cog_unload(self):
        try:
            self.yt.cancel()
        except Exception as e:
            print(f'Stopping the listener failed - error: {e}')
    
    def cog_load(self):
        try:
            self.yt.start()
        except Exception as e:
            print(f'Starting the listener failed - error: {e}')
    
    @app_commands.command(name = "config-youtube", description = "Configures the youtube listener")
    @app_commands.checks.has_any_role('Staff', 'Admin')
    async def set_yt_announce(self, interaction: Interaction, channel : TextChannel):
        self.channel = channel

        

        with open(str(self.config_path), "r") as outfile:
            config_data = json.load(outfile)
                
        config_data['yt_text_channel_id'] = self.channel.id
        with open(str(self.config_path), "w")  as outfile:
            json.dump(config_data, outfile)

        await interaction.response.send_message(content=f'The Youtube Listener has been set to {self.channel}!')

        





    #checks every 30 seconds if there's been a youtube video published
    @tasks.loop(seconds=30.0)
    async def yt(self):
        self.vods()
        for msg in self.msgs:
            await self.channel.send(msg)

        with open(str(self.config_path), "r") as outfile:
            config_data = json.load(outfile)
                
        config_data['vod_count'] = self.vod_count
        with open(str(self.config_path), "w")  as outfile:
            json.dump(config_data, outfile)

    def vods(self):
        def get_playlist(self):
            playlist_re = self.youtube.playlistItems().list(
                part = 'contentDetails,snippet',
                playlistId = self.playlist_id)
            
            playlist = playlist_re.execute()
            
            return playlist, playlist_re
        def vod_count(self):
            return self.playlist['pageInfo']['totalResults']
        

        def get_new_vod_count(self):
            return vod_count(self) - self.vod_count
        
        def clamp(i, max_num, min_num):
            return max(min(i, max_num), min_num)


        self.playlist, _ = get_playlist(self)

        self.new_vod_count = get_new_vod_count(self)

        self.msgs = []
        
        if self.new_vod_count == 0:
            return
        else:
            
            for i in range(clamp(self.new_vod_count, 5, 0)):
                vod = self.playlist['items'][i]
                channel_title = vod['snippet']['channelTitle']
                vid_url = 'https://www.youtube.com/watch?v=' + str(vod['contentDetails']['videoId'])

                self.msgs.append(f'{channel_title} just posted a new video! Check it out! {vid_url}')
            
    
            self.vod_count = vod_count(self)
    
            
            
