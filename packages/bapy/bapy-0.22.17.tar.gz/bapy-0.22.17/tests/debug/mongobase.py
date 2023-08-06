#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio

from bapy import ic
from bapy import MongoBase
from conftest import mongoconn


def test_mongobase_sync():
    mongoconn(project=False)
    client = MongoBase()
    client.drop()
    client.find_one_and_update({}, {'$set': {'b': 2}}, upsert=True)
    assert [i for i in client.find({})][0] == client.find_one({'b': 2})


async def test_mongobase_async():
    mongoconn()
    client = MongoBase()
    await client.drop()
    await client.find_one_and_update({}, {'$set': {'b': 2}}, upsert=True)
    assert (await client.find({}).to_list(True))[0] == await client.find_one({'b': 2})


test_mongobase_sync()
asyncio.run(test_mongobase_async(), debug=False)
