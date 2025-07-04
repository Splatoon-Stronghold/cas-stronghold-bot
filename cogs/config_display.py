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

        # google sheet role management stuff

        gsheet_id = get_config("google_sheet_id")
        gsheet_sheet_name = get_config("google_sheet_name")

        gsheet_discord_id_col = get_config("google_sheet_discordID_column")
        gsheet_perm_role_col = get_config("google_sheet_position_role_column")
        gsheet_team_role_col = get_config("google_sheet_team_role_column")

        await interaction.response.send_message(
            f'''```Current Configurations
Youtube:
- {"\n - ".join(yt) if yt else "[not configured]"}
Twitch:
- {"\n - ".join(twitch) if twitch else "[not configured]"}
Auto-Publisher:
- {"\n - ".join(publish) if publish else "[not configured]"}
Google Sheet Role Management:
- ID: {gsheet_id if gsheet_id else "[not configured]"}
- Sheet Name / Tab: {gsheet_sheet_name if gsheet_sheet_name else "[not configured]"}
- Discord ID Column (A=1, B=2): {gsheet_discord_id_col + 1 if gsheet_discord_id_col else "[not configured]"}
- Position Role Column (A=1, B=2): {gsheet_perm_role_col + 1 if gsheet_perm_role_col else "[not configured]"}
- Team Role Column (A=1, B=2): {gsheet_team_role_col + 1 if gsheet_team_role_col else "[not configured]"}```'''
        )
