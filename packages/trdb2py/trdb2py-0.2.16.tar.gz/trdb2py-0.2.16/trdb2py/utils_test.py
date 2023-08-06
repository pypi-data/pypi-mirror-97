# -*- coding:utf-8 -*-
import pytest
from trdb2py.utils import nextWeekDay


def test_nextWeekDay():
    d51 = nextWeekDay(5, 1)
    assert d51 == 1

    d42 = nextWeekDay(4, 2)
    assert d42 == 1

    d14 = nextWeekDay(1, 4)
    assert d14 == 5

    d24 = nextWeekDay(2, 4)
    assert d24 == 1

    d241 = nextWeekDay(2, 4, 0, 6)
    assert d241 == 6    

    d251 = nextWeekDay(2, 5, 0, 6)
    assert d251 == 0        
