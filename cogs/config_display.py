from discord import Interaction, app_commands
from discord.ext import commands

from utils import env
from utils.config import get_config


class ConfigDisplay(commands.Cog):
    """
    ConfigDisplay Cog.

    To display configuration.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="config-data", description="Displays the configuration information.")
    @app_commands.checks.has_any_role("Staff", "Admin")
    @app_commands.guilds(env.get_guild_id())
    @app_commands.guild_only()
    async def config_data(self, interaction: Interaction) -> None:
        """
        Displays config data.

        Method to show in discord the config data.
        """
        yt = get_config("youtube_announcement_channels")
        twitch = get_config("twitch_announcement_channels")
        publish = get_config("publish_announcement_channels")
        await interaction.response.send_message(
            f'''```Current Configurations
Youtube:
- {"\n - ".join(yt) if yt else "[not configured]"}
Twitch:
- {"\n - ".join(twitch) if twitch else "[not configured]"}
Auto-Publisher:
- {"\n - ".join(publish) if publish else "[not configured]"}```'''
        )
