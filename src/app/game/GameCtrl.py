import defs_sg
from katagames_sdk.engine import EngineEvTypes, EventReceiver
from sprites import Explosion, Bomb
import katagames_sdk.engine as kataen


pygame = kataen.import_pygame()


class GameCtrl(EventReceiver):

    def __init__(self, explo, ship, nugget, li_bombs, spacebg, danger_spr, friendly_spr, ref_view):
        super().__init__()

        self.danger_spr = danger_spr
        self.explosions = explo
        self.friendly_spr = friendly_spr

        self.li_bombs = li_bombs
        self.ship = ship
        self.nugget = nugget
        self.space_bg = spacebg

        self._v = ref_view
        self.paused = False

    def _update_gamelogic(self):
        li_bombs = self.li_bombs

        # check if there are enough bombs... If not, we add one
        if len(li_bombs) < defs_sg.nb_bombs:
            obj = Bomb()
            li_bombs.append(obj)
            self.danger_spr.add(obj)

        if pygame.sprite.collide_rect_ratio(0.8)(self.ship, self.nugget):
            # we manage to gather a nugget
            self.ship.snd_yay.play()
            self.nugget.reset()
            defs_sg.scoreboard.score += defs_sg.nugget_reward

        hit_bombs = pygame.sprite.spritecollide(
            self.ship,
            self.danger_spr,
            False,  # kill
            pygame.sprite.collide_rect_ratio(defs_sg.BOMB_RECT_RATIO)
        )

        if hit_bombs:
            self.ship.snd_boom.play()

            for elt in hit_bombs:
                self.explosions.append(
                    Explosion(self.ship.rect.center)
                )
                self.explosions.append(
                    Explosion(elt.rect.center)
                )
                elt.reset()

            defs_sg.scoreboard.lives -= len(hit_bombs)

            if defs_sg.scoreboard.lives <= 0:
                self.pev(EngineEvTypes.POPSTATE)

        self.space_bg.update()
        self.friendly_spr.update()
        self.danger_spr.update()

        # gestion explosions
        if len(defs_sg.tag_can_remove):
            for elt in defs_sg.tag_can_remove:
                self.explosions.remove(elt)
            defs_sg.tag_can_remove.clear()
        for e in self.explosions:
            e.update()

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.LOGICUPDATE:
            if not self.paused:
                self._update_gamelogic()
            defs_sg.scoreboard.update()

        elif ev.type == pygame.QUIT:
            self.pev(EngineEvTypes.POPSTATE)

        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            self.pev(EngineEvTypes.POPSTATE)

        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:
            if self.paused:
                self.unpause_game()

        elif ev.type == pygame.constants.WINDOWLEAVE:
            if not self.paused:
                self.pause_game()

    def pause_game(self):
        self._v.set_msg_pause(True)
        self.paused = True
        pygame.mouse.set_visible(True)

    def unpause_game(self):
        self._v.set_msg_pause(False)
        self.paused = False
        pygame.mouse.set_visible(False)
