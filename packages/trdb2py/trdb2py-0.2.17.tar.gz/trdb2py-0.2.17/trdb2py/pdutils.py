# -*- coding:utf-8 -*-
import trdb2py.trading2_pb2
from trdb2py.utils import str2asset, asset2str
from datetime import datetime
import time
import pandas as pd
import numpy as np
import math
from trdb2py.timeutils import str2timestamp, getDayInYear, getYearDays, calcYears


def buildPNLReport(lstpnl: list) -> pd.DataFrame:
    """
    buildPNLReport - 将PNL列表转换为pandas.DataFrame，方便计算
    """
    fv0 = {
        'title': [],
        'asset': [],
        'maxDrawdown': [],
        'maxDrawdownStart': [],
        'maxDrawdownEnd': [],
        'maxDrawup': [],
        'maxDrawupStart': [],
        'maxDrawupEnd': [],
        'sharpe': [],
        'annualizedReturns': [],
        'annualizedVolatility': [],
        'totalReturns': [],
        'variance': [],
        'buyTimes': [],
        'sellTimes': [],
        'stoplossTimes': [],
        'maxUpDay': [],
        'maxPerUpDay': [],
        'maxDownDay': [],
        'maxPerDownDay': [],
        'maxUpWeek': [],
        'maxPerUpWeek': [],
        'maxDownWeek': [],
        'maxPerDownWeek': [],
        'maxUpMonth': [],
        'maxPerUpMonth': [],
        'maxDownMonth': [],
        'maxPerDownMonth': [],
        'maxUpYear': [],
        'maxPerUpYear': [],
        'maxDownYear': [],
        'maxPerDownYear': [],
        'perWinRate': [],
        'values': [],
    }

    for v in lstpnl:
        fv0['title'].append(v['title'])

        fv0['asset'].append(asset2str(v['pnl'].asset))

        fv0['maxDrawdown'].append(v['pnl'].maxDrawdown)
        fv0['maxDrawdownStart'].append(datetime.fromtimestamp(
            v['pnl'].maxDrawdownStartTs).strftime('%Y-%m-%d'))
        fv0['maxDrawdownEnd'].append(datetime.fromtimestamp(
            v['pnl'].maxDrawdownEndTs).strftime('%Y-%m-%d'))

        fv0['maxDrawup'].append(v['pnl'].maxDrawup)
        fv0['maxDrawupStart'].append(datetime.fromtimestamp(
            v['pnl'].maxDrawupStartTs).strftime('%Y-%m-%d'))
        fv0['maxDrawupEnd'].append(datetime.fromtimestamp(
            v['pnl'].maxDrawupEndTs).strftime('%Y-%m-%d'))

        fv0['sharpe'].append(v['pnl'].sharpe)
        fv0['annualizedReturns'].append(v['pnl'].annualizedReturns)
        fv0['annualizedVolatility'].append(v['pnl'].annualizedVolatility)
        fv0['totalReturns'].append(v['pnl'].totalReturns)
        fv0['variance'].append(v['pnl'].variance)

        fv0['buyTimes'].append(v['pnl'].buyTimes)
        fv0['sellTimes'].append(v['pnl'].sellTimes)
        fv0['stoplossTimes'].append(v['pnl'].stoplossTimes)

        fv0['maxUpDay'].append(datetime.fromtimestamp(
            v['pnl'].maxUpDayTs).strftime('%Y-%m-%d'))
        fv0['maxPerUpDay'].append(v['pnl'].maxPerUpDay)
        fv0['maxDownDay'].append(datetime.fromtimestamp(
            v['pnl'].maxDownDayTs).strftime('%Y-%m-%d'))
        fv0['maxPerDownDay'].append(v['pnl'].maxPerDownDay)

        fv0['maxUpWeek'].append(datetime.fromtimestamp(
            v['pnl'].maxUpWeekTs).strftime('%Y-%m-%d'))
        fv0['maxPerUpWeek'].append(v['pnl'].maxPerUpWeek)
        fv0['maxDownWeek'].append(datetime.fromtimestamp(
            v['pnl'].maxDownWeekTs).strftime('%Y-%m-%d'))
        fv0['maxPerDownWeek'].append(v['pnl'].maxPerDownWeek)

        fv0['maxUpMonth'].append(datetime.fromtimestamp(
            v['pnl'].maxUpMonthTs).strftime('%Y-%m-%d'))
        fv0['maxPerUpMonth'].append(v['pnl'].maxPerUpMonth)
        fv0['maxDownMonth'].append(datetime.fromtimestamp(
            v['pnl'].maxDownMonthTs).strftime('%Y-%m-%d'))
        fv0['maxPerDownMonth'].append(v['pnl'].maxPerDownMonth)

        fv0['maxUpYear'].append(datetime.fromtimestamp(
            v['pnl'].maxUpYearTs).strftime('%Y-%m-%d'))
        fv0['maxPerUpYear'].append(v['pnl'].maxPerUpYear)
        fv0['maxDownYear'].append(datetime.fromtimestamp(
            v['pnl'].maxDownYearTs).strftime('%Y-%m-%d'))
        fv0['maxPerDownYear'].append(v['pnl'].maxPerDownYear)

        fv0['values'].append(len(v['pnl'].values))

        if v['pnl'].sellTimes + v['pnl'].stoplossTimes == 0:
            fv0['perWinRate'].append(0)
        else:
            fv0['perWinRate'].append(
                v['pnl'].winTimes * 1.0 / (v['pnl'].sellTimes + v['pnl'].stoplossTimes))

    return pd.DataFrame(fv0)


