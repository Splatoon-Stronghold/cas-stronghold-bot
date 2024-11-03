from discord.ext import commands
from discord import app_commands
from discord import Interaction
from discord import TextChannel
import json
import os
from pathlib import Path
from utils.config import get_config, add_channel, remove_channel
from utils import env

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Set up logging_channels as a dictionary for {guild:channel ID} pairs
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
    

    # TODO implement member mute
    @commands.Cog.listener()
    async def on_member_update(self,before,after):
        pass

    # TODO implement delete messages
    @commands.Cog.listener()
    async def on_message_delete(self,message):
        pass

    # TODO implement edit messages
    @commands.Cog.listener()
    async def on_message_edit(self,before,after):
        guild_id = before.guild.id
        channel = self.logging_channels[guild_id]

        before_string = ("**Before:**" if len(before.content) <= 750
                        else "**Before:** (Trimmed at 750)")
        after_string = ("**After:**" if len(after.content) <= 750
                        else "**After:** (Trimmed at 750)")

        payload = (f"# Message edited\n"
                        f"**Member:** `{before.author.id}` <@{before.author.id}>\n"
                        f"{before_string} `{before.content[:750]}`\n"
                        f"{after_string} `{after.content[:750]}`")
        
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
