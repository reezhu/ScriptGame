# -*- coding: utf-8 -*-
import os
import thread
import time
import traceback

import MathUtils
import OperationUtils

RESOURCES = []
COOL = {}
BATTLE_COUNT = {}
THREADHOLD = 0.92
modes = []
exit = None
switchCoolDown = 0
from random import randint


def scanModes():
    print "扫描预设方案……"

    if not os.path.exists("./mode"):
        os.mkdir("./mode")
    for dir in os.listdir("./mode"):
        if os.path.isdir("./mode/" + dir):
            print len(modes), "-->", dir
            modes.append(dir)
    if len(modes) == 0:
        print "没有方案！请在mode目录下添加方案！"
    default = 0
    i = raw_input("选择一个方案：(默认0)\n")
    if i.isdigit() and int(i) < len(modes):
        default = int(i)
    folder = modes[default]
    scanResources(folder)


def scanResources(folder):
    global exit
    exit = None
    del RESOURCES[:]
    print "已选择方案：", folder
    for f in os.listdir('./mode/' + folder):
        if "exit" in f:
            exit = f.split('.')[1]
        elif ".d" not in f:
            RESOURCES.append(('./mode/' + folder + "/" + f).decode("gbk"))
    RESOURCES.sort()
    return RESOURCES,exit


def run(win, index):
    count = 0
    OperationUtils.resizeWin(win, 1152, 679)
    start = False
    lastStage = None
    duplicateStage = 0
    while True:
        imsrc = OperationUtils.getWindowCVimg(win)
        result, stage, detail = OperationUtils.locatStage(RESOURCES, hWnd=win, imsrc=imsrc, threshold=THREADHOLD)
        if result:
            print time.strftime("%H:%M:%S", time.localtime()), index, stage
            if lastStage is not stage:
                lastStage = stage
                duplicateStage = 0
            else:
                duplicateStage += 1
                if duplicateStage % 10 == 0:
                    print "重复点击", index, duplicateStage
                if duplicateStage > 20:
                    duplicateStage = switchMode(duplicateStage)

            Position = MathUtils.randomPosition(detail["rectangle"], offset=31)
            OperationUtils.clickPosition(win, Position)
            if "end" in stage:
                count += 1
                print(str(index) + "累计进行了" + str(count) + "次战斗")
                if count > 20:
                    duplicateStage = switchMode(duplicateStage)

                rate = 80
                while randint(0, 100) < rate:
                    rate /= 2
                    print(str(index) + "随机点击")
                    time.sleep(randint(100, 500) / 1000.0)
                    Position = MathUtils.randomPosition(detail["rectangle"], offset=31)
                    OperationUtils.clickPosition(win, Position)
            if "start" in stage:
                start = True
            else:
                start = False
            time.sleep(randint(400, 600) / 1000.0)
        else:
            # print(str(win) + "无匹配(战斗中)，等待……")
            if start:
                time.sleep(randint(5, 10))
                start = False
            else:
                time.sleep(randint(100, 300) / 1000.0)


def switchMode(duplicateStage):
    global switchCoolDown
    if (time.time() - switchCoolDown) < 20:
        return
    if exit is not None and exit in modes:
        scanResources(exit)
        duplicateStage = 0
        switchCoolDown = int(time.time())
    else:
        raise Exception("重复点击！")
        pass
    return duplicateStage


if __name__ == '__main__':
    open('file.txt', 'w').close()
    # try:
    label = '阴阳师-网易游戏'.decode("utf8").encode("gbk")
    wins = OperationUtils.getAllWindows([label])
    if len(wins) == 0:
        print('没有找到窗口')
        raise RuntimeError('window not found')
    for win in wins:
        BATTLE_COUNT[win] = 0
    scanModes()
    index = 0
    for win in wins:
        try:
            thread.start_new_thread(run, (win, index))
            index += 1
        except Exception:
            traceback.print_exc(file=open('error.log', 'a+'))
            raise Exception
    if (True):
        time.sleep(3600 * 9)
