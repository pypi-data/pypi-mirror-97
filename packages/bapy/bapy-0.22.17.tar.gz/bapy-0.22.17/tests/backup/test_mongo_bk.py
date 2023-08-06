#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest

from bapy import cmd
from bapy import IPLoc
from bapy import IPv4
from bapy import mongocol
from bapy import MongoColMotor
from bapy import MongoColPy
from bapy import MongoConn
from bapy import mongodb
from bapy import MongoDBMotor
from bapy import MongoDBPy
from bapy import MongoOldIP
from bapy import Obj
from bapy.data.test_addr import google_addr
from bapy.data.test_addr import google_name

db_name = 'pytest'
col_name = 'test'
data = {db_name: col_name}

cmd('mongossh.sh')


def test_mongoip():
    one = MongoOldIP(_id=google_addr, _db='test', _connection=MongoConn.LOCAL)
    isinstance(one._id, IPv4)
    isinstance(one.loc, IPLoc)
    assert one.name == google_name
    assert one.col.name == MongoOldIP.__class__.__name__
    one.col.drop()
    assert one.find_self == dict()
    rv = one.update_self


@pytest.mark.asyncio
async def test_mongoip_aio():
    one = MongoOldIP(_id=google_addr, _db='test')
    isinstance(one._id, IPv4)
    isinstance(one.loc, IPLoc)
    assert one.name == google_name
    assert await one.col_aio.name == MongoOldIP.__class__.__name__
    await one.col.drop()
    assert await one.find_self_aio == dict()
    rv = await one.update_self_aio


