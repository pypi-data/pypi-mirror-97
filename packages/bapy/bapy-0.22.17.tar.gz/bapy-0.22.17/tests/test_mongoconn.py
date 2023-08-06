#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest

from bapy import MongoClientMotor
from bapy import MongoClientPy
from bapy import MongoColMotor
from bapy import MongoColPy
from bapy import MongoDBMotor
from bapy import MongoDBPy

from conftest import mongoconn


def test_mongoconn_sync():
    conn = mongoconn(project=False)
    assert not conn.password
    assert isinstance(conn.client(), (MongoClientPy, MongoDBPy))
    db = conn.db()
    assert isinstance(db, MongoDBPy)
    assert db.name == conn.name
    col = conn.col()
    assert isinstance(col, MongoColPy)
    assert col.name == conn.col_name
    if col.name in db.list_collection_names():
        col.drop()
    assert not conn.codec
    data = {db.name: col.name}
    col.insert_one(data)
    assert db.name in col.find_one(data)
    col.drop()


@pytest.mark.asyncio
async def test_mongoconn_async():
    conn = mongoconn()
    assert conn.password
    assert isinstance(conn.client(), (MongoClientMotor, MongoDBMotor))
    db = conn.db()
    assert isinstance(db, MongoDBMotor)
    assert db.name == conn.name
    col = conn.col()
    assert isinstance(col, MongoColMotor)
    assert col.name == conn.col_name
    if col.name in await db.list_collection_names():
        await col.drop()
    assert conn.codec
    data = {db.name: col.name}
    await col.insert_one(data)
    assert db.name in await col.find_one(data)
    await col.drop()
