# -*- coding: utf-8 -*-
# @Author  : Ree
# @Email   : zhuweiyuan@corp.netease.com
import ctypes
import os
import time

import aircv
import cv2
import numpy
import psutil
import win32api
import win32con
import win32gui
import win32ui

import MathUtils

LONG = ctypes.c_long
DWORD = ctypes.c_ulong
ULONG_PTR = ctypes.POINTER(DWORD)
WORD = ctypes.c_ushort



class MOUSEINPUT(ctypes.Structure):
    _fields_ = (('dx', LONG),
                ('dy', LONG),
                ('mouseData', DWORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (('wVk', WORD),
                ('wScan', WORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (('uMsg', DWORD),
                ('wParamL', WORD),
                ('wParamH', WORD))


class _INPUTunion(ctypes.Union):
    _fields_ = (('mi', MOUSEINPUT),
                ('ki', KEYBDINPUT),
                ('hi', HARDWAREINPUT))


class INPUT(ctypes.Structure):
    _fields_ = (('type', DWORD),
                ('union', _INPUTunion))


def MouseInput(flags, x, y, data):
    return MOUSEINPUT(x, y, data, flags, 0, None)


def KeybdInput(code, flags):
    return KEYBDINPUT(code, code, flags, 0, None)


def HardwareInput(message, parameter):
    return HARDWAREINPUT(message & 0xFFFFFFFF, parameter & 0xFFFF, parameter >> 16 & 0xFFFF)


INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARD = 2


def Input(structure):
    if isinstance(structure, MOUSEINPUT):
        return INPUT(INPUT_MOUSE, _INPUTunion(mi=structure))
    if isinstance(structure, KEYBDINPUT):
        return INPUT(INPUT_KEYBOARD, _INPUTunion(ki=structure))
    if isinstance(structure, HARDWAREINPUT):
        return INPUT(INPUT_HARDWARD, _INPUTunion(hi=structure))
    raise TypeError('Cannot create INPUT structure!')


def Mouse(flags, x=0, y=0, data=0):
    return Input(MouseInput(flags, x, y, data))


def Keyboard(code, flags=0):
    return Input(KeybdInput(code, flags))


def Hardware(message, parameter=0):
    return Input(HardwareInput(message, parameter))


def SendInput(*inputs):
    nInputs = len(inputs)
    LPINPUT = INPUT * nInputs
    pInputs = LPINPUT(*inputs)
    cbSize = ctypes.c_int(ctypes.sizeof(INPUT))
    return ctypes.windll.user32.SendInput(nInputs, pInputs, cbSize)


def setLowPriority():
    p = psutil.Process(os.getpid())
    print p.nice()
    p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)


def getWindowCVimg(win):
    # print win32gui.GetWindowRect(hWnd)
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(win)
    left, top, right, bot = win32gui.GetWindowRect(win)
    width = right - left
    height = bot - top
    # 创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟存储空间
    res = True
    while res:
        try:
            saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
            res = False
        except:
            time.sleep(1)
    # 将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)

    # 保存bitmap到内存设备描述表
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
    # 获取位图信息
    signedIntsArray = saveBitMap.GetBitmapBits(True)
    # 内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(win, hWndDC)

    im_opencv = numpy.frombuffer(signedIntsArray, dtype='uint8')
    im_opencv.shape = (height, width, 4)
    return im_opencv
    # cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2RGB)


def findImage(imsrc, item, threshold=0.9):
    return aircv.find_template(imsrc, item, threshold=threshold)


def clickPosition(hWnd, position, click=None):
    x_position, y_position = position
    # 将两个16位的值连接成一个32位的地址坐标
    long_position = win32api.MAKELONG(x_position, y_position)
    # win32api.SendMessage(hwnd, win32con.MOUSEEVENTF_LEFTDOWN, win32con.MOUSEEVENTF_LEFTUP, long_position)
    # if click is None:
    # 点击左键
    # win32api.SendMessage(hWnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
    # win32api.SendMessage(hWnd, win32con.WM_MOVE, win32con.MK_LBUTTON, long_position)
    # win32api.SendMessage(hWnd, win32con.WM_LBUTTONUP, 0, long_position)
    sendClick(hWnd, position, win32con.WM_LBUTTONDOWN)
    win32api.SendMessage(hWnd, win32con.WM_MOVE, win32con.MK_LBUTTON, long_position)
    win32api.SendMessage(hWnd, win32con.WM_MOVE, win32con.MK_LBUTTON, long_position + 1)
    sendClick(hWnd, position, win32con.WM_LBUTTONUP, button=0)
    # elif click:
    #     win32api.SendMessage(hWnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
    # elif click is False:
    #
    #     win32api.SendMessage(hWnd, win32con.WM_MOVE, win32con.MK_LBUTTON, long_position)
    #     win32api.SendMessage(hWnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)


def clickImage(win, path, threshold=0.9, imsrc=None):
    if imsrc is None:
        imsrc = getWindowCVimg(win)
    edit = getImage(path.encode("gbk"))
    result = aircv.find_template(imsrc, edit, threshold=threshold)
    if result:
        print "click", path
        position = MathUtils.randomPosition(result['rectangle'], offset=31)
        saveImage(imsrc, [(position, position, position, position)])
        clickPosition(win, position)
        # x, y = position
        # sendClick(win, position, win32con.WM_LBUTTONDOWN)
        # time.sleep(0.01)
        # sendClick(win, position, win32con.WM_LBUTTONUP, button=0)
        #
        # win32api.SetCursorPos((x, y))
        # Left click
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        # time.sleep(0.05)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        # SendInput(Mouse(win32con.MOUSEEVENTF_ABSOLUTE | win32con.MOUSEEVENTF_LEFTDOWN, x, y))
        # time.sleep(0.01)
        # SendInput(Mouse(win32con.MOUSEEVENTF_ABSOLUTE | win32con.MOUSEEVENTF_LEFTUP, x, y))


def hasImage(win, path, threshold=0.9, imsrc=None):
    if imsrc is None:
        imsrc = getWindowCVimg(win)
    if isinstance(path, str):
        edit = getImage(path)
    else:
        edit = path
    result = aircv.find_template(imsrc, edit, threshold=threshold)
    if result:
        return True
    return False


def swip(fromposition, positions, win):
    sendClick(win, fromposition, win32con.WM_LBUTTONDOWN)
    target = fromposition
    for position in positions:
        x1, y1 = fromposition
        x2, y2 = position
        for i in range(50):
            temp = (int((x2 - x1) * i / 50.0 + x1), int((y2 - y1) * i / 50.0 + y1))
            sendClick(win, temp, win32con.WM_MOUSEMOVE)
            time.sleep(0.001)
        sendClick(win, position, win32con.WM_MOUSEMOVE)
        target = position
        fromposition = position

    time.sleep(0.1)
    sendClick(win, target, win32con.WM_LBUTTONUP, button=0)


def sendClick(hWnd, position, id, button=win32con.MK_LBUTTON):
    x_position, y_position = position
    # 将两个16位的值连接成一个32位的地址坐标
    long_position = win32api.MAKELONG(x_position, y_position)
    win32api.PostMessage(hWnd, id, button, long_position)


def getAllWindows(labels):
    def callback(hwnd, hwnds):
        for label in labels:
            if label in win32gui.GetWindowText(hwnd):
                hwnds.append(hwnd)
                return True

    hwnds = []

    def getY(win):
        x1, y1, x2, y2 = win32gui.GetWindowRect(win)
        return y1

    win32gui.EnumWindows(callback, hwnds)

    hwnds.sort(key=getY)

    return hwnds


def findAllImage(path, imsrc, threshold=0.9):
    return aircv.find_all_template(imsrc, path, threshold=threshold)


def saveImage(imsrc, poses, color=(0, 255, 0), line_width=3):
    for pos1, pos2, pos3, pos4 in poses:
        # cv2.circle(img, pos, circle_radius, color, line_width)
        pos1 = (int(pos1[0]), int(pos1[1]))
        pos4 = (int(pos4[0]), int(pos4[1]))
        cv2.rectangle(imsrc, pos1, pos4, color, line_width)
    cv2.imwrite("snapshot.png", imsrc)


def draw_rec(img, poses, color=(0, 255, 0), line_width=3):
    for pos1, pos2, pos3, pos4 in poses:
        # cv2.circle(img, pos, circle_radius, color, line_width)
        pos1 = (int(pos1[0]), int(pos1[1]))
        pos4 = (int(pos4[0]), int(pos4[1]))
        cv2.rectangle(img, pos1, pos4, color, line_width)
    cv2.imshow('objDetect', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def getCount():
    first = True
    image = None
    i = 0
    while first or image is not None:
        image = cv2.imread("dream/item{0}house.png".format(i))
        i += 1
        first = False
    print i - 1, "matches"
    return i


def draw_rec(img, poses, color=(0, 255, 0), line_width=3):
    for pos1, pos2, pos3, pos4 in poses:
        # cv2.circle(img, pos, circle_radius, color, line_width)
        pos1 = (int(pos1[0]), int(pos1[1]))
        pos4 = (int(pos4[0]), int(pos4[1]))
        cv2.rectangle(img, pos1, pos4, color, line_width)
    cv2.imshow('objDetect', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def resizeWin(win, x, y):
    x1, y1, x2, y2 = win32gui.GetWindowRect(win)
    # print x1, y1, x2, y2
    win32gui.SetWindowPos(win, win32con.HWND_BOTTOM, x1, y1, x, y, win32con.SWP_NOZORDER)


cache = {}
useCache = False


def getImage(path):
    if not useCache:
        return cv2.imread(path)
    if path in cache:
        return cache[path]
    else:
        # print "cache", path
        image = cv2.imread(path)
        cache[path] = image
        return image


def locatStage(RESOURCES, hWnd=None, imsrc=None, threshold=0.9):
    if imsrc is not None:
        pass
    else:
        if hWnd:
            imsrc = getWindowCVimg(hWnd)
        else:
            raise RuntimeError("window id is None")
    # draw_rec(imsrc, [((0,0), (0,0), (0,0), (0,0))])
    for image in RESOURCES:

        result = aircv.find_template(imsrc, getImage(image.encode("gbk")), threshold=(0.98 if ("++" in image) else 0.8 if ("--" in image) else threshold))
        if result:
            # draw_rec(imsrc, [result['rectangle']])
            return True, image, result
    return False, None, None


def imread(path):
    return cv2.imread(path)


class WindowOperator:
    def __iadd__(self, win):
        self.win = win
        self.image = getWindowCVimg(win)
        self.time = 0

    def getWinImage(self):
        if self.image == None:
            self.image = getWindowCVimg(self.win)
        return self.image

    def wait(self, min=0, max=100):
        self.image = None
        time.sleep(MathUtils.rand(min, max))

    def waitShort(self, min=0, max=100):
        time.sleep(MathUtils.rand(min, max))

    def click(self, position):
        clickPosition(self.win, position)

    def clickImage(self, path, threshold=0.9):
        clickImage(self.win, path, imsrc=self.image, threshold=threshold)

    def swip(self, fromPostion, toPositons):
        swip(fromPostion, toPositons, self.win)
