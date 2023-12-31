# Cas Bot

## Current To Do:

- /uptime : Polish output for displaying uptime since bot was last online.
- /config-twitch : Automation for Twitch livestream pings: add/remove names of channels to send to.
- /process-replays : Automation for Replay VODs service. Needs:
  - Support for temporarily storing images & videos (large files).
  - Ability to download a video file from a Google Drive share link.
  - Ability to upload said video file to YouTube using information from Discord command.
  - Ability to determine type of YT thumbnail to use for video based on VOD type.
  - Ability to create a YouTube video name using information from Discord command.
  - Ability to edit YouTube description with custom text from a Discord message that can be edited (allows non-tech staff to edit upload info)
- Documentation of current Discord bot commands

## Completed:
- Create base framework for Discord bot.
- Add support for responding to Discord commands. Needs:
  - Generic response to test ability to respond to commands.
- Add in Auto Publisher functions. Needs:
  - Ability to automatically publish messages in announcement channels.
  - Support for commands to add & set up channels for auto publishing.
- Twitch livestream pings. Needs:
  - Support for Twitch livestreams.
  - Support for commands to set up Twitch livestreams for text channels.
- YouTube livestream pings. Needs:
  - Support for YouTube livestreams.
  - Support for commands to set up YouTubve livestreams for text channels.
