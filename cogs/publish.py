# import json
# import os
# from pathlib import Path
from typing import List, Union

from discord import Interaction, Message, app_commands

# from discord import TextChannel
from discord.ext import commands
from discord.ext.commands import Bot

from utils import env
from utils.config import add_channel, get_config, remove_channel


class Publish(commands.Cog):
    """
    Publish command Cog.

    TODO: Check typing
    """

    publish_channels: Union[str, List[str]]
    bot: Bot

    def __init__(self, bot: Bot):
        self.bot = bot

        self.publish_channels = get_config("publish_announcement_channels")

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        """
        Message callback.

        Action when message event is triggered.
        """
        # Converts important msg properties to strings
        channel = str(message.channel)

        # Publishes msg if it's one of the channels which should be published
        # fix the bug in this with using str
        if channel in self.publish_channels:
            try:
                await message.publish()
            except Exception as e:
                print(e)

    @app_commands.command(name="config-publisher", description="Sets the channels to be auto-published")
    @app_commands.checks.has_any_role("Staff", "Admin")
    @app_commands.guilds(env.get_guild_id())
    @app_commands.guild_only()
    async def config_publisher(self, interaction: Interaction, add: str = None, remove: str = None) -> None:
        """
        Publisher method.

        Method for configure publish cog.
        """
        response = interaction.response
        if add:
            if add in [channel.name for channel in interaction.guild.channels]:
                self.publish_channels = add_channel("publish_announcement_channels", add)
                await response.send_message(content=f'"{add}" has been added to the list of channels to be published!')
            else:
                await response.send_message(
                    content=f'"{add}" was not added from the list of channels to be published. '
                    f"Please check that it is spelled correctly and case sensitive"
                )
        if remove:
            if remove not in self.publish_channels:
                await response.send_message(
                    content=f'"{remove}" was not removed from the list of channels to be published. '
                    f"Please check that it is spelled correctly and case sensitive"
                )
            else:
                try:
                    self.publish_channels = remove_channel("publish_announcement_channels", remove)
                    await response.send_message(
                        content=f'"{remove}" has been removed from the list of channels to be published!'
                    )
                except Exception as e:
                    print(e)
                    await response.send_message(
                        content=f'"{remove}" was not removed from the list of channels to be published. '
                        f"Please check that it is spelled correctly and case sensitive"
                    )
