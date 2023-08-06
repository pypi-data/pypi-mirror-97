# -*- coding:utf-8 -*-
import pytest
import trdb2py.trading2_pb2
from datetime import datetime
from trdb2py.timeutils import str2timestamp, getDayInYear, getYearDays
from trdb2py.pdutils import (buildPNLReport, getPNLLastTs, getPNLValueWithTimestamp, mergePNL, mergePNLEx,
                             rmPNLValuesWithTimestamp, getPNLTimestampLowInMonth, getPNLTimestampHighInMonth,
                             countTradingDays4Year, calcAnnualizedVolatility, rebuildPNL)


def test_countTradingDays4Year():
    pnl = trdb2py.trading2_pb2.PNLAssetData()
    arr = []

    ts = int(trdb2py.str2timestamp('2013-05-01', '%Y-%m-%d'))
    for i in range(0, 480):
        dt = datetime.utcfromtimestamp(ts)

        if dt.weekday() >= 0 and dt.weekday() < 5:
            pnl.values.append(trdb2py.trading2_pb2.PNLDataValue(ts=ts))

        ts += 60 * 60 * 24

    pnl.values.extend(arr)

    assert len(pnl.values) == 343
    assert countTradingDays4Year(pnl) == 261
