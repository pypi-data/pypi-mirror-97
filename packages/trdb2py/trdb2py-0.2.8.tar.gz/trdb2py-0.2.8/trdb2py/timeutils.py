# -*- coding:utf-8 -*-
from datetime import datetime


def str2timestamp(strtime: str, strformat: str):
    dt = datetime.strptime(strtime, strformat)
    return dt.timestamp()


def getDayInYear(year, month, day):
    daymonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
        daymonth[1] = 29

    if month == 1:
        return day
    else:
        return sum(daymonth[:month-1])+day


def getYearDays(year):
    if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
        return 366

    return 365
