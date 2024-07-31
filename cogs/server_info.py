from discord.ext import commands
from discord import app_commands
from discord import Interaction
from utils import env

class ServerInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = 'server-info', description = 'Show stats about the server')
    @app_commands.checks.has_any_role('Staff', 'Admin')
    @app_commands.guilds(env.get_guild_id())
    @app_commands.guild_only()
    async def server_info(self, interaction: Interaction):
        guild = interaction.guild
        response = interaction.response

        if guild is not None:
            await response.send_message(
                f'**Members:** `{guild.member_count}`\n'
                f'**Roles:** `{len(guild.roles)}`\n'
                f'**Categories:** `{len(guild.categories)}`\n'
                f'**Text Channels:** `{len(guild.text_channels)}`\n'
                f'**Voice Channels:** `{len(guild.voice_channels)}`\n'
                f'**ID:** `{guild.id}`\n'
                f'**Created:** <t:{int(guild.created_at.timestamp())}:F>',
                ephemeral=True
            )
        else:
            await response.send_message('Failed to get server information.', ephemeral=True)
