from distutils.util import strtobool
from datetime import date
from pathlib import Path

import logging
import os

PROJECT_BASE_DIR = os.path.dirname(os.path.realpath(__file__))
EXECUTABLE_FOLDER = os.path.join(PROJECT_BASE_DIR, "executables")
ALLOW_PLAY = bool(strtobool(os.environ.get("ALLOW_PLAY", "True")))

# define the reactions here, so they can be changed from one place
REACTIONS = {
    "crying_laughing": "😂",
    "cum_face": "😩",
    "raised_eye": "🤨",
    "smirk": "😏",
    "drooling": "🤤",
    "blush": "🤔",
    "point_right":"👉",
    "point_left": "👈",
    "stony_boi": "🗿",
    "cigarette": "🚬",
    "banana": "🍌",
    "rain": "💦",
    "aubergine": "🍆",
    "red_b": "🅱️",
    "red_100": "💯",
    "wheelchair": "🧑‍🦽",
    "wheelchair_sign": "♿",
    "male_sign": "♂️",
    # "female_sign": "♀️", # removed, as we do not recognise women in this server
    "ok": "👌🏿",

    "a": "🇦",
    "b": "🇧",
    "c": "🇨",
    "d": "🇩",
    "e": "🇪",
    "f": "🇫",
    "g": "🇬",
    "h": "🇭",
    "i": "🇮",
    "j": "🇯",
    "k": "🇰",
    "l": "🇱",
    "m": "🇲",
    "n": "🇳",
    "o": "🇴",
    "p": "🇵",
    "q": "🇶",
    "r": "🇷",
    "s": "🇸",
    "t": "🇹",
    "u": "🇺",
    "v": "🇻",
    "w": "🇼",
    "x": "🇽",
    "y": "🇾",
    "z": "🇿",

    "0": "0️⃣",
    "1": "1️⃣",
    "2": "2️⃣",
    "3": "3️⃣",
    "4": "4️⃣",
    "5": "5️⃣",
    "6": "6️⃣",
    "7": "7️⃣",
    "8": "8️⃣",
    "9": "9️⃣",
    "10": "🔟",

    "hearts": "♥",
    "spades": "♠",
    "diamonds": "♦",
    "clubs": "♣",
}

# logger init
DEBUG = False
LOG_DIR = os.path.join(PROJECT_BASE_DIR, "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

log_filename = f"{date.today().strftime('%Y_%m_%d')}_cumlog.log"
full_log_name = f"{os.path.join(LOG_DIR, log_filename)}"
Path(full_log_name).touch(exist_ok=True)

# noinspection PyArgumentList
logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.FileHandler(full_log_name),
        logging.StreamHandler()
    ],
    level=logging.DEBUG if DEBUG else logging.INFO,
    )
LOGGER = logging.getLogger('BaseLogger')
