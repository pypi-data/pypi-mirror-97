# -*- coding:utf-8 -*-
import pytest
import trdb2py.trading2_pb2
from datetime import datetime
from trdb2py.timeutils import str2timestamp, getDayInYear, getYearDays


def test_getYearDays():
    assert getYearDays(2019) == 365
    assert getYearDays(2020) == 366
    assert getYearDays(2000) == 366
    assert getYearDays(1900) == 365

def test_getDayInYear():
    assert getDayInYear(2021, 1, 1) == 1
    assert getDayInYear(2021, 1, 31) == 31
    assert getDayInYear(2021, 2, 28) == 31 + 28
