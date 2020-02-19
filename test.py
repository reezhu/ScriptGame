# -*- coding: utf-8 -*-
# @Author  : Ree
# @Email   : zhuweiyuan@corp.netease.com
# @Project : PokeMod
import numpy
import win32api
import win32con
import win32gui
import win32ui
import win32print


def getnum(maxRange=2, size=2):
    arr = numpy.random.randn(size)
    if arr.max() > maxRange or arr.min() < -maxRange:
        return getnum()
    else:
        return arr


# for i in range(100):
#     a,b=getnum()
#     a=1*(a+2)/4
#     b=1*(b+2)/4
#     print a,b
# hDC = win32gui.GetDC(0)
# print  win32api.EnumDisplayMonitors(None, None)
# print win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
# print win32print.GetDeviceCaps(hDC, win32con.HORZRES)
# print win32print.GetDeviceCaps(hDC, win32con.LOGPIXELSX)


# import requests
#
# cookie = [
#     {
#         "domain": ".opyw.163.gz",
#         "hostOnly": False,
#         "httpOnly": False,
#         "name": "Hm_lpvt_7d6465217b1b44018c4557d9e7d804eb",
#         "path": "/",
#         "sameSite": "unspecified",
#         "secure": False,
#         "session": True,
#         "storeId": "0",
#         "value": "1567651900",
#         "id": 1
#     },
#     {
#         "domain": ".opyw.163.gz",
#         "expirationDate": 1599187900,
#         "hostOnly": False,
#         "httpOnly": False,
#         "name": "Hm_lvt_7d6465217b1b44018c4557d9e7d804eb",
#         "path": "/",
#         "sameSite": "unspecified",
#         "secure": False,
#         "session": False,
#         "storeId": "0",
#         "value": "1567582467",
#         "id": 2
#     }
# ]
# response = requests.post("http://192.168.47.106:9001/study_5mins/v1/player", {"player_id": 42},
#                          cookies={".opyw.163.Hm_lpvt_7d6465217b1b44018c4557d9e7d804eb": "1567651900", ".opyw.Hm_lvt_7d6465217b1b44018c4557d9e7d804eb.gz": "1567582467"})
# print response


# for line in reversed(open("C:\Program Files\OpenVPN\log\savpn3.log").readlines()):
#     text =  line.rstrip()
#     if "CONNECTED,SUCCESS,10.62.0" in text:
#         elements = text.split(",")
#         print elements[3]
#         break

for i in 1:
    print i