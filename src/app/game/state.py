import glvars as defs_sg
import katagames_sdk.engine as kataen
from DifficultyModel import DifficultyModel
from katagames_sdk.engine import BaseGameState
from katagames_sdk.engine import EngineEvTypes, EventReceiver
from sprites import SpaceBg, Nugget, ScoreBoard, Bomb, Explosion
from app.game.GameCtrl import GameCtrl


pygame = kataen.import_pygame()


class GameView(EventReceiver):

    def __init__(self, sprites):
        super().__init__()

        self.sprites = sprites
        self.pause_msg = None
        self.font = pygame.font.SysFont(None, 28)

    def set_msg_pause(self, boolval):
        if boolval:
            self.pause_msg = self.font.render(
                'Mouse cursor out of screen! Press SPACE to resume the game',
                True,
                (111, 111, 100),
                (0, 0, 0)
            )
        else:
            self.pause_msg = None

    def proc_event(self, ev, source):
        friendly_sprites = self.sprites['friendly']
        spacebg = self.sprites['spacebg']
        my_ship = self.sprites['ship']
        li_explosions = self.sprites['explo']
        danger_sprites = self.sprites['danger']

        if ev.type == EngineEvTypes.PAINT:
            screen_ref = ev.screen
            screen_ref.blit(spacebg.image, spacebg.rect.topleft)
            my_ship.draw_trail(screen_ref)

            friendly_sprites.draw(screen_ref)

            # EXPLO
            for e in li_explosions:
                if e.visible:
                    screen_ref.blit(e.image, e.rect.topleft)
                else:
                    defs_sg.tag_can_remove.add(e)

            danger_sprites.draw(screen_ref)
            screen_ref.blit(defs_sg.scoreboard.image, defs_sg.scoreboard.rect.topleft)

            if self.pause_msg:
                tmp = self.pause_msg.get_size()
                scr_size = screen_ref.get_size()
                screen_ref.blit(self.pause_msg, ((scr_size[0] - tmp[0]) // 2, (scr_size[1] - tmp[1]) // 2))

            kataen.gfx_updater.display_update()


class GameState(BaseGameState):
    def __init__(self, gsid, gsname):
        super().__init__(gsid, gsname)
        self._v = self._ctrl = None
        self.diffmod = None

    def enter(self):
        """
        :return: a tuple (score: int, abort: bool)
        """
        if defs_sg.cdiff:
            defs_sg.cdiff.reset()
            self.diffmod = defs_sg.cdiff
        else:
            self.diffmod = DifficultyModel()
            defs_sg.cdiff = self.diffmod

        diff = self.diffmod

        if defs_sg.music_obj is None:
            print('music starts')
            defs_sg.music_obj = pygame.mixer.Sound(defs_sg.ASSETS[-5])
            defs_sg.music_obj.set_volume(0.08)
            defs_sg.music_obj.play(-1)

        # reset it
        defs_sg.scoreboard = ScoreBoard()
        # optim for the web version (load big img gfx)
        Explosion.preload_animation()

        li_bombs = []
        my_ship = defs_sg.ship
        my_ship.engine_sound.play(-1)

        nugget = Nugget()
        spacebg = SpaceBg()
        li_explosions = list()

        for k in range(diff.nb_bombs):
            li_bombs.append(Bomb())

        friendly_sprites = pygame.sprite.Group(nugget, my_ship)
        danger_sprites = pygame.sprite.Group(*li_bombs)

        dico = {
            'friendly': friendly_sprites,
            'danger': danger_sprites,
            'ship': my_ship,
            'spacebg': spacebg,
            'explo': li_explosions
        }

        # - ajout composants
        self._v = GameView(dico)
        self._ctrl = GameCtrl(
            diff,
            li_explosions,
            my_ship,
            nugget,
            li_bombs,
            spacebg,
            danger_sprites,
            friendly_sprites,
            self._v
        )
        self._v.turn_on()
        self._ctrl.turn_on()
        pygame.mouse.set_visible(False)

    def release(self):
        defs_sg.ship.engine_sound.stop()

        self._v.turn_off()
        self._ctrl.turn_off()

        print('new score obtained: ', end='')
        print("{:,}$".format(defs_sg.scoreboard.score))

        defs_sg.last_score = defs_sg.scoreboard.score
