"""
author: Thomas "wkta" Iwaszko

 MIT Licence
"""
from os import sep


# temporary?
tag_can_remove = set()
scoreboard = None
abort_sig = None

# - comm between game states
top_score = 0
last_score = None
aborting = False

# - gl in- game vars
nuggets_out = 0
nb_bombs = 2  # will get increased later on
booster_flag = False
nugget_reward = 100
ship = None
music_obj = None

difficulty = 1  # starts at 1, but gets increased every STEP_FOR_DIFF_INCREM
simu_avatar_speed = 2


def reset_gl_game_vars():
    global difficulty, simu_avatar_speed, nuggets_out, nb_bombs, booster_flag, nugget_reward

    nuggets_out = 0
    nb_bombs = 2
    booster_flag = False
    nugget_reward = 100

    difficulty = 1
    simu_avatar_speed = 2


# - const
VER = '0.2104'
CAPTION = 'Space Gatherer v.' + VER
print(CAPTION)
print(' ~ ~ ~ welcome ~ ~ ~')
ASSET_DIR = 'assets'
ASSETS = [  # order matters!
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


def update_paths():
    global ASSETS
    for k, elt in enumerate(ASSETS):
        ASSETS[k] = sep.join((ASSET_DIR, ASSETS[k]))


# - const (game balancing)
STEP_FOR_DIFF_INCREM = 3  # nb of nuggets out for difficulty increase
FPS_CAP = 45
BOMB_RECT_RATIO = 0.6
STEERING_LIMIT = 17  # px
