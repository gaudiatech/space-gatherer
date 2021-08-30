import random
import defs_sg
import tuning as tuning
import katagames_sdk.engine as kataen


pygame = kataen.import_pygame()


class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.scr = kataen.get_screen()

        temp = pygame.image.load(defs_sg.ASSETS[4])
        self.image = pygame.transform.scale(temp, (128, 128))

        self.rect = self.image.get_rect()
        self.dx = None
        self.increm_yspeed = None
        self.reset()

    def reset(self):
        self.rect.bottom = 0
        self.rect.centerx = random.randint(0+33, -33+self.scr.get_width()-1)

        if random.random() > 0.5:
            self.dx = random.randint(-3, -1)
        else:
            self.dx = random.randint(1, 2)
        self.increm_yspeed = random.randint(1, 5)

    def update(self):
        self.rect.centerx += self.dx
        self.rect.centery += defs_sg.simu_avatar_speed + self.increm_yspeed

        if self.rect.top > self.scr.get_height():
            self.reset()


class Nugget(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(defs_sg.ASSETS[3])
        self.rect = self.image.get_rect()

        self.reset()
        defs_sg.nuggets_out -= 1  # first reset doesnt count

    def update(self):
        self.rect.centery += defs_sg.simu_avatar_speed
        if self.rect.top > kataen.get_screen().get_height():
            self.reset()

    def reset(self):
        self.rect.centery = 0
        self.rect.centerx = random.randrange(0, kataen.get_screen().get_width())

        defs_sg.nuggets_out += 1
        if defs_sg.nuggets_out == defs_sg.STEP_FOR_DIFF_INCREM:
            tuning.handle_diff_increase()
            defs_sg.nuggets_out = 0


class ScoreBoard(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.maxlives = 5
        self.lives = self.maxlives
        self.score = 0
        self.font = pygame.font.SysFont(None, 50)

        self.text = ""

    def update(self):
        self.text = "HP: {}/{}  |  Cash: {:,}$".format(self.lives, self.maxlives, self.score)

        self.image = self.font.render(self.text, True, (255, 255, 0))
        self.rect = self.image.get_rect()


class Explosion(pygame.sprite.Sprite):

    strip = None

    def __init__(self, pos_init):
        super().__init__()

        self.visible = True
        self.nb_frames = len(self.__class__.strip)
        self.image = self.strip[0]
        self.curr_frame = 0
        self.rect = self.image.get_rect()
        self.rect.center = pos_init
        self.slow_anim_cpt = 0

    @classmethod
    def preload_animation(cls):
        if cls.strip is None:
            # print(defs_sg.ASSETS[6])
            tmp_img = pygame.image.load(defs_sg.ASSETS[6])
            tmp_img.convert_alpha()
            cls.strip = list()

            def spr_loc(k):
                spr_per_line = 8
                i = k % spr_per_line
                j = k // spr_per_line
                return 82 * i, 80 * j, 82, 80

            supertemp = pygame.surface.Surface((82, 80))
            supertemp.convert()

            for p in range(4, 21):
                supertemp.blit(tmp_img, (0, 0), spr_loc(p))
                # tmp = pygame.transform.scale(supertemp, (int(3.22*82), 192))
                tmp = supertemp.copy()
                tmp.set_colorkey((0xff, 0, 0xff))
                cls.strip.append(tmp)

    def update(self):
        self.curr_frame = self.curr_frame + 1

        if self.curr_frame >= self.nb_frames:
            self.visible = False
        else:

            self.slow_anim_cpt += 1
            if not (self.slow_anim_cpt % 2):
                self.image = self.strip[self.curr_frame]

            self.rect.centery += defs_sg.simu_avatar_speed + random.randint(-8, 8)
            self.rect.centerx += random.randint(-30, 32)


class SpaceBg(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(defs_sg.ASSETS[0])
        self.image = self.image.convert()  # ?
        self.scr = kataen.get_screen()

        self.bsup_y = self.scr.get_height()-1

        # TODO modif img directement pr eviter manipulations in game
        target_w = self.scr.get_width()
        target_h = self.scr.get_height()*3
        self.image = pygame.transform.scale(self.image, (target_w, target_h))

        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.bottomleft = 0, self.bsup_y

    def update(self):
        self.rect.centery += defs_sg.simu_avatar_speed  # vertical scrolling

        if self.rect.top >= 0:
            self.reset()


class Spacecraft(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        # print(defs_sg.ASSETS[1])
        self.image = pygame.image.load(defs_sg.ASSETS[1])
        self.rect = self.image.get_rect()

        self.consty = kataen.get_screen().get_height()-95
        self.rect.center = (kataen.get_screen().get_width()//2, self.consty)  # init position
        self._low_speed = True

        if not pygame.mixer:
            print("problem with sounds!")
        else:
            pygame.mixer.init()

            self._snd_slow_engin = pygame.mixer.Sound(defs_sg.ASSETS[-1])
            self._snd_slow_engin.set_volume(0.44)
            
            self._snd_fast_engin = pygame.mixer.Sound(defs_sg.ASSETS[-4])
            self._snd_fast_engin.set_volume(1.22)

            self.snd_boom = pygame.mixer.Sound(defs_sg.ASSETS[-2])
            self.snd_boom.set_volume(0.55)

            self.snd_yay = pygame.mixer.Sound(defs_sg.ASSETS[-3])
            self.snd_yay.set_volume(0.8)

            self.engine_sound = self._snd_slow_engin

        self.trail_img = pygame.image.load(defs_sg.ASSETS[2])
        self.big_trail_img = pygame.image.load(defs_sg.ASSETS[5])

        self.trail_sz = self.trail_img.get_size()
        self._k = 1

        # queued delta_x
        self._q_deltax = 0

    def reset(self):
        self.consty = kataen.get_screen().get_height() - 95
        self.rect.center = (kataen.get_screen().get_width() // 2, self.consty)  # init position
        self._low_speed = True

    def draw_trail(self, surf):
        tx, ty = self.rect.bottomleft

        if self._k == 0:
            decalx, decaly = -1, -1
        elif self._k == 1:
            decalx, decaly = 1, -1
        elif self._k == 2:
            decalx, decaly = -1, 1
        else:
            decalx, decaly = 1, 1

        if defs_sg.booster_flag:
            surf.blit(self.big_trail_img, (decalx + tx, -11 + decaly + ty))
        else:
            surf.blit(self.trail_img, (decalx + tx, -11 + decaly + ty))

    def update(self):
        if defs_sg.booster_flag and self._low_speed:
            self._low_speed = False
            self._snd_slow_engin.stop()
            self.engine_sound = self._snd_fast_engin
            self.engine_sound.play(-1)

        posx, posy = pygame.mouse.get_pos()

        curr_var = abs(self.rect.centerx - posx)
        if self.rect.centerx < posx:
            effective_delta = min(defs_sg.STEERING_LIMIT, curr_var)
        else:
            effective_delta = -1 * min(defs_sg.STEERING_LIMIT, curr_var)

        self.rect.center = (self.rect.centerx + effective_delta, self.consty)

        # update the trail effect
        self._k = (self._k + 1) % 4
