import Setting
import State


class AI(State.State):
    def __init__(self, state):
        super().__init__(state.health, state.life, [state.num[0][:], state.num[1][:]],
                         [state.ban[0][:], state.ban[1][:]],
                         state.action)
        self.maximizingplayer = 0
        self.depth = 0
        self.value = 0
        self.cmd = []

    def search(self, player):
        self.maximizingplayer = player
        return self.alphabeta(-Setting.Setting.inf, Setting.Setting.inf, player)

    def alphabeta(self, alpha, beta, player):
        if self.is_Final():
            return self.value, self.cmd
        children = []
        cmd = []

        self.expand_add(children, player)

        for child in children:
            value, c = child.alphabeta(alpha, beta, player ^ 1)
            if player == self.maximizingplayer:
                if value > alpha:
                    alpha = value
                    cmd = c[:]
            else:
                if value < beta:
                    beta = value
                    cmd = c[:]
            if alpha >= beta:
                break
        return alpha if player == self.maximizingplayer else beta, cmd[:]

    def is_Final(self):
        self.depth += 1
        self.de_Ban()
        return self.depth > Setting.Setting.max_depth or super().is_Final()

    def child(self):
        ai = AI(self)
        ai.value = self.value
        ai.cmd = self.cmd[:]
        ai.depth = self.depth
        ai.maximizingplayer = self.maximizingplayer
        return ai

    def add_Value(self, value, player):
        self.value += value if player == self.maximizingplayer else -value

    def expand_add(self, children, player):
        for i in range(2):
            for j in range(2):
                if self.can_add(player, i, j):
                    ai = self.child()
                    ai.add_Num(player, i, j)
                    if self.depth == 1:
                        ai.cmd += (i, j)
                    ai.expand_exec(player, children, i)

                if self.num[player ^ 1][j] == self.num[player ^ 1][j ^ 1]:
                    break
            if self.num[player][i] == self.num[player][i ^ 1]:
                break

    def expand_exec(self, player, children, n):
        if self.action[-1] == 0 or not self.can_Exec(player, n):
            nvalue = self.num[player].count(5) * Setting.Setting.value_num_5 + self.num[player].count(
                0) * Setting.Setting.value_num_0 - sum(self.ban[player]) * Setting.Setting.value_ban
            self.add_Value(nvalue, player)
            children.append(self)
        else:
            for i in range(2):
                if self.can_Execute_n(player, n):
                    ai = self.child()
                    ai.execute_n(player, n, i)
                    if self.depth == 0:
                        ai.cmd += (i,)
                    ai.expand_exec(player, children, n)

                    if self.num[player ^ 1][i] == self.num[player ^ 1][i ^ 1]:
                        break

    def add_Health(self, player, health_num):
        super().add_Health(player, health_num)
        self.add_Value(Setting.Setting.value_health * health_num, player)

    def add_Life(self, player, life_num):
        super().add_Life(player, life_num)
        self.add_Value(Setting.Setting.value_life * life_num, player)

    def on_Damage(self, player, damage_num):
        super().on_Damage(player, damage_num)
        self.add_Value(Setting.Setting.value_damage * damage_num, player)

    def on_Death(self, player):
        super().on_Death(player)
        self.add_Value(Setting.Setting.value_death, player)

    def de_Ban(self):
        for i in range(2):
            for j in range(2):
                if self.ban[i][j] >= 1:
                    self.ban[i][j] -= 1
                    self.add_Value(Setting.Setting.value_ban, i)
