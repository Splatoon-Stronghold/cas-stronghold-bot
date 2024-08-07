import discord

from discord.ext import commands, tasks
from discord import app_commands
from discord import Interaction
from discord import TextChannel
import json
import os
from utils import env
from pathlib import Path
import time
import datetime



class Uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        base_path = (Path(os.path.abspath(__file__)) /'..' /'..').resolve()
        self.config_path = base_path / 'config_data.json'

        with open(self.config_path) as json_file: # add path thing
            self.config_data = json.load(json_file)        

    @app_commands.command(name = "uptime", description = "Shows duration of time since bot came online")
    @app_commands.checks.has_any_role('Staff', 'Admin')
    @app_commands.guilds(env.get_guild_id())
    @app_commands.guild_only()
    async def display_uptime(self, interaction: Interaction):
        basepath = os.path.dirname(__file__)
        filepath = os.path.abspath(os.path.join(basepath, "..", "time.json"))

        def find_time_difference(file_directory):
            # Finds difference, in seconds, from time.json's file to the current time.
            end_int = time.time()
            


            with open(file_directory, "r") as infile:
                data = json.load(infile)


            start_time = datetime.datetime.fromtimestamp(data["start_time"])

            end_time = datetime.datetime.fromtimestamp(end_int)

            duration = end_time - start_time

            duration_in_s = duration.total_seconds()
            return duration_in_s
        
        seconds_interval = find_time_difference(filepath)

        await interaction.response.send_message(content=f'Time since bot was online: {seconds_interval} seconds.')

