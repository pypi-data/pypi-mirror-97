# -*- coding:utf-8 -*-
import pytest
from trdb2py.indicator import isPriceIndicator


def test_isPriceIndicator():
    assert isPriceIndicator('ema.5') == True
    assert isPriceIndicator('rsi.5') == False
    assert isPriceIndicator("ta-ema.29>day/1d/5m/53700") == True
    assert isPriceIndicator("ta-ema") == True
    assert isPriceIndicator('rsi') == False
