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

# YouTube
YT_API_KEY=...
YT_CHANNEL_ID=...

# Logging Channel
LOGGING_CHANNEL_NAME=...
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
# Remember to do:
source venv/bin/activate # or activate.fish, etc.

python3 main.py
```