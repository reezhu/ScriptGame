# -*- coding: utf-8 -*-
import os
import thread
import time
import traceback

import MathUtils
import OperationUtils

THREADHOLD = 0.92
switchCoolDown = 0
from random import randint


class Robot:
    def __init__(self, win, index):
        self.index = "{" + str(index) + "}"
        self.win = win
        self.folder = None
        self.RESOURCES = []
        self.battleCount = 0
        self.exit = None
        self.limit = None
        self.duplicateStage = 0
        self.duplicate = 20
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
        self.folder = self.modes[default]
        self.scanResources(self.folder)

    def scanResources(self, folder):
        self.exit = None
        self.RESOURCES = []
        print "已选择方案：", folder
        for f in os.listdir('./mode/' + folder):
            if "exit" in f:
                self.exit = f.split('.')[1]
            elif "limit" in f:
                self.limit = int(f.split('.')[1])
            elif "duplicate" in f:
                self.duplicate = int(f.split('.')[1])
            elif not f.endswith(".d"):
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
        self.duplicateStage = 0
        while True:
            imsrc = OperationUtils.getWindowCVimg(self.win)
            # OperationUtils.saveImage(imsrc, [])
            try:
                result, stage, detail = OperationUtils.locatStage(self.RESOURCES, hWnd=self.win, imsrc=imsrc, threshold=THREADHOLD)
            except:
                self.scanResources(self.folder)
                continue
            if result:
                print time.strftime("%H:%M:%S", time.localtime()), self.index, stage
                if lastStage is not stage:
                    lastStage = stage
                    self.duplicateStage = 0
                elif "ignore" not in stage:
                    self.duplicateStage += 1
                    if self.duplicateStage % 10 == 0:
                        print time.strftime("%H:%M:%S", time.localtime()), "重复点击", self.index, self.duplicateStage
                    if self.duplicateStage > self.duplicate:
                        self.duplicateStage = self.switchMode()
                # OperationUtils.draw_rec(OperationUtils.getWindowCVimg(self.win), [detail["rectangle"]], line_width=10, color=(255, 0, 0))
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
                if "[" in stage and "]" in stage:
                    name = stage.split("]")[0]
                    split = name.split("[")[1]
                    offsetx, offsety = split.split(",")
                    x, y = Position
                    Position = (x + int(offsetx), y + int(offsety))
                    # OperationUtils.draw_rec(OperationUtils.getWindowCVimg(self.win), [((x + int(offsetx), y + int(offsety)), (x, y), (x, y), (x, y))], line_width=5, color=(0, 255, 0))
                    # OperationUtils.draw_rec(OperationUtils.getWindowCVimg(self.win), [((x + 100, y), (x, y), (x, y), (x, y))], line_width=5, color=(0, 255, 0))
                    # OperationUtils.draw_rec(OperationUtils.getWindowCVimg(self.win), [((x, y + 250), (x, y), (x, y), (x, y))], line_width=5, color=(0, 255, 0))
                if "{" in stage and "}" in stage:
                    # 跳转功能
                    name = stage.split("}")[0]
                    split = name.split("{")[1]
                    index = str(stage.encode("utf8")).rfind("/")
                    OperationUtils.clickImage(self.win, str(stage.encode("utf8"))[0:index + 1] + split, threshold=THREADHOLD - 0.1)
                    # OperationUtils.draw_rec(OperationUtils.getWindowCVimg(self.win), [(Position, Position, Position, Position)], line_width=10, color=(255, 0, 0))
                    time.sleep(randint(1000, 2000) / 1000.0)
                    if "}}" in stage:
                        Position = None
                if Position is not None:
                    OperationUtils.clickPosition(self.win, Position)
                if "end" in stage:
                    self.battleCount += 1
                    print time.strftime("%H:%M:%S", time.localtime()), str(self.index) + "累计进行了" + str(self.battleCount) + "次战斗"
                    if self.limit is not None and self.battleCount >= self.limit:
                        self.duplicateStage = self.switchMode()

                    rate = 100
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
                    time.sleep(randint(2000, 3000) / 100.0)
                else:
                    time.sleep(randint(800, 1000) / 1000.0)
            else:
                # print(str(self.index) + "无匹配(战斗中)，等待……")
                if start:
                    time.sleep(randint(3, 5))
                    start = False
                else:
                    time.sleep(randint(500, 800) / 1000.0)


def startRobot(index):
    try:
        instance = Robot(win, index)
        instance.scanModes()
        thread.start_new_thread(instance.run, ())
        return thread
    except Exception:
        traceback.print_exc(file=open('error.log', 'a+'))


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
    threads = []
    for win in wins:
        threads.append(startRobot(index))

        index += 1

    if (True):
        time.sleep(3600 * 9)
