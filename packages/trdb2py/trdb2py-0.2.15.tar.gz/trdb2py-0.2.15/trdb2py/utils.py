# -*- coding:utf-8 -*-
import trdb2py.trading2_pb2


def str2asset(asset: str) -> trdb2py.trading2_pb2.Asset:
    arr = asset.split('.', -1)
    if len(arr) != 2:
        raise ValueError

    return trdb2py.trading2_pb2.Asset(
        market=arr[0],
        code=arr[1],
    )


def nextWeekDay(cday: int, offday: int, startday: int = 1, endday: int = 5) -> int:
    """
    nextWeekDay - 计算周几向后偏移，譬如周1的2天后是周3，周5的2天后是周2
    """

    if cday < startday:
        cday = startday

    offday = offday % 7

    if cday + offday > endday:
        cday += offday + (6 - endday) + (startday - 0)
    else:
        cday += offday

    while cday > 6:
        cday -= 7

    return cday


def asset2str(asset: trdb2py.trading2_pb2.Asset) -> str:
    return asset.market + '.' + asset.code
