import defs_sg


def handle_diff_increase():

    def add_bomb(increm=1):
        defs_sg.nb_bombs += increm
        # print('bombs: ', end='')
        # print(glvars.nb_bombs)

    def boost_speed(increm=1):
        defs_sg.simu_avatar_speed += increm
        # print('av speed: ', end='')
        # print(glvars.simu_avatar_speed)

    defs_sg.difficulty += 1
    # print('  (DEBUG - new DIFF. level is ' + str(glvars.difficulty) + ')')

    if defs_sg.difficulty == 2:
        boost_speed()  # S
    elif defs_sg.difficulty == 3:
        add_bomb()  # BB
    elif defs_sg.difficulty == 4:
        boost_speed()  # S
    elif defs_sg.difficulty == 5:
        add_bomb(2)  # B

    elif defs_sg.difficulty == 6:   # frow now on, speed will go 1+2+3 then rewards are boosted
        boost_speed()
    elif defs_sg.difficulty == 7:
        boost_speed(2)
    elif defs_sg.difficulty == 8:
        boost_speed(3)
        defs_sg.booster_flag = True
        defs_sg.nugget_reward = 175

    elif defs_sg.difficulty == 16:
        add_bomb()

    elif defs_sg.difficulty == 32:
        add_bomb()
