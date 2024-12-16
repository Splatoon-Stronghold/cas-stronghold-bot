from discord import Interaction, app_commands
from discord.ext import commands
from discord.ext.commands import Bot

from utils import env
from utils.start_time import get_uptime


class Uptime(commands.Cog):
    """
    Uptime commands.

    Cog for Uptime
    """

    bot: Bot

    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(name="uptime", description="Shows duration of time since bot came online")
    @app_commands.checks.has_any_role("Staff", "Admin")
    @app_commands.guilds(env.get_guild_id())
    @app_commands.guild_only()
    async def display_uptime(self, interaction: Interaction) -> None:
        """
        Displays uptime since bot came online.

        TODO: Check typing
        """
        uptime = get_uptime()

        await interaction.response.send_message(content=f"Time since bot was online: {uptime} seconds.")