def getPNLLastTs(pnl: trdb2py.trading2_pb2.PNLAssetData):
    ctrlnums = len(pnl.lstCtrl)

    if ctrlnums <= 0:
        return -1

    return pnl.lstCtrl[ctrlnums - 1].ts


def getPNLLastCtrl(pnl: trdb2py.trading2_pb2.PNLAssetData) -> trdb2py.trading2_pb2.CtrlNode:
    ctrlnums = len(pnl.lstCtrl)

    if ctrlnums <= 0:
        return None

    return pnl.lstCtrl[ctrlnums - 1]


def getPNLValueWithTimestamp(ts, pnl: trdb2py.trading2_pb2.PNLAssetData, isAdd: bool = True) -> int:
    if isAdd:
        for i in range(0, len(pnl.values)):
            if ts == pnl.values[i].ts:
                return i

            if ts < pnl.values[i].ts:
                pnl.values.insert(i, trdb2py.trading2_pb2.PNLDataValue(ts=ts))

                return i

        pnl.values.append(trdb2py.trading2_pb2.PNLDataValue(ts=ts))

        return len(pnl.values) - 1

    for i in range(0, len(pnl.values)):
        if ts == pnl.values[i].ts:
            return i

        i = i + 1

    return -1


def mergePNL(lstpnl: list) -> trdb2py.trading2_pb2.PNLAssetData:
    pnl = trdb2py.trading2_pb2.PNLAssetData()

    for vpnl in lstpnl:
        v = vpnl['pnl']

        for cai in range(0, len(v.values)):
            di = getPNLValueWithTimestamp(v.values[cai].ts, pnl)
            pnl.values[di].value += v.values[cai].value
            pnl.values[di].cost += v.values[cai].cost

            if pnl.values[di].cost > 0:
                pnl.values[di].perValue = pnl.values[di].value / \
                    pnl.values[di].cost
            else:
                pnl.values[di].perValue = 1

    return pnl


def mergePNLEx(pnldest: trdb2py.trading2_pb2.PNLAssetData, pnlsrc: trdb2py.trading2_pb2.PNLAssetData, inmoney):
    for cai in range(0, len(pnlsrc.values)):
        di = getPNLValueWithTimestamp(pnlsrc.values[cai].ts, pnldest)
        pnldest.values[di].value += (pnlsrc.values[cai].value - inmoney)

        if pnldest.values[di].cost > 0:
            pnldest.values[di].perValue = pnldest.values[di].value / \
                pnldest.values[di].cost
        else:
            pnldest.values[di].perValue = 1


def rmPNLValuesWithTimestamp(ts, pnl: trdb2py.trading2_pb2.PNLAssetData):
    i = getPNLValueWithTimestamp(ts, pnl)
    del pnl.values[i+1:]


def getPNLTimestampLowInMonth(pnl: trdb2py.trading2_pb2.PNLAssetData) -> list:
    ts = 0
    dt = None
    lastPerValue = 0
    arr = []

    for i in range(0, len(pnl.values)):
        v = pnl.values[i]

        if ts == 0:
            ts = v.ts
            dt = datetime.utcfromtimestamp(ts)
            lastPerValue = v.perValue
        else:
            cdt = datetime.utcfromtimestamp(v.ts)
            if dt.year == cdt.year and dt.month == cdt.month:
                if lastPerValue > v.perValue:
                    ts = v.ts
                    dt = cdt
                    lastPerValue = v.perValue

                if i == len(pnl.values) - 1:
                    arr.append(ts)
            else:
                arr.append(ts)

                ts = v.ts
                dt = cdt
                lastPerValue = v.perValue

    return arr


def getPNLTimestampHighInMonth(pnl: trdb2py.trading2_pb2.PNLAssetData) -> list:
    ts = 0
    dt = None
    lastPerValue = 0
    arr = []

    for i in range(0, len(pnl.values)):
        v = pnl.values[i]

        if ts == 0:
            ts = v.ts
            dt = datetime.utcfromtimestamp(ts)
            lastPerValue = v.perValue
        else:
            cdt = datetime.utcfromtimestamp(v.ts)
            if dt.year == cdt.year and dt.month == cdt.month:
                if lastPerValue < v.perValue:
                    ts = v.ts
                    dt = cdt
                    lastPerValue = v.perValue

                if i == len(pnl.values) - 1:
                    arr.append(ts)
            else:
                arr.append(ts)

                ts = v.ts
                dt = cdt
                lastPerValue = v.perValue

    return arr


