from discord.ext import commands
from discord import app_commands
from discord import Interaction
from discord import TextChannel
import json
import os
from pathlib import Path
from utils.config import get_config, add_channel, remove_channel
from utils import env

class Publish(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.publish_channels = get_config('publish_announcement_channels')

    @commands.Cog.listener()
    async def on_message(self,message):
        # Converts important msg properties to strings
        channel = str(message.channel)

        # Publishes msg if it's one of the channels which should be published
        # fix the bug in this with using str
        if channel in self.publish_channels:
            try:
                await message.publish()
            except Exception as e:
                print(e)
        

        
    @app_commands.command(name = "config-publisher", description = "Sets the channels to be auto-published")
    @app_commands.checks.has_any_role('Staff', 'Admin')
    @app_commands.guilds(env.get_guild_id())
    @app_commands.guild_only()
    async def config_publisher(self, interaction: Interaction, add: str = None, remove: str = None):
        response = interaction.response
        if add:
            if add in [channel.name for channel in interaction.guild.channels]:
                self.publish_channels = add_channel('publish_announcement_channels', add)
                await response.send_message(content=f'"{add}" has been added to the list of channels to be published!')
            else:
                await response.send_message(content=f'"{add}" was not added from the list of channels to be published. Please check that it is spelled correctly and case sensitive')
        if remove:
            if remove not in self.publish_channels:
                await response.send_message(content=f'"{remove}" was not removed from the list of channels to be published. Please check that it is spelled correctly and case sensitive')
            else:
                try:
                    self.publish_channels = remove_channel('publish_announcement_channels', remove)
                    await response.send_message(content=f'"{remove}" has been removed from the list of channels to be published!')
                except:
                    await response.send_message(content=f'"{remove}" was not removed from the list of channels to be published. Please check that it is spelled correctly and case sensitive')
            