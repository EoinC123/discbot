from distutils.util import strtobool
from datetime import date
from pathlib import Path

import logging
import os

PROJECT_BASE_DIR = os.path.dirname(os.path.realpath(__file__))

NAME_TO_MUSIC_MAPPING = {
    111233508520767488: "fuck_books.mp3",  # Eoin
    145350084983390208: "itwasmebarry.mp3",  # Ronan
    120990968173297665: "windows-xp-startup.mp3",  # Archie
    186588349807591434: "im-fast-as-f-boi.mp3",  # Paul
    219639243733991424: "epic-sax-guy.mp3",  # Peter
    100295458856931328: "08-_Fuckin_Gay.mp3",  # David A
    223485287974699008: "jawohl.mp3",  # Dave D
    221240253472702466: "trump-cum.mp3",  # Jason
    292454324368572416: "build-a-wall.mp3",  # Scott
    155807750344015872: "egel.mp3",  # Nigel
    182658393549438986: "wide-putin.mp3",  # Darren
    176758486410067987: "Wont_Fuck_Girls.mp3",  # Conor
    234765588847656960: "ytug.mp3", # Olan
    178232645832933376: "wake_up_liberal.mp3", # Kieran
}

PLAYLISTS = {
    "gachi": [
        # "https://www.youtube.com/watch?v=c9JNp6kdKqU&ab_channel=GachiFingers", # need to "confirm age"
        "https://www.youtube.com/watch?v=NdqbI0_0GsM&ab_channel=flox_",
        "https://www.youtube.com/watch?v=PFyMhNZB-lc&ab_channel=Bossofthisgym",
        "https://www.youtube.com/watch?v=kOCxHu_F5xo&ab_channel=Cypac",
        "https://www.youtube.com/watch?v=9Ebdpv0KOlM&ab_channel=Cypac",
        "https://www.youtube.com/watch?v=z2OGa6RyYDE",
    ],
}


EXECUTABLE_FOLDER = os.path.join(PROJECT_BASE_DIR, "executables")
SOUND_EFFECTS_FOLDER = os.path.join(PROJECT_BASE_DIR, "sound_effects")

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

GAMBLING_DB = os.path.join(PROJECT_BASE_DIR, "gamble.db")

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