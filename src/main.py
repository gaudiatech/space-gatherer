"""
 a basic video game coded fast
 by Thomas Iwaszko,
 2021 Aug 4th -18th | (c)Gaudia Tech Inc.
 ported to the katagames-SDK on Aug 30th

 MIT license

 Thomas works to make https://kata.games possible...
 We are recruiting game devs/ python coders, so if
 you like well-written python games, get in touch!

 email: contact@kata.games
"""

import glvars
import katagames_sdk.engine as kataen
from katagames_sdk.engine import enum_builder


pygame = kataen.import_pygame()
GameStates = enum_builder(
    'Intro',
    'Game'
)


def run_game():
    kataen.init(kataen.HD_MODE)

    if not kataen.runs_in_web():
        def update_paths():
            from os import sep
            for k, elt in enumerate(glvars.ASSETS):
                glvars.ASSETS[k] = sep.join((glvars.ASSET_DIR, glvars.ASSETS[k]))
        update_paths()

    kataen.tag_multistate(GameStates, glvars, False)
    pygame.mixer.init()

    gctrl = kataen.get_game_ctrl()
    gctrl.turn_on()
    gctrl.loop()

    print('GAME OVER.')
    print('Best score: {:,}$'.format(glvars.top_score))

    kataen.cleanup()


if __name__ == '__main__':
    run_game()
