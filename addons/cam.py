import os
import requests
from urllib.parse import urljoin
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

WEBCAM_USER = os.getenv("WEBCAM_USER")
WEBCAM_PASSWORD = os.getenv("WEBCAM_PASSWORD")
WEBCAM_IP = os.getenv("WEBCAM_IP")
WEBCAM_PORT = os.getenv("WEBCAM_PORT")
WEBCAM_BASE=f"http://{WEBCAM_IP}:{WEBCAM_PORT}"


def photo(name="photo.jpg"):
    r = requests.get(urljoin(WEBCAM_BASE, "shot.jpg"), auth=HTTPBasicAuth(WEBCAM_USER, WEBCAM_PASSWORD))
    file = open(name, "wb")
    file.write(r.content)
    file.close()
    # path = os.path.join(BASE_DIR, name)

    return name

def torch(state=True):
    if state:
        requests.get(urljoin(WEBCAM_BASE, "enabletorch"), auth=HTTPBasicAuth(WEBCAM_USER, WEBCAM_PASSWORD))
    else:
        requests.get(urljoin(WEBCAM_BASE, "disabletorch"), auth=HTTPBasicAuth(WEBCAM_USER, WEBCAM_PASSWORD))

def nightvision(state=True):
    night_vision_average_default = "settings/night_vision_average?set=2"
    night_vision_gain_default = "settings/night_vision_gain?set=1.0"
    night_vision_average = "settings/night_vision_average?set=16"
    night_vision_gain = "settings/night_vision_gain?set=4.0"
    night_vision_on = "settings/night_vision?set=on"
    night_vision_off = "settings/night_vision?set=off"
    
    if state:
        requests.get(urljoin(WEBCAM_BASE, night_vision_average), auth=HTTPBasicAuth(WEBCAM_USER, WEBCAM_PASSWORD))
        requests.get(urljoin(WEBCAM_BASE, night_vision_gain), auth=HTTPBasicAuth(WEBCAM_USER, WEBCAM_PASSWORD))
        requests.get(urljoin(WEBCAM_BASE, night_vision_on), auth=HTTPBasicAuth(WEBCAM_USER, WEBCAM_PASSWORD))
    else:
        requests.get(urljoin(WEBCAM_BASE, night_vision_average_default), auth=HTTPBasicAuth(WEBCAM_USER, WEBCAM_PASSWORD))
        requests.get(urljoin(WEBCAM_BASE, night_vision_gain_default), auth=HTTPBasicAuth(WEBCAM_USER, WEBCAM_PASSWORD))
        requests.get(urljoin(WEBCAM_BASE, night_vision_off), auth=HTTPBasicAuth(WEBCAM_USER, WEBCAM_PASSWORD))

def record_video(state=True):
    if state:
        requests.get(urljoin(WEBCAM_BASE, "startvideo"), auth=HTTPBasicAuth(WEBCAM_USER, WEBCAM_PASSWORD))
    else:
        requests.get(urljoin(WEBCAM_BASE, "stopvideo"), auth=HTTPBasicAuth(WEBCAM_USER, WEBCAM_PASSWORD))
