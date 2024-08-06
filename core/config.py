from __future__ import annotations
from typing import List, Dict, Any

import attr


@attr.s(auto_attribs=True)
class AnnouncementChannels:
    youtube: List[str]
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