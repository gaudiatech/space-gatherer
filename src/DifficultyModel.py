

class DifficultyModel:
    STEP_FOR_DIFF_INCREM = 3

    def __init__(self):
        self.booster_flag = None
        self.diff_level = None
        self.nb_bombs = None
        self.nuggets_out = None
        self.nugget_reward = None
        self.simu_avatar_speed = None
        self.reset()

    def reset(self):
        self.booster_flag = False
        self.diff_level = 1
        self.nb_bombs = 2
        self.nuggets_out = 0
        self.nugget_reward = 100
        self.simu_avatar_speed = 2

    def add_bomb(self, increm=1):
        self.nb_bombs += increm

    def boost_speed(self, increm=1):
        self.simu_avatar_speed += increm

    def handle_diff_increase(self):
        self.diff_level += 1
        # print('  (DEBUG - new DIFF. level is ' + str(glvars.difficulty) + ')')

        if self.diff_level == 2:
            self.boost_speed()  # S
        elif self.diff_level == 3:
            self.add_bomb()  # BB
        elif self.diff_level == 4:
            self.boost_speed()  # S
        elif self.diff_level == 5:
            self.add_bomb(2)  # B

        elif self.diff_level == 6:   # frow now on, speed will go 1+2+3 then rewards are boosted
            self.boost_speed()
        elif self.diff_level == 7:
            self.boost_speed(2)
        elif self.diff_level == 8:
            self.boost_speed(3)
            self.booster_flag = True
            self.nugget_reward = 175

        elif self.diff_level == 16:
            self.add_bomb()

        elif self.diff_level == 32:
            self.add_bomb()
