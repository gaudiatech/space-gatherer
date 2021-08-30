import random

import glvars
import glvars as defs_sg
import katagames_sdk.api as katapi
import katagames_sdk.engine as kataen
from katagames_sdk.engine import EventReceiver, EngineEvTypes, CgmEvent, gui
from sprites import Spacecraft, SpaceBg


pygame = kataen.import_pygame()


def cb_playgame():
    if glvars.mobi_balance >= glvars.challengeprice:
        tmp = katapi.pay_for_challenge(glvars.acc_id)
        # tmp contains payment_feedback, numero_challenge, chall_seed
        if not tmp[0]:
            print('something s wrong with starting the challenge!')
        else:
            glvars.challenge_id = tmp[1]
            random.seed(tmp[2])  # seed has been set (constant random gen. for 1 challenge)
            print('challenge is starting...')
            kataen.get_manager().post(CgmEvent(EngineEvTypes.PUSHSTATE, state_ident=glvars.GameStates.Game))


class IntroView(EventReceiver):

    X_ALIGN = 192

    def __init__(self):
        super().__init__()
        defs_sg.ship = Spacecraft()
        self.space_bg = SpaceBg()

        self.allspr = pygame.sprite.Group(self.space_bg, defs_sg.ship)
        self.ins_font = pygame.font.Font(None, 30)
        bt_font = pygame.font.Font(None, 44)

        self.ins_labels = list()

        # create buttons
        bt_pos = [self.X_ALIGN, 375]
        self._bt_play = gui.Button(bt_font, 'Confirm and play', bt_pos, callback=cb_playgame)

        def back_effect():
            kataen.get_manager().post(CgmEvent(EngineEvTypes.POPSTATE))
        self._bt_cancel = gui.Button(bt_font, 'Exit', (bt_pos[0], bt_pos[1] + 50), callback=back_effect)

    def init_instruction(self):
        del self.ins_labels[:]
        instructions = (
            "{} |top score in this session: {:,}$".format(defs_sg.CAPTION, defs_sg.top_score),
            "Instructions: you're a reckless gatherer hunting for valuable",
            "minerals in the most dangerous part of the Galaxy.",
            "",
            "Fly over small Planetoids to gather minerals, but watch out",
            "for bombs; remainings of the last great space conflict.",
            "Your spaceship would explode if hit by too many explosions.",
            "Good luck!",
            "",
            "you have {} MOBI, one attempt requires {} MOBI".format(glvars.mobi_balance, glvars.challengeprice),
            "Click the button below to start"
        )
        nb_ins = len(instructions)
        for k, ins_txt in enumerate(instructions):
            if k == 0:
                col = (255, 255, 0)
            elif k == nb_ins - 1:
                col = (233, 16, 8)
            else:
                col = (111, 111, 90)
            temp_label = self.ins_font.render(ins_txt, True, col, (0, 0, 0))
            self.ins_labels.append(temp_label)

    def turn_off(self):
        super().turn_off()
        self._bt_cancel.turn_off()
        self._bt_play.turn_off()

    def turn_on(self):
        super().turn_on()
        self._bt_cancel.turn_on()
        self._bt_play.turn_on()

    def proc_event(self, ev, source):
        if ev.type == kataen.EngineEvTypes.PAINT:
            screen_ref = ev.screen
            self.allspr.draw(screen_ref)

            for i in range(len(self.ins_labels)):
                screen_ref.blit(self.ins_labels[i], (self.X_ALIGN, (1 + i) * 30))

            ev.screen.blit(self._bt_play.image, self._bt_play.position)
            ev.screen.blit(self._bt_cancel.image, self._bt_cancel.position)
