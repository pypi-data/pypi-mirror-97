# -*- coding:utf-8 -*-
import pytest
from trdb2py.config import loadConfig


def test_loadConfig():
    cfg = loadConfig('./tests/config.yaml')

    assert cfg['servaddr'] == '127.0.0.1:5002'
    assert cfg['token'] == '123abc'
