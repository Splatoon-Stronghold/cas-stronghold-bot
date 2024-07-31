# Cas Bot

## Running
### Configure
#### Environment variables
Define the environment variables used in [`utils/env.py`](./utils/env.py) in your environment or `.env` (`.env` takes priority):
```ini
# Discord
DISCORD_TOKEN=...
GUILD_ID=...

# Twitch
TWITCH_CLIENT=...
TWITCH_SECRET=...
TWITCH_USER=...
TWITCH_DISCORD_CHANNEL=...

# YouTube
YT_API_KEY=...
YT_CHANNEL_ID=...
```

#### Configuration files

Copy [`config_data-example.json`](./config_data-example.json), rename it to `config_data.json` and adjust the options as needed.

`time.json` will be created automatically when the bot starts.

### Prepare & install dependencies

For macOS:

```bash
python3 -m venv ./venv
source venv/bin/activate # or activate.fish, etc.
pip3 install --force-reinstall -v "pip<24.1"
pip3 install --upgrade setuptools
pip3 install -r requirements.txt
```

### Run

```bash

### Misc

#### List actually used dependencies
```bash
pipx install pipreqs
pipreqs .
```

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
