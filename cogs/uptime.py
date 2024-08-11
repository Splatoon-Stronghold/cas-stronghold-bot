from discord.ext import commands
from discord import app_commands
from discord import Interaction
from utils import env
from utils.start_time import get_uptime

class Uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot     

    @app_commands.command(name = "uptime", description = "Shows duration of time since bot came online")
    @app_commands.checks.has_any_role('Staff', 'Admin')
    @app_commands.guilds(env.get_guild_id())
    @app_commands.guild_only()
    async def display_uptime(self, interaction: Interaction):
        uptime = get_uptime()

        await interaction.response.send_message(content=f'Time since bot was online: {uptime} seconds.')

