from discord.ext import commands
from discord import app_commands
from discord import Interaction
from discord import TextChannel
from discord import AllowedMentions
from discord import Object
import json
import os
from pathlib import Path
from utils.config import get_config, add_channel, remove_channel
from utils import env

class Logging(commands.Cog):
    def __init__(self, bot):
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
    async def on_user_update(self,before,after):
        pass


    # TODO implement member banning
    @commands.Cog.listener()
    async def on_member_ban(self,guild,user):
        channel = self.logging_channels[guild.id]
        
        await channel.send(
                    content=
                        f"# Member banned\n"
                        f"**Member:** `{user.id}` <@{user.id}>\n"
                        
                    )
    

    @commands.Cog.listener()
    async def on_member_update(self,before,after):
        channel = self.logging_channels[before.guild.id]

        if before.timed_out_until != after.timed_out_until:
            if before.timed_out_until is None:
                await channel.send(
                    content=
                        f"# Member timed out\n"
                        f"**Member:** `{before.id}` <@{before.id}>\n"
                        f"**Until:** <t:{int(after.timed_out_until.timestamp())}:F>",
                    allowed_mentions=AllowedMentions(
                        users=[Object(id=before.id)]
                    )
                )
            elif after.timed_out_until is None:
                await channel.send(
                    content=
                        f"# Member timeout removed\n"
                        f"**Member:** `{before.id}` <@{before.id}>\n"
                        f"**Was timed out until:** <t:{int(before.timed_out_until.timestamp())}:F>",
                    allowed_mentions=AllowedMentions(
                        users=[Object(id=before.id)]
                    )
                )
            else: # Not sure if this can happen
                await channel.send(
                    content=
                        f"# Member timeout changed\n"
                        f"**Member:** `{before.id}` <@{before.id}>\n"
                        f"**Was timed out until:** <t:{int(before.timed_out_until.timestamp())}:F>"
                        f"**Now timed out until:** <t:{int(after.timed_out_until.timestamp())}:F>",
                    allowed_mentions=AllowedMentions(
                        users=[Object(id=before.id)]
                    )
                )


    @commands.Cog.listener()
    async def on_message_delete(self,message):
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
        all_flags = filter(lambda flag_name: flag_name != 'suppress_notifications', message.flags.VALID_FLAGS)
        # Create list of flag names only for flags that are True
        flags = [flag for flag in all_flags if getattr(message.flags, flag)]

        # Create text listing the True flags
        flags_notice = ""
        if len(flags) > 0:
            flags_notice = f" ({', '.join(flags)})"

        # TODO: attachments? reactions? other metadata?

        await channel.send(
            content=
                f"# Message deleted\n"
                f"**Message:** `{message.id}` https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}{flags_notice}\n"
                f"**Author:** `{message.author.id}` <@{message.author.id}>\n"
                f"**Content:** {len(message.content)} characters{content_notice}\n"
                f"```"
                f"{sanitized_content}"
                f"```",
            allowed_mentions=AllowedMentions(
                users=[Object(id=message.author.id)]
            )
        )

    # TODO implement edit messages
    @commands.Cog.listener()
    async def on_message_edit(self,before,after):
        guild_id = before.guild.id
        channel = self.logging_channels[guild_id]

        before_string = ("**Before:**" if len(before.content) <= 750
                        else "**Before:** (Trimmed at 750)")
        after_string = ("**After:**" if len(after.content) <= 750
                        else "**After:** (Trimmed at 750)")

        before_sanitized_content = before.content[:750].replace("```", "‵‵‵") 
        after_sanitized_content = after.content[:750].replace("```", "‵‵‵") 


        payload = (f"# Message edited\n"
                        f"**Member:** `{before.author.id}` <@{before.author.id}>\n"
                        f"{before_string} ```{before_sanitized_content}```\n"
                        f"{after_string} ```{after_sanitized_content}```")
        
        await channel.send(
                    content=payload   
                    )


    # TODO implement purge messages
    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):
        '''
        Need a way to purge messages before this is fully implemented.

        DISCORD_CHARACTER_LIMIT = 2000

        deleted_channel = list(payload)[0].channel_id

        sending_channel = self.logging_channels[deleted_channel.guild.id]


        final_message = ""
        final_message += "# Message Purge\n"
        final_message += f"**Number of messages:** {len(payload)}\n"
        final_message += f"**Channel:** {deleted_channel}\n"

        final_message += "\n"

        for msg in payload:
            # person: message [with no code formatting]
            final_message += f"<@{msg.author.id}>: {msg.content.replace("```", "‵‵‵")}"
            final_message += "\n"

            if(len(final_message) >= DISCORD_CHARACTER_LIMIT):
                final_message = final_message[:DISCORD_CHARACTER_LIMIT - 3]
                final_message += "..."
                break


        await sending_channel.send(
            content=final_message   
            )
        '''



    # TODO implement member joining
    @commands.Cog.listener()
    async def on_member_join(self,member):
        pass

    # TODO implement member leaving
    @commands.Cog.listener()
    async def on_member_remove(self,member):
        pass
