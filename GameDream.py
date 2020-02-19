# coding=utf8
# @Author  : Ree
import thread
import time
import traceback
import OperationUtils as op
import MathUtils as math
from random import randint

autoDrag = False
rectangles = [((187, 525), (187, 544L), (208L, 525), (208L, 544L)),
              ((356, 446), (356, 465L), (377L, 446), (377L, 465L)),
              ((525, 351), (525, 370L), (546L, 351), (546L, 370L)),
              ((187, 693), (187, 712L), (208L, 693), (208L, 712L)),
              ((355, 606), (355, 625L), (376L, 606), (376L, 625L)),
              ((525, 522), (525, 541L), (546L, 522), (546L, 541L)),
              ((188, 861), (188, 880L), (209L, 861), (209L, 880L)),
              ((356, 775), (356, 794L), (377L, 775), (377L, 794L)),
              ((525, 690), (525, 709L), (546L, 690), (546L, 709L))]
gold = []
other = []


def findNearest(rectangles, param):
    max = -1
    total = 9999999999
    a, b = (param[0][0] + param[3][0]) / 2, param[1][1]
    for i in range(9):
        x, y = rectangles[i][3]

        t = (a - x) * (a - x) + (b - y) * (b - y)
        if t < total:
            total = t
            max = i
    if max >= 9999999999:
        return None
    else:
        # print "nearest", max
        return rectangles[max]


def scanImage(path):
    import os
    list = []
    for f in os.listdir('./dream/' + path + "/"):
        if ".d" not in f and "house" not in f:
            list.append(('./dream/' + path + "/" + f).decode("gbk"))
    list.sort()
    return list


def getOperationMode(win, imsrc):
    # return 0
    for i in range(6):
        if op.hasImage(win, "dream/mode" + str(i) + ".png", threshold=0.7):
            # op.saveImage(imsrc, [])
            return i
    return -1


def mode0(win, imsrc):
    global autoDrag
    op.clickImage(win, "dream/mode0.png", imsrc=imsrc)
    time.sleep(randint(1000, 2000) / 1000.0)
    autoDrag = False
    print "train finished, fallback to normal"
    op.clickImage(win, "dream/mode0-1.png")
    time.sleep(randint(1000, 2000) / 1000.0)
    op.clickImage(win, "dream/edit.png")
    time.sleep(randint(1500, 2000) / 1000.0)

    for i in range(6):
        print "click a"
        op.clickImage(win, "dream/fallback/a{0}.png".format(str(i)))
        time.sleep(randint(1500, 2000) / 1000.0)
        print "click change"
        op.clickImage(win, "dream/fallback/change.png")
        time.sleep(randint(1500, 2000) / 1000.0)
        print "click b"
        op.clickImage(win, "dream/fallback/b{0}.png".format(str(i)))
        time.sleep(randint(1500, 2000) / 1000.0)
        print "random"
        op.clickImage(win, "dream/fallback/random.png")
        time.sleep(2)
    op.clickImage(win, "dream/edit2.png")




def mode1(win, imsrc):
    op.clickImage(win, "dream/mode1.png", imsrc=imsrc)


def mode2(win, imsrc):
    op.clickImage(win, "dream/mode2.png", imsrc=imsrc)
    time.sleep(randint(500, 1000) / 1000.0)
    op.clickImage(win, "dream/mode2-1.png")


def modeSupply(count, win, imsrc):
    global gold, other
    if not op.hasImage(win, "dream/train.png"):
        return 0, 0
    print "detected a train"
    gItem = 0
    for file in gold:
        hfile = file.replace(".png", "house.png")
        item = op.imread(file)
        house = op.imread(hfile)
        if house is None:
            print hfile, "not found!"
            continue
        result = op.findImage(imsrc, item)
        if result:
            print "found item", file
            position = math.randomPosition(result['rectangle'])
            imsrc = op.getWindowCVimg(win)
            result2 = op.findImage(imsrc, house, threshold=0.7)

            if result2:
                print "found target for item", file
                gItem += 1
                # op.saveImage(imsrc, [result['rectangle']])
                fromposition = position
                for _ in range(randint(2, 4)):
                    position = math.randomPosition(findNearest(rectangles, result2['rectangle']))
                    op.swip(fromposition, [position], win)
                time.sleep(randint(500, 1000) / 1000.0)

            else:
                print "ERROR!!!!: no target found for item", file
                break

            imsrc = op.getWindowCVimg(win)
    oItem = 0
    for file in other:
        item = op.imread(file)
        result = op.findImage(imsrc, item)
        if result:
            print "found item", file
            oItem += 1
            position = math.randomPosition(result['rectangle'])
            x, y = position
            op.swip(position, [(x, y - 100,)], win)
    time.sleep(randint(500, 1000) / 1000.0)
    imsrc = op.getWindowCVimg(win)
    if op.hasImage(win, "dream/train.png") and oItem > 0:
        print "refresh the train"

        op.clickImage(win, "dream/close.png")
        time.sleep(randint(1000, 2000) / 1000.0)
        op.clickImage(win, "dream/mode5.png")
    return gItem, oItem


