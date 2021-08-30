"""
author: Thomas "wkta" Iwaszko
MIT Licence
"""


# **> CONSTANTS <**
ASSET_DIR = 'assets'
ASSETS = [  # warning: the order matters!
    'myspace.png',  # used for the bg,
    'my-plane.png',  # spacecraft
    'sc-trail.png',  # spacecraft's trail

    'minerals.png',  # minerals u can gather for cash
    'space_mine.png',  # obstacles that wrecks the spacecraft
    'sc-trail-maxpower.png',

    'explo_sprsheet.png',  # animation explo
    '',
    '',

    # - rule: always access sound assets
    # by ussing a negative index value e.g. ASSETS[-2]
    'Interstellar.ogg',  # music playing throughout the game
    'fast-reactor.wav',  # turbomode!
    'get-cash.wav',  # when you pickup smth good
    'explosion_002.wav',  # when an obstacle is hit
    'slow-reactor.wav',  # ambiant sound
]
VER = '0.2104'
CAPTION = 'Space Gatherer v.' + VER
FPS_CAP = 45

# (global game balancing)
BOMB_RECT_RATIO = 0.6
STEERING_LIMIT = 17  # px


# **> VARIABLES <**
cdiff = None  # current difficulty, instance of DifficultyModel
tag_can_remove = set()
scoreboard = None
abort_sig = None
top_score = 0
last_score = None
aborting = False
ship = None
music_obj = None
