# -*- coding: utf-8 -*-
import os
import thread
import time
import traceback

from psutil import Process

import MathUtils
import OperationUtils

THREADHOLD = 0.92
switchCoolDown = 0
from random import randint


class Robot:
    def __init__(self, win, index):
        self.index = index
        self.win = win
        self.RESOURCES = []
        self.battleCount = 0
        self.exit = None
        self.limit = None
        self.modes = []

    def scanModes(self):
        print "扫描预设方案……"

        if not os.path.exists("./mode"):
            os.mkdir("./mode")
        for dir in os.listdir("./mode"):
            if os.path.isdir("./mode/" + dir):
                print len(self.modes), "-->", dir
                self.modes.append(dir)
        if len(self.modes) == 0:
            print "没有方案！请在mode目录下添加方案！"
        default = 0
        i = raw_input("为{0}选择一个方案：(默认0)\n".format(index))
        if i.isdigit() and int(i) < len(self.modes):
            default = int(i)
        folder = self.modes[default]
        self.scanResources(folder)

    def scanResources(self, folder):
        self.exit = None
        self.RESOURCES = []
        print "已选择方案：", folder
        for f in os.listdir('./mode/' + folder):
            if "exit" in f:
                self.exit = f.split('.')[1]
            elif "limit" in f:
                self.limit = int(f.split('.')[1])
            elif ".d" not in f:
                self.RESOURCES.append(('./mode/' + folder + "/" + f).decode("gbk"))
        self.RESOURCES.sort()
        self.battleCount = 0
        return self.RESOURCES, self.exit

    def switchMode(self):
        if self.exit is not None and self.exit in self.modes:
            self.scanResources(self.exit)
            duplicateStage = 0
        else:
            raise Exception("重复点击！")
            pass
        return duplicateStage

    def run(self):

        OperationUtils.resizeWin(self.win, 1152, 679)
        start = False
        lastStage = None
        duplicateStage = 0
        while True:
            imsrc = OperationUtils.getWindowCVimg(self.win)
            result, stage, detail = OperationUtils.locatStage(self.RESOURCES, hWnd=self.win, imsrc=imsrc, threshold=THREADHOLD)
            if result:
                print time.strftime("%H:%M:%S", time.localtime()), self.index, stage
                if lastStage is not stage:
                    lastStage = stage
                    duplicateStage = 0
                else:
                    duplicateStage += 1
                    if duplicateStage % 10 == 0:
                        print time.strftime("%H:%M:%S", time.localtime()), "重复点击", self.index, duplicateStage
                    if duplicateStage > 20:
                        duplicateStage = self.switchMode()
                if "@" in stage:
                    name = stage.split(".")[1]
                    split = name.split("@")
                    next = split[1]
                    Position = MathUtils.randomPosition(detail["rectangle"], offset=31)
                    OperationUtils.clickPosition(self.win, Position)
                    self.scanResources(next.encode("utf8"))
                    time.sleep(randint(2000, 2500) / 1000.0)
                    continue
                Position = MathUtils.randomPosition(detail["rectangle"], offset=31)
                OperationUtils.clickPosition(self.win, Position)
                if "end" in stage:
                    self.battleCount += 1
                    print time.strftime("%H:%M:%S", time.localtime()), (str(self.index) + "累计进行了" + str(self.battleCount) + "次战斗")
                    if self.limit is not None and self.battleCount >= self.limit:
                        duplicateStage = self.switchMode()

                    rate = 80
                    while randint(0, 100) < rate:
                        rate /= 2
                        print time.strftime("%H:%M:%S", time.localtime()), (str(self.index) + "随机点击")
                        time.sleep(randint(100, 500) / 1000.0)
                        Position = MathUtils.randomPosition(detail["rectangle"], offset=31)
                        OperationUtils.clickPosition(self.win, Position)
                if "start" in stage:
                    start = True
                else:
                    start = False
                if "wait" in stage:
                    time.sleep(randint(5000, 10000) / 1000.0)
                else:
                    time.sleep(randint(800, 1000) / 1000.0)
            else:
                # print(str(win) + "无匹配(战斗中)，等待……")
                if start:
                    time.sleep(randint(3, 5))
                    start = False
                else:
                    time.sleep(randint(500, 800) / 1000.0)


if __name__ == '__main__':
    open('file.txt', 'w').close()
    # try:
    label = '阴阳师-网易游戏'.decode("utf8").encode("gbk")
    wins = OperationUtils.getAllWindows([label])
    if len(wins) == 0:
        print('没有找到窗口')
        raise RuntimeError('window not found')
    # scanModes()
    index = 0
    OperationUtils.setLowPriority()
    for win in wins:
        try:
            instance = Robot(win, index)
            instance.scanModes()
            thread.start_new_thread(instance.run, ())
            index += 1
        except Exception:
            traceback.print_exc(file=open('error.log', 'a+'))
            raise Exception
    if (True):
        time.sleep(3600 * 9)
