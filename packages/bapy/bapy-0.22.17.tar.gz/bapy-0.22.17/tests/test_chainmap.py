# coding=utf-8
import asyncio
import inspect
from icecream import ic

from bapy import AsDict
from bapy import caller
from bapy import ChainMap
from bapy import ChainMapRV
from bapy import runwarning


def test_chainmap():
    maps = [dict(a=1, b=2), dict(a=2, c=3), dict(a=3, d=4), dict(a=dict(z=1)), dict(a=dict(z=1)), dict(a=dict(z=2))]
    chain = ChainMap(*maps)
    assert chain['a'] == [1, 2, 3, {'z': 1}, {'z': 2}]
    chain = ChainMap(*maps, rv=ChainMapRV.FIRST)
    assert chain['a'] == 1
    chain = ChainMap(*maps, rv=ChainMapRV.ALL)
    assert chain['a'] == [1, 2, 3, {'z': 1}, {'z': 1}, {'z': 2}]

