from katagames_sdk.engine import BaseGameState, EngineEvTypes, EventReceiver
import katagames_sdk.engine as kataen
from sprites import Spacecraft, SpaceBg
import defs_sg


pygame = kataen.import_pygame()


class IntroView(EventReceiver):

    def __init__(self):
        super().__init__()
        defs_sg.ship = Spacecraft()
        self.space_bg = SpaceBg()

        self.allspr = pygame.sprite.Group(self.space_bg, defs_sg.ship)
        ins_font = pygame.font.SysFont(None, 30)

        instructions = (
            "{} | HIGHSCORE is: {:,}$".format(defs_sg.CAPTION, defs_sg.top_score),
            "",
            "Instructions: you're a reckless gatherer hunting for valuable",
            "minerals in the most dangerous part of the Galaxy.",
            "",
            "Fly over small Planetoids to gather minerals, but watch out",
            "for bombs; remainings of the last great space conflict.",
            "Your spaceship would explode if hit by too many explosions.",
            "Good luck!",
            "",
            "Click your ship to start / Press escape to quit"
        )
        nb_ins = len(instructions)
        self.ins_labels = list()

        for k, ins_txt in enumerate(instructions):
            if k == 0:
                col = (255, 255, 0)
            elif k == nb_ins - 1:
                col = (233, 16, 8)
            else:
                col = (111, 111, 90)
            temp_label = ins_font.render(ins_txt, True, col, (0, 0, 0))
            self.ins_labels.append(temp_label)

    def proc_event(self, ev, source):
        if ev.type == kataen.EngineEvTypes.PAINT:
            screen_ref = ev.screen
            self.allspr.draw(screen_ref)
            for i in range(len(self.ins_labels)):
                screen_ref.blit(self.ins_labels[i], (192, (1 + i) * 30))


class MiniEvHandler(kataen.EventReceiver):
    def __init__(self):
        super().__init__()
        self.gctrl = None

    def proc_event(self, ev, source):
        if self.gctrl is None:
            self.gctrl = kataen.get_game_ctrl()

        if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
            self.gctrl.halt()
            defs_sg.aborting = True

        elif ev.type == pygame.MOUSEBUTTONDOWN:
            self.pev(EngineEvTypes.PUSHSTATE, state_ident=1)  # 1 is GameStates.GAME


class IntroState(BaseGameState):
    def __init__(self, stid, stname):
        super().__init__(stid, stname)
        self._c0 = None
        self._v = None

    def enter(self):
        print('declarations ds intro_state...')

        self._v = IntroView()
        self._c0 = MiniEvHandler()

        self._v.turn_on()
        self._c0.turn_on()

    def release(self):
        if defs_sg.music_obj:
            print('music stops')
            defs_sg.music_obj.stop()

        self.pause()

    def pause(self):
        self._c0.turn_off()

    def resume(self):
        pygame.mouse.set_visible(True)
        # already done when exit state "Game"
        # defs_sg.ship.engine_sound.stop()

        # ...but this is required
        defs_sg.ship.reset()

        defs_sg.top_score = max(defs_sg.top_score, defs_sg.last_score)

        self._v = IntroView()
        self._v.turn_on()
        self._c0.turn_on()
