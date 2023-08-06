# -*- coding:utf-8 -*-
import trdb2py.trading2_pb2
from datetime import datetime
import pandas as pd


def analysisResult(result: dict, dtFormat: str = '%Y-%m-%d') -> dict:
    if len(result['pnl'].values) > 0:
        startdt = datetime.fromtimestamp(
            result['pnl'].values[0].ts).strftime(dtFormat)

        enddt = datetime.fromtimestamp(
            result['pnl'].values[len(result['pnl'].values)-1].ts).strftime(dtFormat)

        valuesnums = len(result['pnl'].values)

        if len(result['pnl'].lstCtrl) > 0:
            buynums = 0
            sellnums = 0
            winnums = 0

            for v in result['pnl'].lstCtrl:
                if v.type == trdb2py.trading2_pb2.CtrlType.CTRL_SELL:
                    sellnums = sellnums + 1
                    if v.sellPrice > v.averageHoldingPrice:
                        winnums = winnums + 1
                if v.type == trdb2py.trading2_pb2.CtrlType.CTRL_BUY:
                    buynums = buynums + 1

            winrate = 0
            if sellnums > 0:
                winrate = winnums / sellnums

            return {'startTime': startdt, 'endTime': enddt, 'valuesNums': valuesnums,
                    'buyNums': buynums, 'sellNums': sellnums, 'winNums': winnums, 'winRate': winrate}

        return {'startTime': startdt, 'endTime': enddt, 'valuesNums': valuesnums}

    return None


def getIndicatorInResult(result: dict, indicatorName: str, dtFormat: str = '%Y-%m-%d', scale: float = 10000.0) -> pd.DataFrame:
    if len(result['pnl'].indicators) > 0:
        for v in result['pnl'].indicators:
            if v.fullname == indicatorName:
                fv0 = {
                    'val': [],
                    'date': [],
                }

                for cd in v.data:
                    fv0['val'].append(cd.vals[0] / scale)
                    fv0['date'].append(datetime.fromtimestamp(
                        cd.ts).strftime(dtFormat))

                return pd.DataFrame(fv0)

    return None


def getFirstCtrlTs(resultDest: dict):
    if len(resultDest['pnl'].lstCtrl) > 0:
        for v in resultDest['pnl'].lstCtrl:
            if v.type == trdb2py.trading2_pb2.CtrlType.CTRL_SELL or v.type == trdb2py.trading2_pb2.CtrlType.CTRL_BUY:
                return v.ts

    return resultDest['pnl'].values[0].ts


def buildPNLDataFrame(result: dict, isPerValue: bool = True, dtFormat: str = '%Y-%m-%d', startTs=0) -> pd.DataFrame:
    fv0 = {'date': [], 'value': []}

    if startTs > 0:
        startVal = 0
        for v in result['pnl'].values:
            if v.ts >= startTs:
                if isPerValue:
                    startVal = v.perValue
                else:
                    startVal = v.value - v.cost

                break

        for v in result['pnl'].values:
            if v.ts >= startTs:
                fv0['date'].append(datetime.fromtimestamp(
                    v.ts).strftime(dtFormat))

                if isPerValue:
                    fv0['value'].append(v.perValue / startVal)
                else:
                    fv0['value'].append(v.value - v.cost - startVal)

        return pd.DataFrame(fv0)

    for v in result['pnl'].values:
        fv0['date'].append(datetime.fromtimestamp(
            v.ts).strftime(dtFormat))

        if isPerValue:
            fv0['value'].append(v.perValue)
        else:
            fv0['value'].append(v.value - v.cost)

    return pd.DataFrame(fv0)
