class Setting(object):
    value_ban = 1

    value_num_0 = 5
    value_num_5 = 2

    value_death = -11
    value_damage = -2
    value_life = 10
    value_health = 2

    inf = 100
    max_depth = 1

    player_life_init = 1
    player_life_min = 0
    player_life_max = 2

    player_health_init = 3
    player_health_min = 0
    player_health_max = 10

    player_num_init = [1, 1]

    num_health_4 = 2
    num_health_7 = 1
    num_health_104 = 4
    num_health_107 = 2

    num_damage_7 = (3, 1)
    num_damage_8 = (1, 3)
    num_damage_9 = (1, 1)
    num_damage_100 = (2, 0)
    num_damage_101 = (1, 4)
    num_damage_108 = (1, player_health_max + 1)
    num_damage_107 = (3, 2)

    num_life_105 = 1

    num_ban_6 = 2
    num_ban_106 = 4

    input_first = "请输入您({0})要使用的数字编号:"
    input_second = "请输入您({0})要加的数字编号:"

    @classmethod
    def input(cls, n):
        if n == 2:
            return "请输入您({0})要复制(2)的数字编号:"
        elif n == 3:
            return "请输入您({0})要加(3)的数字编号:"
        elif n == 6:
            return "请输入您({0})要封禁(6)的数字编号:"
        elif n == 9:
            return "请输入您({0})要钩(9)的数字编号:"
