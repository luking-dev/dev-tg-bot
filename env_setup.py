import os

TELEGRAM_BOT = input("> Type your Telegram Bot API Token: ")
ALERTS_CHANNEL = input("> Type your Alerts Channel ID: ")
BOT_USERNAME = input("> Type your bot username: ")
ADMIN = input("> Type your user/admin ID: ")
ADMIN_USER = input("> Type your admin username: ")
MULTIMEDIA_DIR = os.path.join(input("> Type the directorie in which bot must download your multimedia: "))

file = open(".env", "w")
with file:
    file.writelines(f'''\
TELEGRAM_BOT={TELEGRAM_BOT}
ALERTS_CHANNEL={ALERTS_CHANNEL}
BOT_USERNAME={BOT_USERNAME}
ADMIN={ADMIN}
ADMIN_USER={ADMIN_USER}
MULTIMEDIA_DIR={MULTIMEDIA_DIR}\
''')
