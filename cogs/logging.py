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
        pass

    # TODO implement delete messages
    @commands.Cog.listener()
    async def on_message_delete(self,message):
        pass

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
