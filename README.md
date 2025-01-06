# Cas Bot

## Running
### Configure
#### Environment variables
Define the environment variables used in [`utils/env.py`](./utils/env.py) in your environment or `.env` (`.env` takes priority):
```ini
# For loading config file, not required
BOT_CONFIG_PATH=config_data.json

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

#### Setting up your own bot application

Follow instructions in [BOT_INSTALLATION.md](BOT_INSTALLATION.md)

#### Configuration files

Copy [`config_data-example.json`](./config_data-example.json), rename it to `config_data.json` and adjust the options as needed.

`time.json` will be created automatically when the bot starts.

### Prepare & install dependencies

1. [Install `pipx`](https://pipx.pypa.io/stable/installation/).
2. [Install `poetry`](https://python-poetry.org/docs/#installation):
  ```bash
  pipx install poetry
  ```
3. Install dependencies:
  ```bash
  poetry install
  ```
4. Set up precommit hooks:
  ```bash
  poetry run pre-commit install
  ```

### Run

For overriding the .env guild you can set FORCE_GUILD_ID value
```bash
export FORCE_GUILD_ID="YOUR_TARGET_GUILD_ID"
```

```bash
poetry run task bot
```

For more tasks, see [`pyproject.toml`](./pyproject.toml).

### Misc

#### List actually used direct dependencies
```bash
pipx install pipreqs
pipreqs .
```

#### Uninstall pre-commit hooks
```bash
poetry run pre-commit uninstall
```
