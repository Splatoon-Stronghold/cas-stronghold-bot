from discord.ext import commands
from discord import app_commands, Interaction
from core.config import BotConfig
from utils import env


VALID_CONFIG_ROLES = ['Staff', 'Admin']


class ConfigData(commands.Cog):
    guild_id: int = None
    _config_data: BotConfig = None

    def __init__(self, bot, bot_config: BotConfig = None):
        self.bot = bot
        if bot_config:
            self._config_data = bot_config
        print('Config Data COG added!')

    def _build_config_string(self) -> str:
        """
        This private method retrieves a markdown ready
        response for Discord bot

        Returns
        -------
            str:
                Formatted data if bot config instance exists
                if not, it will retrieve a message indicating
                that the bot config data is not provided
        """
        if not self._config_data:
            return "Not config data provided"
        store_data = self._config_data.get_store_json()
        config_data = f"""
        \r```markdown
        \rYoutube announcement channels: {", ".join(store_data.get('youtube_announcement_channels', []))} 
        \rVOD count: {store_data.get('vod_count', 0)}
        \rYoutube text channel ID: {store_data.get('yt_text_channel_id', '')}
        \rTwitch announcement channels: {",".join([k for k in store_data.get('twitch_announcement_channels', {})])}
        \rPublish announcement channels: {", ".join(store_data.get('youtube_announcement_channels', []))}
        ```
        """

        return config_data

    @app_commands.command(name='get-config-data', description='Command for retrieving CAS Bot commands')
    @app_commands.checks.has_any_role(*VALID_CONFIG_ROLES)
    @app_commands.guilds(env.get_guild_id())
    @app_commands.guild_only()
    async def get_config_data(self, interaction: Interaction):
        await interaction.response.send_message(self._build_config_string(), ephemeral=True)

    @get_config_data.error
    async def get_config_data_handler(self, ctx: Interaction, error):
        if isinstance(error, app_commands.MissingAnyRole):
            print("You don't have the required roles for using this command")
            await ctx.response.send_message("You cannot get response from this command", ephemeral=True)
