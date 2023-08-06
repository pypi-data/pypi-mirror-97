#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
from bson import ObjectId

from bapy import ChainMap
from bapy import MongoCol
from conftest import IPAddr
from conftest import MongoDoc


def test_mongocol_sync():
    client = MongoDoc.get(ObjectId(), project=False)
    client.data = ['dump_test']
    client.drop()
    col = MongoCol(_cls=MongoDoc)
    for c in [client, MongoDoc.get(ObjectId(), project=False)]:
        c.update_sync()
        assert col.unique_sync(instance=False) == col.unique_sync()  # _id == _id_obj
        assert col.unique_sync('data', instance=False) == col.unique_sync('data')  # data == data_obj
    col.set_sync()
    assert col.lst == col.lst_sorted
    assert col.chain == col.chain_sorted
    assert col.obj == col.obj_sorted
    for dump in col.obj:
        assert isinstance(dump, MongoDoc)
    dumps = [col.lst, col.lst_sorted, col.obj, col.obj_sorted]
    assert col.chain['data'][0] == client.data
    assert sum(map(len, dumps)) == 2 * len(dumps)
    assert col.dct == col.dct_sorted
    assert ChainMap(*col.dct.values())['data'] == col.chain['data']


# noinspection DuplicatedCode,PyArgumentList
@pytest.mark.asyncio
async def test_mongocol_async():
    client = MongoDoc.get(IPAddr().ping)
    client.data = ['dump_test_aio']
    await client.drop()
    col = MongoCol(_cls=MongoDoc)
    _id = list()
    for c in [MongoDoc.get(), client, MongoDoc.get(IPAddr().myip, type_=set)]:
        _id.append(c._id)
        await c.update_async()
        assert await col.unique_async(instance=False) == await col.unique_async()  # _id == _id_obj
    sort_id = sorted(_id)
    await col.set_async()

    index = 0
    for i in col.lst:
        assert i.get('_id') == _id[index]
        index += 1

    index = 0
    for i in col.lst_sorted:
        assert i.get('_id') == sort_id[index]
        index += 1

    index = 0
    for i in col.obj:
        assert i._id == _id[index]
        index += 1

    index = 0
    for i in col.obj_sorted:
        assert i._id == sort_id[index]
        index += 1

    assert col.chain_sorted['_id'] == sort_id
    assert col.chain != col.chain_sorted
    assert col.obj != col.obj_sorted
    for dump in col.obj:
        assert isinstance(dump, MongoDoc)

    dumps = [col.lst, col.lst_sorted, col.obj, col.obj_sorted]
    assert col.chain['data'][1] == client.data
    assert sum(map(len, dumps)) == 3 * len(dumps)
    assert col.dct == col.dct_sorted
    assert list(col.dct.keys()) == _id
    assert list(col.dct_sorted.keys()) == sort_id

    assert ChainMap(*col.dct.values())['data'] == col.chain['data']
