from discord.ext import commands
from discord import app_commands
from discord import Interaction
import json
import os

config_path = ''.join(os.path.abspath(__file__).split('cogs/publish.py')[0] + ('config_data.json'))

class Publish(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open(config_path) as json_file: # add path thing
            self.config_data = json.load(json_file)


    @commands.Cog.listener()
    async def on_message(self,message):
        # Converts important msg properties to strings
        channel = str(message.channel)

        # Publishes msg if it's one of the channels which should be published
        if channel in self.config_data['announcement_channels']:
            try:
                await message.publish()
            except Exception as e:
                print(e)
        

        
    @app_commands.command(name = "config-publisher", description = "Sets the channels to be auto-published")
    @app_commands.checks.has_any_role('Staff', 'Admin')
    async def config_publisher(self, interaction: Interaction, add: str = None, remove: str = None):
        response = interaction.response
        if add != None:
            if add in str(interaction.guild.channels):
                self.config_data['announcement_channels'].append(add)
                await response.send_message(content=f'"{add}" has been added to the list of channels to be published!')
            else:
                await response.send_message(content=f'"{add}" was not added from the list of channels to be published. Please check that it is spelled correctly and case sensitive')
        if remove != None:
            try:
                self.config_data['announcement_channels'].remove(remove)
                await response.send_message(content=f'"{remove}" has been removed from the list of channels to be published!')
            except:
                await response.send_message(content=f'"{remove}" was not removed from the list of channels to be published. Please check that it is spelled correctly and case sensitive')
            

        with open(config_path, "w") as outfile:
            json.dump(self.config_data, outfile)