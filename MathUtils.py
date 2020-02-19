# -*- coding: utf-8 -*-
# @Author  : Ree
import numpy
from random import randint


def randomPosition(param,offset = 0):
    def getnum(maxRange=2, size=2):
        arr = numpy.random.randn(size)
        if arr.max() > maxRange or arr.min() < -maxRange:
            return getnum()
        else:
            return arr

    xm, ym = param[0]
    xn, yn = param[0]
    # print param
    for x, y in param:
        if x > xm:
            xm = x
        elif x < xn:
            xn = x
        if y > ym:
            ym = y
        if y < yn:
            yn = y
    ranx, rany = getnum()
    result = (int((xm - xn) * (ranx + 2) / 4 + xn), int((ym - yn) * (rany + 2) / 4 + yn) - offset)
    # print result
    return result


def rand(min=0, max=100):
    return randint(min * 1000, max * 1000) / 1000.0

def topLeft(elem):
    if elem is not None:
        x, y = elem[0]
        return x<<10 + y
    return -1