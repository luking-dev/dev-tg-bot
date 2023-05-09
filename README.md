# Development Telegram Bot
 
Telegram Bot with several features.


## Quickstart
You must run ```python env_setup.py``` to create environment variables needed by the bot, or create a ```.env``` file and defining the following variables:

- ```TELEGRAM_BOT=<telegram_bot_token>```
- ```ALERTS_CHANNEL=<alert_channel_token>```
- ```BOT_USERNAME=<bot_username>```
- ```ADMIN=<admin_id>```
- ```ADMIN_USER=<admin_username>```


## Installation

### Dependencies

```bash
pip install -r requirements.txt
```

## Creating environment variables file

You must run ```env_setup.py``` to generate a ```.env``` file which contains useful data:

```bash
python env_setup.py
```

Follow screen instructions

## Usage

```bash
python bot.py
```