def modeCollection(count, win, imsrc):
    # 收菜
    print "collecting...."
    positions = [math.randomPosition(rec) for rec in rectangles]
    op.swip(positions[0], positions[1:], win)
    # for rec in rectangles:
    #     position = randomPosition(rec)
    #     sendClick(win, position, win32con.WM_LBUTTONDOWN)
    #     sendClick(win, position, win32con.WM_LBUTTONUP, button=0)
    # time.sleep(randint(100, 500) / 1000.0)


def modeOpen(win, imsrc):
    op.clickImage(win, "dream/mode5.png")


def modeLuckPocket(win, imsrc):
    hb = {}
    for ii in range(6):
        hb[ii] = op.imread("dream/hb{0}.png".format(str(ii)))
    hasNext = 3
    while hasNext:
        hasNext -= 1
        for key, value in hb.items():
            if op.hasImage(win, value, imsrc=imsrc):
                # if ac.find_template(imsrc, value, threshold=0.9):
                hasNext = 3
                op.clickImage(win, "dream/hb{0}.png".format(str(key)), imsrc=imsrc)
                print "opened a red pack", key
                break

        if hasNext > 0:
            time.sleep(randint(500, 1000) / 1000.0)
            imsrc = op.getWindowCVimg(win)


def run(win, index, count):
    global gold, other
    # x1, y1, x2, y2 = win32gui.GetWindowRect(win)
    # print x1, y1, x2, y2
    # win32gui.SetWindowPos(win, win32con.HWND_BOTTOM, x1, y1, 1152, 679, win32con.SWP_NOZORDER)
    gold = scanImage("gold")
    other = scanImage("other")
    while True:
        imsrc = op.getWindowCVimg(win)
        mode = getOperationMode(win, imsrc)
        print "detected mode", mode
        t = 1
        if mode == 0:
            mode0(win, imsrc)
            t = randint(1, 3)
        if mode == 1:
            mode1(win, imsrc)
            t = randint(1, 3)
        if mode == 2:
            mode2(win, imsrc)
            t = randint(1, 3)
        elif mode == 3:
            if len(rectangles) != 9:
                modeLocating(win)
            elif autoDrag and op.hasImage(win, "dream/train.png", imsrc=imsrc):
                g, o = modeSupply(count, win, imsrc)
            elif not autoDrag and randint(0, 100) < 20:
                modeUpgrade(win, imsrc)
            else:
                modeCollection(count, win, imsrc)
            if autoDrag:
                t = (randint(3, 5))
            else:
                t = randint(200, 600)
        elif mode == 4:
            modeLuckPocket(win, imsrc)
            t = randint(3, 4)
        elif mode == 5:
            modeOpen(win, imsrc)
            t = randint(3, 4)
        print "waiting for next round", t
        time.sleep(t)


def modeUpgrade(win, imsrc):
    # 升级
    print "upgradeing...."
    op.clickImage(win, "dream/edit.png", imsrc=imsrc)
    time.sleep(randint(500, 1000) / 1000.0)
    op.clickImage(win, "dream/upgrade{0}.png".format(randint(0, 4)), threshold=0.8)
    time.sleep(randint(1000, 1500) / 1000.0)
    imsrc = op.getWindowCVimg(win)
    for _ in range(2):
        op.clickImage(win, "dream/upgrade.png", imsrc=imsrc)
        time.sleep(randint(200, 500) / 1000.0)

    op.clickImage(win, "dream/edit2.png", threshold=0.8, imsrc=imsrc)
    time.sleep(randint(500, 1000) / 1000.0)


def modeLocating(win):
    global rectangles
    # rectangles = []
    while len(rectangles) != 9:
        while len(rectangles) != 9:
            time.sleep(1)
            imsrc = op.getWindowCVimg(win)
            coin = op.imread("dream/coin.png")
            result = op.findAllImage(coin, imsrc, threshold=0.6)
            rectangles = [res['rectangle'] for res in result]
            # draw_rec(imsrc, rectangles)
        rectangles.sort(key=math.topLeft)
        print "finish locating coins"


if __name__ == '__main__':
    open('file.txt', 'w').close()
    # try:
    label = ['家国梦'.decode("utf8").encode("gbk"), 'MuMu模拟器'.decode("utf8").encode("gbk")]
    wins = op.getAllWindows(label)
    count = op.getCount() - 1
    if len(wins) == 0:
        print('没有找到窗口')
        raise RuntimeError('window not found')
    index = 0
    i = raw_input("是否启用自动收货？(y/n)：(默认n)\n")
    if "t" in i or "y" in i:
        autoDrag = True
    # rectangles = []
    for win in wins:
        try:
            thread.start_new_thread(run, (win, index, count))
            index += 1
        except Exception:
            traceback.print_exc(file=open('error.log', 'a+'))
            raise Exception
    while (True):
        time.sleep(10000)
