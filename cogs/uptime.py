import discord

from discord.ext import commands, tasks
from discord import app_commands
from discord import Interaction
from discord import TextChannel
from utils import env
from utils.start_time import get_uptime



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
        uptime = get_uptime()

        await interaction.response.send_message(content=f'Time since bot was online: {uptime} seconds.')

