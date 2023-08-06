# -*- coding:utf-8 -*-

ArrPriceIndicator = ["ema", "sma", "smma", "wma", "ta-sma", "ta-ema",
                     "ta-wma", "ta-dema", "ta-tema", "ta-trima", "ta-kama", "ta-mama", "ta-t3"]


def isPriceIndicator(name: str) -> bool:
    arr = name.split('.')

    try:
        ArrPriceIndicator.index(arr[0])
        return True
    except Exception:
        return False


def isNeedSecondY(lst: list) -> bool:
    for v in lst:
        if not isPriceIndicator(v):
            return True

    return False
