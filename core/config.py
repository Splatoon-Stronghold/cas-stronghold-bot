from __future__ import annotations
import attr
import json
from pathlib import Path
from typing import List, Dict, Any, Union


@attr.s(auto_attribs=True)
class BasePlatformConfig(attr.AttrsInstance):
    announcement_channels: List[str] | None = None
    text_channel_id: int | None = None
    vod_count: int | None = None
    _platform_name: str | None = None

    def get_json(self) -> Dict[str, Any]:
        return attr.asdict(self)


@attr.s(auto_attribs=True)
class YoutubePlatformConfig(BasePlatformConfig):
    _platform_name = 'Youtube'


@attr.s(auto_attribs=True)
class TwitchPlatformConfig(BasePlatformConfig):
    _platform_name = 'Twitch'
    # The platforms should have same data structure
    announcement_channels: Dict[str, Any] = None


@attr.s(auto_attribs=True)
class PublishPlatformConfig(BasePlatformConfig):
    # This "publish" category should have a name ?
    # _platform_name = 'Publish'
    pass


@attr.s(auto_attribs=True)
class BotConfig(attr.AttrsInstance):
    youtube: YoutubePlatformConfig
    twitch: TwitchPlatformConfig
    publish: PublishPlatformConfig

    @classmethod
    def factory(
            cls,
            vod_count: int,
            youtube_text_channel_id: int,
            youtube_channels: List[str] = None,
            twitch_channels: Dict[str, Any] = None,
            publish_channels: List[str] = None,
            twitch_text_channel_id: int = None,
            publish_text_channel_id: int = None
    ) -> BotConfig:
        bot_config = cls(
            youtube=YoutubePlatformConfig(
                announcement_channels=youtube_channels,
                vod_count=vod_count,
                text_channel_id=youtube_text_channel_id
            ),
            twitch=TwitchPlatformConfig(
                announcement_channels=twitch_channels,
                # vod_count=0,  # Once we have this value we can uncomment this
                text_channel_id=twitch_text_channel_id
            ),
            publish=PublishPlatformConfig(
                announcement_channels=publish_channels,
                # vod_count=0,  # Once we have this value we can uncomment this
                text_channel_id=publish_text_channel_id
            )
        )

        return bot_config

    def get_json(self) -> Dict[str, Any]:
        return attr.asdict(self)

    def get_store_json(self) -> Dict[str, Any]:
        return {
            "youtube_announcement_channels": self.youtube.announcement_channels,
            "vod_count": self.youtube.vod_count,
            "yt_text_channel_id": self.youtube.text_channel_id,
            "twitch_announcement_channels": self.twitch.announcement_channels,
            "publish_announcement_channels": self.publish.announcement_channels
        }


def generate_bot_config(config_data: Dict[str, Any] = None) -> BotConfig:
    """
    This function will generate a BotConfig instance from a dictionary
    """
    if not config_data:
        config_data = dict()
    youtube_channels = config_data.get("youtube_announcement_channels", [])
    publish_channels = config_data.get("publish_announcement_channels", [])
    twitch_channels = config_data.get("twitch_announcement_channels", {})
    vod_count = config_data.get("vod_count", 0)
    youtube_text_channel_id = config_data.get("yt_text_channel_id", 0)
    twitch_text_channel_id = config_data.get("twitch_text_channel_id", 0)
    publish_text_channel_id = config_data.get("publish_text_channel_id", 0)
    return BotConfig.factory(
        youtube_channels=youtube_channels,
        twitch_channels=twitch_channels,
        publish_channels=publish_channels,
        vod_count=vod_count,
        youtube_text_channel_id=youtube_text_channel_id,
        twitch_text_channel_id=twitch_text_channel_id,
        publish_text_channel_id=publish_text_channel_id
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


def get_bot_config(
        file_path: Union[str | Path] = None,
        config_data: Union[Dict[str, Any] | None] = None
) -> BotConfig:
    """
    This function encapsulates the whole BotConfig retrieving

    Will read from a path for a json file for getting an instance,
    will accept a dictionary for getting a instance or will accept
    no parameters and will build it by default

    Parameters
    ----------
    file_path:
        The path for the JSON file can be a string or Path object
    config_data:
        The dictionary for the BotConfig instance

    Returns
    -------
        BotConfig: A Bot config instance
    """
    if file_path:
        return load_bot_config_from_file(file_path)
    return generate_bot_config(config_data)
