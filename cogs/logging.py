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

    # TODO implement name change
    @commands.Cog.listener()
    async def on_user_update(self,before,after):
        pass


    # TODO implement member banning
    @commands.Cog.listener()
    async def on_member_ban(self,guild,user):
        pass


    # TODO implement member mute
    @commands.Cog.listener()
    async def on_member_update(self,before,after):
        channel = self.bot.guilds[0].text_channels[0] # TODO

        if before.timed_out_until != after.timed_out_until:
            if before.timed_out_until is None:
                await channel.send(
                    content=
                        f"# Member timed out\n"
                        f"**Member:** `{before.id}` <@{before.id}>\n"
                        f"**Until:** <t:{int(after.timed_out_until.timestamp())}:F>",
                    allowed_mentions=AllowedMentions(
                        users=[Object(id=after.id)]
                    )
                )
            elif after.timed_out_until is None:
                await channel.send(
                    content=
                        f"# Member timeout removed\n"
                        f"**Member:** `{before.id}` <@{before.id}>\n"
                        f"**Was timed out until:** <t:{int(before.timed_out_until.timestamp())}:F>",
                    allowed_mentions=AllowedMentions(
                        users=[Object(id=after.id)]
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
                        users=[Object(id=after.id)]
                    )
                )


    # TODO implement delete messages
    @commands.Cog.listener()
    async def on_message_delete(self,message):
        channel = self.bot.guilds[0].text_channels[0] # TODO

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

        types = []
        if message.flags.crossposted:
            types.append("crossposted")
        if message.flags.is_crossposted:
            types.append("is_crossposted")
        if message.flags.source_message_deleted:
            types.append("source_message_deleted")
        if message.flags.suppress_embeds:
            types.append("suppress_embeds")
        if message.flags.urgent: # shouldn't happen?
            types.append("urgent")
        if message.flags.has_thread:
            types.append("has_thread")
        if message.flags.ephemeral: # shouldn't happen?
            types.append("ephemeral")
        if message.flags.loading: # shouldn't happen?
            types.append("loading")
        if message.flags.failed_to_mention_some_roles_in_thread:
            types.append("failed_to_mention_some_roles_in_thread")
        if message.flags.silent:
            types.append("silent")
        # Needs discord.py >= 2.3
        # if message.flags.voice:
        #     types.append("voice")

        type_notice = ""
        if len(types) > 0:
            type_notice = f" ({', '.join(types)})"

        # TODO: attachments? reactions? other metadata?

        await channel.send(
            content=
                f"# Message deleted\n"
                f"**Message:** `{message.id}` https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}{type_notice}\n"
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
        pass


    # TODO implement purge messages
    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):
        pass


    # TODO implement member joining
    @commands.Cog.listener()
    async def on_member_join(self,member):
        pass

    # TODO implement member leaving
    @commands.Cog.listener()
    async def on_member_remove(self,member):
        pass