def countTradingDays4Year(pnl: trdb2py.trading2_pb2.PNLAssetData):
    if len(pnl.values) > 0:
        fy = calcYears(pnl.values[0].ts, pnl.values[len(pnl.values) - 1].ts)

        return int(len(pnl.values) / fy)

    return 0


def calcAnnualizedVolatility(pnl: trdb2py.trading2_pb2.PNLAssetData):
    # https://www.zhihu.com/question/19770602
    # https://wiki.mbalib.com/wiki/%E5%8E%86%E5%8F%B2%E6%B3%A2%E5%8A%A8%E7%8E%87

    if len(pnl.values) > 0:
        arr = []
        for i in range(1, len(pnl.values)):
            arr.append(
                math.log(pnl.values[i].perValue / pnl.values[i-1].perValue))

        arrstd = np.std(arr)
        pnl.annualizedVolatility = arrstd * \
            math.sqrt(countTradingDays4Year(pnl))
    else:
        return 0


def rebuildPNL(pnl: trdb2py.trading2_pb2.PNLAssetData):
    if len(pnl.values) > 0:
        pnl.totalReturns = pnl.values[len(pnl.values) - 1].perValue

        calcAnnualizedVolatility(pnl)

        rebuildDrawdown(pnl)

        calcAnnualizedReturns(pnl)

        calcSharpe(pnl)
    else:
        pnl.totalReturns = 1.0
        pnl.annualizedVolatility = 0


def rebuildDrawdown(pnl: trdb2py.trading2_pb2.PNLAssetData):
    maxv = 0
    maxdd = 0
    startts = 0
    maxddsts = 0
    maxddets = 0

    for v in pnl.values:
        if v.perValue > maxv:
            maxv = v.perValue
            v.drawdown = 0
            startts = v.ts
        else:
            v.drawdown = (maxv - v.perValue) / maxv

            if v.drawdown > maxdd:
                maxdd = v.drawdown
                maxddsts = startts
                maxddets = v.ts

    pnl.maxDrawdown = maxdd
    pnl.maxDrawdownStartTs = maxddsts
    pnl.maxDrawdownEndTs = maxddets


def calcAnnualizedReturns(pnl: trdb2py.trading2_pb2.PNLAssetData):
    if len(pnl.values) > 0:
        fy = calcYears(pnl.values[0].ts, pnl.values[len(pnl.values) - 1].ts)
        if fy <= 1:
            pnl.annualizedReturns = pnl.values[len(
                pnl.values) - 1].perValue - 1
        else:
            pnl.annualizedReturns = (pnl.values[len(
                pnl.values) - 1].perValue - 1) / len(pnl.values) * countTradingDays4Year(pnl)


def calcSharpe(pnl: trdb2py.trading2_pb2.PNLAssetData):
    # https://www.zhihu.com/question/27264526

    pnl.sharpe = (pnl.annualizedReturns - 0.03) / pnl.annualizedVolatility


def clonePNLWithTs(pnl: trdb2py.trading2_pb2.PNLAssetData, startTs) -> trdb2py.trading2_pb2.PNLAssetData:
    npnl = trdb2py.trading2_pb2.PNLAssetData()
    firsti = -1
    firstpv = 1

    for cai in range(0, len(pnl.values)):
        if pnl.values[cai].ts >= startTs:
            if firsti < 0:
                firsti = cai
                firstpv = pnl.values[cai].perValue

            di = getPNLValueWithTimestamp(pnl.values[cai].ts, npnl)
            npnl.values[di].value += pnl.values[cai].value
            npnl.values[di].cost += pnl.values[cai].cost

            npnl.values[di].perValue = pnl.values[cai].perValue / firstpv

    return npnl


def genCtrlData(pnl: trdb2py.trading2_pb2.PNLAssetData, ctrlType, isPerValue: bool = True, dtFormat: str = '%Y-%m-%d', defVal=1) -> dict:
    fv1 = {'date': [], 'value': []}
    for v in pnl.lstCtrl:
        if v.type == ctrlType:
            fv1['date'].append(datetime.fromtimestamp(v.ts).strftime(dtFormat))

            vi = getPNLValueWithTimestamp(v.ts, pnl, isAdd=False)
            if vi >= 0:
                if isPerValue:
                    fv1['value'].append(pnl.values[vi].perValue)
                else:
                    fv1['value'].append(
                        pnl.values[vi].value - pnl.values[vi].cost)
            else:
                fv1['value'].append(defVal)

    return fv1
