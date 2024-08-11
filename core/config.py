from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict, Any, Union

import attr


@attr.s(auto_attribs=True)
class AnnouncementChannels:
    youtube: List[str]
    # TODO: Depending on Twitch channel structure, this could be a class
    twitch: Dict[str, Any]
    publish: List[str]

    def get_json(self) -> Dict[str, Any]:
        return attr.asdict(self)

    @classmethod
    def factory(
            cls,
            youtube_channels: List[str],
            twitch_channels: Dict[str, Any],
            publish_channels: List[str],
    ) -> AnnouncementChannels:
        announcement_channels = cls(
            youtube=youtube_channels,
            twitch=twitch_channels,
            publish=publish_channels,
        )

        return announcement_channels


@attr.s(auto_attribs=True)
class BotConfig:
    announcement_channels: AnnouncementChannels
    vod_count: int
    youtube_text_channel_id: int

    @classmethod
    def factory(
            cls,
            vod_count: int,
            youtube_text_channel_id: int,
            youtube_channels: List[str] = None,
            twitch_channels: Dict[str, Any] = None,
            publish_channels: List[str] = None,
    ) -> BotConfig:
        bot_config = cls(
            announcement_channels=AnnouncementChannels.factory(
                youtube_channels=youtube_channels if youtube_channels else [],
                twitch_channels=twitch_channels if twitch_channels else dict(),
                publish_channels=publish_channels if publish_channels else [],
            ),
            vod_count=vod_count,
            youtube_text_channel_id=youtube_text_channel_id,
        )

        return bot_config

    def get_json(self) -> Dict[str, Any]:
        return attr.asdict(self)

    def get_store_json(self) -> Dict[str, Any]:
        return {
            "youtube_announcement_channels": self.announcement_channels.youtube,
            "vod_count": self.vod_count,
            "yt_text_channel_id": self.youtube_text_channel_id,
            "twitch_announcement_channels": self.announcement_channels.twitch,
            "publish_announcement_channels": self.announcement_channels.publish
        }


def generate_bot_config(config_data: Dict[str, Any] = None) -> BotConfig:
    """
    This fucntion will generate a BotConfig instance from a dictionary
    """
    if not config_data:
        config_data = dict()
    youtube_channels = config_data.get("youtube_announcement_channels", [])
    publish_channels = config_data.get("publish_announcement_channels", [])
    twitch_channels = config_data.get("twitch_announcement_channels", {})
    vod_count = config_data.get("vod_count", 0)
    youtube_text_channel_id = config_data.get("yt_text_channel_id", 0)
    return BotConfig.factory(
        youtube_channels=youtube_channels,
        twitch_channels=twitch_channels,
        publish_channels=publish_channels,
        vod_count=vod_count,
        youtube_text_channel_id=youtube_text_channel_id,
    )


def load_bot_config_from_file(file_path: Union[str | Path]) -> BotConfig:
    """
    This function will read a JSON file from path (relative or absolute)
    and return a pre-filled BotConfig instance
    """
    return generate_bot_config(
        json.load(
            open(file_path, encoding='utf-8')
        )
    )
