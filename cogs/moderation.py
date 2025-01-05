from datetime import timedelta

from discord import Guild, Interaction, Member, Message, app_commands
from discord.ext import commands

from utils import env


class Moderation(commands.Cog):
    """
    Moderation cog.

    Includes moderation commands.
    """

    def __init__(self, bot: commands.Bot) -> commands.Cog:
        """
        Initializes the bot.

        Only needs the instance of the discord bot.
        """
        self.bot = bot

        # From logging.py
        logging_channel_name = env.get_logging_channel_name()
        self.logging_channels = {}

        for guild in bot.guilds:
            for channel in guild.channels:
                if channel.name == logging_channel_name:
                    self.logging_channels[guild.id] = channel

    async def reason_log(
        self, action: str, guild: Guild, user: Member, reason: str, limit: int = None, count: int = None
    ) -> None:
        """
        Additional logging.

        Only used for kick.
        """
        channel = self.logging_channels[guild.id]
        message = ""

        if action == "kick":
            message = f"# Member kicked\n" f"**Member:** `{user.id}` <@{user.id}>\n" f"**Reason**: {reason}"
        elif action == "ban":
            message = f"# Member banned\n" f"**Member:** `{user.id}` <@{user.id}>\n" f"**Reason**: {reason}"
        elif action == "timeout" and limit:
            message = (
                f"# Member muted\n"
                f"**Member:** `{user.id}` <@{user.id}>\n"
                f"**Duration: {limit} hours\n"
                f"**Reason**: {reason}"
            )
        elif action == "purge" and count:
            message = (
                f"# Messages Purged\n" f"**Moderator:** `{user.id}` <@{user.id}>\n" f"**Message Count:** {count}\n"
            )

        if message:
            await channel.send(content=message)

    @app_commands.command(name="kick", description="Kicks user")
    @app_commands.checks.has_any_role("Mod", "Admin")
    @app_commands.guilds(env.get_guild_id())
    @app_commands.guild_only()
    async def kick(self, interaction: Interaction, user: Member, reason: str) -> None:
        """
        Kick member.

        Method to kick member with a required reason.
        """
        response = interaction.response
        log_reason = f"Moderator: {interaction.user.name}, Reason: {reason}"
        if not reason:
            await response.send_message(
                "Failure: Invalid input or incomplete command, please try again.", ephemeral=True
            )
            return

        try:
            await user.kick(reason=log_reason)
            await response.send_message(f"Success: <@{user.id}> ({user.id}) kicked for {reason}.", ephemeral=True)

            await self.reason_log("kick", interaction.guild, user, reason)
        except Exception as e:
            print(e)
            await response.send_message(
                "Failure: Invalid input or incomplete command, please try again.", ephemeral=True
            )

    @app_commands.command(name="timeout", description="Timeout user")
    @app_commands.checks.has_any_role("Mod", "Admin")
    @app_commands.guilds(env.get_guild_id())
    @app_commands.guild_only()
    async def timeout(self, interaction: Interaction, user: Member, hours: int, reason: str) -> None:
        """
        Timeout member.

        Method to timeout member with a required reason for a duration.
        """
        response = interaction.response
        log_reason = f"Moderator: {interaction.user.name}, Reason: {reason}"
        if not reason:
            await response.send_message(
                "Failure: Invalid input or incomplete command, please try again.", ephemeral=True
            )
            return

        try:
            await user.timeout(timedelta(hours=hours), reason=log_reason)
            await response.send_message(
                f"Success: <@{user.id}> ({user.id}) timed-out for {hours} hours because {reason}.", ephemeral=True
            )

            # await self.reason_log('timeout', interaction.guild, user, reason, limit=hours)
        except Exception as e:
            print(e)
            await response.send_message(
                "Failure: Invalid input or incomplete command, please try again.", ephemeral=True
            )

    @app_commands.command(name="ban", description="Bans user")
    @app_commands.checks.has_any_role("Mod", "Admin")
    @app_commands.guilds(env.get_guild_id())
    @app_commands.guild_only()
    async def ban(self, interaction: Interaction, user: Member, reason: str) -> None:
        """
        Ban member.

        Method to ban member with a required reason.
        """
        response = interaction.response
        log_reason = f"Moderator: {interaction.user.name}, Reason: {reason}"
        if not reason:
            await response.send_message(
                "Failure: Invalid input or incomplete command, please try again.", ephemeral=True
            )
            return

        try:
            await user.ban(reason=log_reason)
            await response.send_message(f"Success: <@{user.id}> ({user.id}) banned for {reason}.", ephemeral=True)

            # await self.reason_log('ban', interaction.guild, user, reason)
        except Exception as e:
            print(e)
            await response.send_message(
                "Failure: Invalid input or incomplete command, please try again.", ephemeral=True
            )

    @app_commands.command(name="purge", description="Purges messages")
    @app_commands.checks.has_any_role("Mod", "Admin")
    @app_commands.guilds(env.get_guild_id())
    @app_commands.guild_only()
    async def purge(self, interaction: Interaction, count: int, reason: str) -> None:
        """
        Purge messages.

        Method to purge a specific number of messages with a required reason.
        """
        response = interaction.response
        log_reason = f"Moderator: {interaction.user.name}, Reason: {reason}"
        if not reason:
            await response.send_message(
                "Failure: Invalid input or incomplete command, please try again.", ephemeral=True
            )
            return
        if count > 100:
            await response.send_message(
                "Failure: Invalid input or incomplete command, please try again. Too many messages purged.",
                ephemeral=True,
            )
            return

        def check_not_cmd(x: Message) -> bool:
            """Checks if the message wasn't the command that was called."""
            return x.id != interaction.id

        try:
            await response.defer(ephemeral=True)

            await interaction.channel.purge(limit=count, reason=log_reason, check=check_not_cmd, bulk=True)
            await interaction.followup.send(f"Success: {count} messages purged for {reason}.", ephemeral=True)

            # await self.reason_log('purge', interaction.guild, interaction.user, reason, count=count)
        except Exception as e:
            print(e)
            await interaction.followup.send(
                "Failure: Invalid input or incomplete command, please try again.", ephemeral=True
            )
            print(e)
