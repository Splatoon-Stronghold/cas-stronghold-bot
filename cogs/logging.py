# FIXME: Will be removed
# import json
# import os
# from pathlib import Path

from discord import AllowedMentions, Guild, Member, Message, Object, User

# FIXME: Doesn't seem to be necessary
# from discord import Interaction, TextChannel, app_commands
from discord.ext import commands
from discord.ext.commands import Bot

from utils import env

# FIXME: Doesn't seem to be necessary
# from utils.config import add_channel, get_config, remove_channel


DISCORD_CHARACTER_LIMIT = 2000
EACH_MESSAGE_LIMIT = 100


class Logging(commands.Cog):
    """
    Logging cog.

    Addon for logging commands.
    """

    def __init__(self, bot: Bot):
        self.bot = bot

        # Set up logging_channels as a dictionary for {guild id:channel} pairs
        logging_channel_name = env.get_logging_channel_name()
        self.logging_channels = {}

        for guild in bot.guilds:
            for channel in guild.channels:
                if channel.name == logging_channel_name:
                    self.logging_channels[guild.id] = channel

    # TODO implement name change
    @commands.Cog.listener()
    async def on_user_update(self, before: User, after: User) -> None:
        """
        User update callback.

        Dummy action, typing required
        """
        print(f"# User updated: from: {str(before)}, to {str(after)}")

    # TODO implement member banning
    @commands.Cog.listener()
    async def on_member_ban(self, guild: Guild, user: Member) -> None:
        """
        Member ban callback.

        Message logging when user is banned.
        """
        channel = self.logging_channels[guild.id]

        await channel.send(content=f"# Member banned\n" f"**Member:** `{user.id}` <@{user.id}>\n")

    @commands.Cog.listener()
    async def on_member_update(self, before: Member, after: Member) -> None:
        """
        Member update callback.

        Message logging when user is updated.
        """
        channel = self.logging_channels[before.guild.id]

        if before.timed_out_until != after.timed_out_until:
            if before.timed_out_until is None:
                await channel.send(
                    content=f"# Member timed out\n"
                    f"**Member:** `{before.id}` <@{before.id}>\n"
                    f"**Until:** <t:{int(after.timed_out_until.timestamp())}:F>",
                    allowed_mentions=AllowedMentions(users=[Object(id=before.id)]),
                )
            elif after.timed_out_until is None:
                await channel.send(
                    content=f"# Member timeout removed\n"
                    f"**Member:** `{before.id}` <@{before.id}>\n"
                    f"**Was timed out until:** <t:{int(before.timed_out_until.timestamp())}:F>",
                    allowed_mentions=AllowedMentions(users=[Object(id=before.id)]),
                )
            else:  # Not sure if this can happen
                await channel.send(
                    content=f"# Member timeout changed\n"
                    f"**Member:** `{before.id}` <@{before.id}>\n"
                    f"**Was timed out until:** <t:{int(before.timed_out_until.timestamp())}:F>"
                    f"**Now timed out until:** <t:{int(after.timed_out_until.timestamp())}:F>",
                    allowed_mentions=AllowedMentions(users=[Object(id=before.id)]),
                )

    @commands.Cog.listener()
    async def on_message_delete(self, message: Message) -> None:
        """
        Message deletion callback.

        Message logging when message is deleted.
        """
        channel = self.logging_channels[message.guild.id]

        # Do not log deletions in the logging channel itself
        if message.channel.id == channel.id:
            return

        content_notice = ""

        # Replacing with U+2035 REVERSED PRIME
        sanitized_content = message.content.replace("```", "‵‵‵")
        character_limit = 1500
        if len(sanitized_content) > character_limit:
            sanitized_content = sanitized_content[:character_limit]
            content_notice += f" (trimmed at {character_limit})"

        # There is a "silent" alias for "suppress_notifications", keeping only "silent" to not log duplicate information
        all_flags = filter(lambda flag_name: flag_name != "suppress_notifications", message.flags.VALID_FLAGS)
        # Create list of flag names only for flags that are True
        flags = [flag for flag in all_flags if getattr(message.flags, flag)]

        # Create text listing the True flags
        flags_notice = ""
        if len(flags) > 0:
            flags_notice = f" ({', '.join(flags)})"

        # TODO: attachments? reactions? other metadata?

        await channel.send(
            content=f"# Message deleted\n"
            f"**Message:** `{message.id}` https://discord.com/channels/{message.guild.id}/"
            f"{message.channel.id}/{message.id}{flags_notice}\n"
            f"**Author:** `{message.author.id}` <@{message.author.id}>\n"
            f"**Content:** {len(message.content)} characters{content_notice}\n"
            f"```"
            f"{sanitized_content}"
            f"```",
            allowed_mentions=AllowedMentions(users=[Object(id=message.author.id)]),
        )

    @commands.Cog.listener()
    async def on_message_edit(self, before: Message, after: Message) -> None:
        """
        Message edition callback.

        Message logging when message is edited.
        """
        guild_id = before.guild.id
        channel = self.logging_channels[guild_id]

        before_string = "**Before:**" if len(before.content) <= 750 else "**Before:** (Trimmed at 750)"
        after_string = "**After:**" if len(after.content) <= 750 else "**After:** (Trimmed at 750)"

        before_sanitized_content = before.content[:750].replace("```", "‵‵‵")
        after_sanitized_content = after.content[:750].replace("```", "‵‵‵")

        payload = (
            f"# Message edited\n"
            f"**Member:** `{before.author.id}` <@{before.author.id}>\n"
            f"{before_string} ```{before_sanitized_content}```\n"
            f"{after_string} ```{after_sanitized_content}```"
        )

        await channel.send(content=payload)

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload: Bot) -> None:
        """
        Raw bulk message deletion callback.

        Message logging when raw bulk message is deleted.

        Typing required
        """
        deleted_channel = list(payload.cached_messages)[0].channel
        deleted_guild_id = deleted_channel.guild.id

        sending_channel = self.logging_channels[deleted_guild_id]

        header_content = (
            "# Message Purge\n"
            + f"**Number of messages:** {len(payload.cached_messages)}\n"
            + f"**Purged message link:** https://discord.com/channels/{deleted_guild_id}/"
            + f"{deleted_channel.id}/{payload.cached_messages[0].id}\n"
        )

        purge_message_content = ""

        for msg_index, msg in enumerate(payload.cached_messages):
            # person: message [with no code formatting]

            # truncate and sanitize the message content
            curr_message_content = msg.content.replace("```", "‵‵‵").replace("`", "‵")
            if len(curr_message_content) > EACH_MESSAGE_LIMIT:
                curr_message_content = curr_message_content[: EACH_MESSAGE_LIMIT - 3]
                curr_message_content += "..."

            curr_message = f"<@{msg.author.id}> `{curr_message_content}`\n"

            # if we're above the character limit, we should truncate the last message.
            if len(header_content) + len(purge_message_content) + len(curr_message) >= DISCORD_CHARACTER_LIMIT:

                header_content += f"Truncated at {msg_index} messages.\n"

                curr_message_limit = DISCORD_CHARACTER_LIMIT - len(purge_message_content) - len(header_content)

                curr_message = curr_message[: curr_message_limit - 6]
                curr_message += "...`"

                purge_message_content += curr_message
                break
            else:
                purge_message_content += curr_message

        final_message = header_content + purge_message_content

        await sending_channel.send(content=final_message)

    # TODO implement member joining
    @commands.Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        """
        Member join callback.

        Member join logging when member is joined.
        """
        print(f"[CAS] Member joined {str(member)}")

    # TODO implement member leaving
    @commands.Cog.listener()
    async def on_member_remove(self, member: Member) -> None:
        """
        Member leave callback.

        Member leave logging when member is removed.
        """
        print(f"[CAS] Member removed {str(member)}")
