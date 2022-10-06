# any configuration should be stored here
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath("bot.py"))
os.chdir(BASE_DIR)

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ALERTS_CHANNEL = os.getenv("ALERTS_CHANNEL")
BOT_USERNAME = os.getenv("BOT_USERNAME")
ADMIN = os.getenv("ADMIN")
ADMIN_USER = os.getenv("ADMIN_USER")
WEBCAM_USER = os.getenv("WEBCAM_USER")
WEBCAM_PASSWORD = os.getenv("WEBCAM_PASSWORD")
WEBCAM_IP = os.getenv("WEBCAM_IP")
WEBCAM_PORT = os.getenv("WEBCAM_PORT")
INSTAGRAM_USER = os.getenv("INSTAGRAM_USER")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
MULTIMEDIA_DIR = os.getenv("MULTIMEDIA_DIR")

data = {
    "units": {
        "seconds": {
            "factor": 1,
            "text": "second"
        },
        "minutes": {
            "factor": 1,
            "text": "minute"
        },
        "hours": {
            "factor": 1,
            "text": "hour"
        },
    }
}
