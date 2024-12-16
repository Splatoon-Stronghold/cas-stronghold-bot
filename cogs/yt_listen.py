import json
import os
from pathlib import Path
from typing import Any, Tuple

from discord import TextChannel, app_commands
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from googleapiclient.discovery import build

from utils import env


class YtListener(commands.Cog):
    """
    Youtube Listener.

    Cog for Youtube listener.
    """

    def __init__(self, bot: Bot):
        self.bot = bot

        # twitch and discord channel info
        base_path = (Path(os.path.abspath(__file__)) / ".." / "..").resolve()
        self.config_path = base_path / "config_data.json"

        self.API_KEY = env.get_yt_api_key()
        self.YT_CHANNEL = env.get_yt_channel_id()

        with open(self.config_path) as json_file:  # add path thing
            config_data = json.load(json_file)
            self.vod_count = config_data["vod_count"]
            self.channel = bot.get_channel(config_data["yt_text_channel_id"])

        self.youtube = build("youtube", "v3", developerKey=self.API_KEY)
        self.playlist_id = (
            self.youtube.channels()
            .list(part="snippet,contentDetails,statistics,status", id=self.YT_CHANNEL)
            .execute()["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        )
        self.playlist = None
        self.new_vod_count = self.vod_count
        self.msgs = []

    def cog_unload(self) -> None:
        """
        Unload Cog method.

        Prints error trace instead of raising an exception.
        """
        try:
            self.yt.cancel()
        except Exception as e:
            print(f"Stopping the youtube listener failed - error: {e}")

    def cog_load(self) -> None:
        """
        Load Cog method.

        Prints error trace instead of raising an exception.
        """
        try:
            self.yt.start()
        except Exception as e:
            print(f"Starting the youtube listener failed - error: {e}")

    @app_commands.command(name="config-youtube", description="Configures the youtube listener")
    @app_commands.checks.has_any_role("Staff", "Admin")
    @app_commands.guilds(env.get_guild_id())
    @app_commands.guild_only()
    async def config_youtube(self, interaction: Any, channel: TextChannel) -> None:  # noqa: ANN401
        """Configs youtube instance."""
        self.channel = channel

        with open(str(self.config_path), "r") as outfile:
            config_data = json.load(outfile)

        config_data["yt_text_channel_id"] = self.channel.id
        with open(str(self.config_path), "w") as outfile:
            json.dump(config_data, outfile)

        await interaction.response.send_message(content=f"The Youtube Listener has been set to {self.channel}!")

    @tasks.loop(seconds=30.0)
    async def yt(self) -> None:
        """Checks every 30 seconds if there's been a youtube video published."""
        self.vods()
        for msg in self.msgs:
            await self.channel.send(msg)

        with open(str(self.config_path), "r") as outfile:
            config_data = json.load(outfile)

        config_data["vod_count"] = self.vod_count
        with open(str(self.config_path), "w") as outfile:
            json.dump(config_data, outfile)

    def get_playlist(self: "YtListener") -> Tuple[Any, Any]:
        """Gets Youtube playlist."""
        playlist_re = self.youtube.playlistItems().list(part="contentDetails,snippet", playlistId=self.playlist_id)

        playlist = playlist_re.execute()
        self.playlist = playlist
        return playlist, playlist_re

    def vod_count(self) -> int:
        """Gets vod count."""
        return self.playlist["pageInfo"]["totalResults"]

    def get_new_vod_count(self) -> int:
        """Returns new vod count."""
        return self.vod_count(self) - self.vod_count

    def vods(self) -> None:
        """Setup vod count."""

        def clamp(i: int, max_num: int, min_num: int) -> int:
            """Clamp an integer between 0 and max_num."""
            return max(min(i, max_num), min_num)

        self.new_vod_count = self.get_new_vod_count()

        if self.new_vod_count == 0:
            return
        else:

            for i in range(clamp(self.new_vod_count, 5, 0)):
                vod = self.playlist["items"][i]
                channel_title = vod["snippet"]["channelTitle"]
                vid_url = "https://www.youtube.com/watch?v=" + str(vod["contentDetails"]["videoId"])

                self.msgs.append(f"{channel_title} just posted a new video! Check it out! {vid_url}")

            self.vod_count = self.vod_count()
