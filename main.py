import os
import random
import sys
import time

import Setting
from AI import AI
from State import State


def input_Error():
    print("输入错误！")
    os.system("pause")


def usage_Error():
    print("无效的操作！")
    os.system("pause")


def Error():
    print("错误！")
    sys.exit()


def cls():
    os.system("cls")


def Exit(st):
    cls()
    ans = input("请问您确定要退出吗？(y/N)")
    if ans not in ('y', 'Y'):
        return 0
    else:
        tm = time.time() - st
        cls()
        print(f"本次运行时长共{tm:.2f}秒，感谢您的使用！")
        os.system("pause")
        sys.exit()


def sInput(n, mode, player, cmd=None):
    if mode == 0 or (mode != 0 and player == 0):
        c = ['A', 'B'][player]
        if n == -1:
            in1 = input(Setting.Setting.input_first.format(c))
            if in1 == '-1':
                return -1, -1
            elif in1 not in ('0', '1'):
                return -2, -2
            in2 = input(Setting.Setting.input_second.format(c))
            if in2 == '-1':
                return -1, -1
            elif in2 not in ('0', '1'):
                return -2, -2
            return int(in1), int(in2)
        else:
            in1 = input(Setting.Setting.input(n).format(c))
            if in1 == '-1':
                return -1
            elif in1 not in ('0', '1'):
                return -2
            return int(in1)
    elif mode == 1:
        if n == -1:
            return random.randint(0, 1), random.randint(0, 1)
        return random.randint(0, 1)
    elif mode == 2:
        if n == -1:
            return cmd[0], cmd[1]
        return cmd[0]
    else:
        Error()


def Battle(mode):
    state = State()
    player = 0
    starttime = time.time()
    t = 1
    while not state.is_Final():
        state.action = (-1,)
        state_copy = state.child()
        c = None
        if mode == 2 and player != 0:
            ai = AI(state_copy)
            v, c = ai.search(player)
        t += 1
        m = 0
        while state.action[-1] != 0:
            cls()
            state.show(t // 2, player)
            if player != 0:
                os.system("pause")
                pass
            if not state.can_do(player):
                if mode == 0 or (mode != 0 and player == 0):
                    print(f"您({['A', 'B'][player]})当前无法操作！")
                    os.system("pause")
                state.action = (0,)
            elif state.action[-1] == -1:
                m, n = sInput(-1, mode, player, c)
                if c is tuple:
                    c = c[2:]
                op = min(m, n)
                if op == -2:
                    input_Error()
                    continue
                elif op == -1:
                    continue
                elif not state.can_add(player, m, n):
                    if mode == 0 or (mode != 0 and player == 0):
                        usage_Error()
                else:
                    state.add_Num(player, m, n)
            else:
                if not state.can_Exec(player, m):
                    state.action = (0,)
                    continue
                n = sInput(state.action[-1], mode, player, c)
                if mode == 2:
                    if c is tuple:
                        c = c[1:]
                if n == -1:
                    state = state_copy
                    continue
                elif n == -2:
                    input_Error()
                    continue
                else:
                    if state.can_Execute(player, m, n):
                        state.execute_n(player, m, n)
                    else:
                        if mode == 0 or (mode != 0 and player == 0):
                            usage_Error()
                        continue
            if state.action[-1] == 0:
                player ^= 1
                state.de_Ban()
    cls()
    state.show(t // 2)
    totaltime = time.time() - starttime
    print(f"{['A', 'B'][player ^ 1]} 取得胜利！")
    print(f"总计 {t // 2} 回合,共用时 {totaltime:.2f} 秒")
    os.system("pause")


def main_Menu(st):
    choose = '-1'
    quit = 0
    mode = 0
    while not quit:
        cls()
        print("\t与零博弈")
        print("\t\tBy KuDikan")
        print("1. 开始游戏")
        print("2. 切换模式")
        print("0. 退出游戏")
        choose = input("请选择：")
        if len(choose) != 1 or choose[0] not in ('1', '2', '0'):
            input_Error()
        else:
            if choose[0] == '1':
                Battle(mode)
            elif choose[0] == '2':
                mode = [0, 1, 2][(mode + 1) % 3]
                print(f"当前模式为 {['PVP', 'PVE', 'PVAI'][mode]}")
                os.system("pause")
            else:
                quit = Exit(st)


def init():
    cls()
    os.system("color 0A")
    os.system("title 与零博弈 V1.0a")


if __name__ == '__main__':
    sys.setrecursionlimit(6000)
    st = time.time()
    init()
    main_Menu(st)
