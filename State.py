import Setting


class State(object):
    def __init__(self, health=None, life=None,
                 num=None,
                 ban=None, action=(0,)):
        if health is None:
            self.health = [Setting.Setting.player_health_init, Setting.Setting.player_health_init]
        else:
            self.health = health[:]
        if life is None:
            self.life = [Setting.Setting.player_life_init, Setting.Setting.player_life_init]
        else:
            self.life = life[:]
        if num is None:
            self.num = [Setting.Setting.player_num_init[:], Setting.Setting.player_num_init[:]]
        else:
            self.num = num
        if ban is None:
            self.ban = [[0, 0], [0, 0]]
        else:
            self.ban = ban
        self.action = tuple(list(action))

    def is_Final(self):
        if min(self.life) <= Setting.Setting.player_life_min:
            return True
        else:
            return False

    def child(self):
        return State(self.health, self.life, [self.num[0][:], self.num[1][:]], [self.ban[0][:], self.ban[1][:]],
                     self.action)

    def add_Life(self, player, life_num):
        self.life[player] = min(self.life[player] + life_num, Setting.Setting.player_life_max)

    def add_Health(self, player, health_num):
        self.health[player] = min(self.health[player] + health_num, Setting.Setting.player_health_max)

    def add_Num(self, player, numid1, numid2):
        self.num[player][numid1] = (self.num[player][numid1] + self.num[player ^ 1][numid2]) % 10
        self.execute(player, numid1)

    def pre_Damage(self, player, damage):
        total_5 = self.num[player].count(5)
        total_0 = self.num[player].count(0)
        resistance = total_5 + total_0
        if damage[0] == 1:
            if resistance <= 0:
                self.on_Damage(player, damage[1])
            else:
                if total_0 >= 1:
                    self.num[player][self.num[player].index(0)] = 1
                else:
                    self.num[player][self.num[player].index(5)] = 1
        elif damage[0] == 3:
            self.on_Damage(player, damage[1])
        elif damage[0] == 2:
            if resistance >= 2:
                self.num[player] = [1, 1].copy()
            else:
                self.on_Death(player)

    def on_Damage(self, player, damage_num):
        self.health[player] = max(self.health[player] - damage_num, Setting.Setting.player_health_min)
        if self.health[player] <= Setting.Setting.player_health_min:
            self.on_Death(player)

    def on_Death(self, player):
        self.life[player] -= 1
        if self.life[player] > Setting.Setting.player_life_min:
            self.re_Birth(player)

    def re_Birth(self, player):
        self.health[player] = Setting.Setting.player_health_init
        self.num[player] = Setting.Setting.player_num_init
        self.ban[player] = [0, 0]

    def execute(self, player, numid):
        if self.num[player][numid] == 0:
            self.execute_10(player, numid ^ 1)
        elif self.num[player][numid ^ 1] == 0:
            self.execute_10(player, numid)
        else:
            self.execute_1(player, numid)

    def execute_1(self, player, numid):
        if self.num[player][numid] in (1, 5):
            self.action = (0,)
        elif self.num[player][numid] in (4, 8, 7):
            if self.num[player][numid] == 4:
                self.add_Health(player, Setting.Setting.num_health_4)
                self.action = (0,)
            elif self.num[player][numid] == 8:
                self.pre_Damage(player ^ 1, Setting.Setting.num_damage_8)
                self.action = (0,)
            elif self.num[player][numid] == 7:
                self.pre_Damage(player ^ 1, Setting.Setting.num_damage_7)
                self.add_Health(player, Setting.Setting.num_health_7)
                self.action = (0,)
        else:
            if self.can_Execute_n(player, numid):
                self.action += (self.num[player][numid],)
            else:
                self.action = (0,)

    def execute_10(self, player, numid):
        if self.num[player][numid] == 1:
            self.pre_Damage(player ^ 1, Setting.Setting.num_damage_101)
            self.action = (0,)
        elif self.num[player][numid] == 4:
            self.add_Health(player, Setting.Setting.num_health_104)
            self.action = (0,)
        elif self.num[player][numid] == 8:
            self.pre_Damage(player ^ 1, Setting.Setting.num_damage_108)
            self.action = (0,)
        elif self.num[player][numid] == 7:
            self.pre_Damage(player ^ 1, Setting.Setting.num_damage_107)
            self.add_Health(player, Setting.Setting.num_health_107)
            self.action = (0,)
        elif self.num[player][numid] == 5:
            self.add_Life(player, Setting.Setting.num_life_105)
            self.action = (0,)
        elif self.num[player][numid] == 0:
            self.pre_Damage(player ^ 1, Setting.Setting.num_damage_100)
            self.num[player] = [1, 1]
            self.action = (0,)
        else:
            self.action += (self.num[player][numid],)

    def can_add(self, player, numid1, numid2):
        if self.num[player ^ 1][numid2] == 0 or self.num[player][numid1] == 0 or self.ban[player][numid1] >= 1:
            return False
        return True

    def can_do(self, player):
        for i in range(2):
            for j in range(2):
                if self.can_add(player, i, j):
                    return True
        return False

    def can_Exec(self, player, numid1):
        for i in range(2):
            if self.can_Execute(player, numid1, i):
                return True
        return False

    def can_Execute(self, player, numid1, numid2):
        if self.num[player][numid1] == 0:
            numid1 ^= 1
        if self.num[player][numid1] == 2:
            func = self.can_Execute_2
        elif self.num[player][numid1] == 3:
            func = self.can_Execute_3
        elif self.num[player][numid1] == 6:
            return True
        elif self.num[player][numid1] == 9:
            func = self.can_Execute_9
        else:
            return True
        if func(player, numid1, numid2):
            return True

    def can_Execute_n(self, player, numid):
        for i in range(2):
            if self.can_Execute(player, numid, i):
                return True
        return False

    def execute_2(self, player, numid1, numid2):
        self.num[player][numid1] = self.num[player ^ 1][numid2]
        self.execute(player, numid1)

    def can_Execute_2(self, player, numid1, numid2):
        if self.num[player][numid1 ^ 1] != 0:
            return self.num[player ^ 1][numid2] not in (1, 2, 0)
        else:
            return self.num[player ^ 1][numid2] not in (2, 0)

    def execute_3(self, player, numid1, numid2):
        self.add_Num(player, numid1, numid2)

    def can_Execute_3(self, player, numid1, numid2):
        return self.num[player ^ 1][numid2] != 0

    def execute_6(self, player, numid1, numid2):
        if self.num[player][numid1 ^ 1] != 0:
            self.ban[player ^ 1][numid2] += Setting.Setting.num_ban_6
        else:
            self.ban[player ^ 1][numid2] += Setting.Setting.num_ban_106
        self.action = (0,)

    def execute_9(self, player, numid1, numid2):
        self.num[player][numid1], self.num[player ^ 1][numid2] = self.num[player ^ 1][numid2], 1
        if self.num[player][numid1 ^ 1] != 0:
            self.pre_Damage(player ^ 1, Setting.Setting.num_damage_9)
            self.action = (0,)
        else:
            self.execute_10(player, numid1)

    def can_Execute_9(self, player, numid1, numid2):
        if self.num[player][numid1 ^ 1] != 0:
            return self.num[player ^ 1][numid2] != 0
        else:
            return self.num[player ^ 1][numid2] not in (9, 0)

    def execute_n(self, player, numid1, numid2):
        if self.num[player][numid1] == 0:
            numid1 ^= 1
        if self.num[player][numid1] == 2:
            self.execute_2(player, numid1, numid2)
        elif self.num[player][numid1] == 3:
            self.execute_3(player, numid1, numid2)
        elif self.num[player][numid1] == 6:
            self.execute_6(player, numid1, numid2)
        elif self.num[player][numid1] == 9:
            self.execute_9(player, numid1, numid2)

    def de_Ban(self):
        for i in range(2):
            for j in range(2):
                if self.ban[i][j] >= 1:
                    self.ban[i][j] -= 1

    def show(self, row, player=-1):
        if player == 0:
            print(f"  A*  与零博弈   B 回合{row}")
        elif player == 1:
            print(f"  A   与零博弈   B*回合{row}")
        else:
            print(f"  A   与零博弈   B 回合{row}")
        beban = [['X' if i == 1 else ' ' for i in self.ban[n]] for n in (0, 1)]
        print(f"0   {self.num[0][0]}{beban[0][0]}\t      {self.num[1][0]}{beban[1][0]}  0")
        print(f"1   {self.num[0][1]}{beban[0][1]}\t      {self.num[1][1]}{beban[1][1]}  1")
        print(f"H   {self.health[0]}\t      {self.health[1]}   H")
        print(f"L   {self.life[0]}\t      {self.life[1]}   L")
        print()
