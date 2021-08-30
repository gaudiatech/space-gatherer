import glvars
import glvars as defs_sg
import katagames_sdk.api as katapi
import katagames_sdk.engine as kataen
from app.intro.IntroView import IntroView
from katagames_sdk.engine import BaseGameState, EventReceiver


pygame = kataen.import_pygame()


class MiniEvHandler(EventReceiver):
    def __init__(self):
        super().__init__()
        self.gctrl = None

    def proc_event(self, ev, source):
        if self.gctrl is None:
            self.gctrl = kataen.get_game_ctrl()

        if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
            self.gctrl.halt()
            defs_sg.aborting = True


class IntroState(BaseGameState):
    def __init__(self, stid, stname):
        super().__init__(stid, stname)
        self._c0 = None
        self._view_w_buttons = None

    @staticmethod
    def _refresh_katagames_info():
        glvars.mobi_balance = katapi.get_user_balance(glvars.acc_id)
        katapi.set_curr_game_id(glvars.UNIQUE_GAME_ID)
        glvars.challengeprice = katapi.get_challengeprice()

    def enter(self):
        print('declarations ds intro_state...')
        self._view_w_buttons = IntroView()

        IntroState._refresh_katagames_info()
        self._view_w_buttons.init_instruction()

        self._c0 = MiniEvHandler()

        self._view_w_buttons.turn_on()
        self._c0.turn_on()

    def resume(self):
        IntroState._refresh_katagames_info()
        defs_sg.top_score = max(defs_sg.top_score, defs_sg.last_score)

        self._view_w_buttons.init_instruction()

        pygame.mouse.set_visible(True)
        # already done when exit state "Game"
        # defs_sg.ship.engine_sound.stop()
        # ...but this is required
        defs_sg.ship.reset()

        self._view_w_buttons.turn_on()
        self._c0.turn_on()

    def pause(self):
        self._view_w_buttons.turn_off()
        self._c0.turn_off()
        # to be 100% sure we dont have a bug with buttons, we add:
        kataen.get_manager().soft_reset()

    def release(self):
        if defs_sg.music_obj:
            print('music stops')
            defs_sg.music_obj.stop()
        self.pause()
        self._c0 = self._view_w_buttons = None
