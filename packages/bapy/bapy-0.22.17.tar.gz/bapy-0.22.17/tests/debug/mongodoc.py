#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio

import pytest
from bson import InvalidDocument
from bson import ObjectId

from bapy import ChainMap
from bapy import ic
from conftest import IPAddr
from conftest import MongoDoc


# noinspection DuplicatedCode
def test_mongodoc_sync():
    client = MongoDoc.get(ObjectId(), project=False)
    client.data = ['dump_test']
    client.drop()
    for c in [client, MongoDoc.get(ObjectId(), project=False), MongoDoc.get(ObjectId(), project=False, type_=set)]:
        if isinstance(c.data, set):
            with pytest.raises(InvalidDocument, match=rf".*set().*"):
                c.update_sync()
        else:
            doc_obj = c.update_sync()
            doc_dict = c.update_sync(instance=False)
            find_obj = c.find_sync()
            find_dict = c.find_sync(instance=False)
            assert c.keys == c.asserts('keys')
            assert isinstance(doc_obj, MongoDoc) and isinstance(doc_dict, dict)
            assert isinstance(doc_obj._id, ObjectId) is isinstance(doc_dict['_id'], ObjectId)
            assert isinstance(find_obj, MongoDoc) and isinstance(find_dict, dict)
            assert isinstance(find_obj._id, ObjectId) is isinstance(find_dict['_id'], ObjectId)
            assert c.data == doc_obj.data == find_obj.data
            assert c.data == doc_dict['data'] == find_dict['data']
            assert c.update_sync(instance=False) == c.find_sync(instance=False)  # document dict.
            assert c.unique_sync(instance=False) == c.unique_sync()  # _id == _id_obj
            assert c.unique_sync('data', instance=False) == c.unique_sync('data')  # data == data_obj
    dump_find = [i for i in client.find()]
    dump_list_dict = client.dump_sync(instance=False, chain=False)
    dump_list_dict_sort = client.dump_sync(instance=False, sort=True, chain=False)
    dump_chain_dict = client.dump_sync(instance=False)
    dump_chain_dict_sort = client.dump_sync(instance=False, sort=True)
    dump_list_instance = client.dump_sync()
    dump_list_instance_sort = client.dump_sync(sort=True)
    assert dump_find == dump_list_dict_sort == dump_list_dict
    assert dump_chain_dict == dump_chain_dict_sort
    assert dump_list_instance == dump_list_instance_sort
    for dump in dump_list_instance:
        assert isinstance(dump, MongoDoc)
    dumps = [dump_find, dump_list_dict, dump_list_dict_sort, dump_list_instance, dump_list_instance_sort]
    assert dump_chain_dict['data'][0] == client.data
    assert sum(map(len, dumps)) == 2 * len(dumps)
    dump_dict = client.dict_sync()
    dump_dict_sort = client.dict_sync(sort=True)
    assert dump_dict == dump_dict_sort
    assert ChainMap(*dump_dict.values())['data'] == dump_chain_dict['data']


# noinspection DuplicatedCode,PyArgumentList
async def test_mongodoc_async():
    client = MongoDoc.get(IPAddr().ping)
    client.data = ['dump_test_aio']
    await client.drop()
    _id = list()
    for c in [MongoDoc.get(), client, MongoDoc.get(IPAddr().myip, type_=set)]:
        _id.append(c._id)
        doc_obj = await c.update_async()
        doc_dict = await c.update_async(instance=False)
        find_obj = await c.find_async()
        find_dict = await c.find_async(instance=False)
        assert client.keys == c.asserts('keys')
        assert isinstance(doc_obj, MongoDoc) and isinstance(doc_dict, dict)
        assert isinstance(doc_obj._id, str) is isinstance(doc_dict['_id'], str)
        assert isinstance(find_obj, MongoDoc) and isinstance(find_dict, dict)
        assert isinstance(find_obj._id, str) is isinstance(find_dict['_id'], str)
        assert c.data == doc_obj.data == find_obj.data
        assert c.data == doc_dict['data'] == find_dict['data']
        assert await c.update_async(instance=False) == await c.find_async(instance=False)  # document dict.
        assert await c.unique_async(instance=False) == await c.unique_async()  # _id == _id_obj
        assert await c.update_async(instance=False) == await c.find_async(instance=False)  # document dict.
    sort_id = sorted(_id)
    dump_find = await client.find().to_list(None)
    dump_list_dict = await client.dump_async(instance=False, chain=False)
    dump_list_dict_sort = await client.dump_async(instance=False, sort=True, chain=False)
    dump_chain_dict = await client.dump_async(instance=False)
    dump_chain_dict_sort = await client.dump_async(instance=False, sort=True)
    dump_list_instance = await client.dump_async()
    dump_list_instance_sort = await client.dump_async(sort=True)
    assert dump_find == dump_list_dict

    index = 0
    for i in dump_list_dict:
        assert i.get('_id') == _id[index]
        index += 1

    index = 0
    for i in dump_list_dict_sort:
        assert i.get('_id') == sort_id[index]
        index += 1

    index = 0
    for i in dump_list_instance:
        assert i._id == _id[index]
        index += 1

    index = 0
    for i in dump_list_instance_sort:
        assert i._id == sort_id[index]
        index += 1

    assert dump_chain_dict_sort['_id'] == sort_id
    assert dump_chain_dict != dump_chain_dict_sort
    assert dump_list_instance != dump_list_instance_sort
    for dump in dump_list_instance:
        assert isinstance(dump, MongoDoc)

    dumps = ic([dump_find, dump_list_dict, dump_list_dict_sort, dump_list_instance, dump_list_instance_sort])
    assert dump_chain_dict['data'][1] == client.data
    ic(sum((map(len, dumps))), 3 * len(dumps))
    assert sum(map(len, dumps)) == 3 * len(dumps)
    dump_dict = await client.dict_async()
    dump_dict_sort = await client.dict_async(sort=True)
    assert dump_dict == dump_dict_sort
    assert list(dump_dict.keys()) == _id
    assert list(dump_dict_sort.keys()) == sort_id

    assert ChainMap(*dump_dict.values())['data'] == dump_chain_dict['data']


test_mongodoc_sync()
asyncio.run(test_mongodoc_async(), debug=False)



#   assert client.keys == ['_id', 'data']
#   data = {module: client.col.name}
#   client.data = data
#     doc = client.update_self
#     assert doc['data'] == data
#     with pytest.raises(InvalidDocument, match=rf".*set().*"):
#         client.data = set()
#         _ = client.update_self
#     assert client.dump['data'][0] == data
#     assert len(client.unique()) == client.count_documents({})
#     assert list(client.dump_dict.keys()) == client.unique()
#     assert '_id' not in client.dump_dict.values()
#     client.drop()
#
#
# # noinspection DuplicatedCode
# @pytest.mark.asyncio
# async def test_mongo_aio():
#     # Path().cd(bapy.project)
#     # client = MongoTest()
#     # assert client.keys == ['_id', 'data']
#     # data = {module, client.col.name}
#     # client.data = data
#     doc = await client.update_self_aio
#     assert isinstance(doc['data'], set)
#     assert doc['data'] == data
#     assert (await client.dump_aio)['data'][0] == data
#     assert len(await client.unique_aio()) == await client.count_documents({})
#     assert list((await client.dump_dict_aio).keys()) == await client.unique_aio()
#     assert '_id' not in (await client.dump_dict_aio).values()
#     await client.drop()
#
#
# test_mongo()
# asyncio.run(test_mongo_aio(), debug=False)

# def test_mongoip():
#     Path().cd(bapy.tests)
#     ip = MongoIP().post_init()
#     assert ip.loc.country_name == 'Spain'
#     assert ip.col_name == MongoIP.__class__.__name__
#     ip.drop()
#     assert ip.find_self == dict()
#     isinstance(ip._id, IPv4)
#     isinstance(ip.loc, IPLoc)
#     with pytest.raises(InvalidDocument):
#         rv = ip.update_self
#
#     rv = ip.update_self_dict
#     assert isinstance(rv['loc'], dict)
#
#     await ip.drop()
#
#
# @pytest.mark.asyncio
# async def test_mongoip_aio():
#     Path().cd(bapy.project)
#     ip = await MongoIP(google_addr).post_init_aio()
#     assert ip.loc.country_name == google_country_name
#     assert ip.col_name == MongoIP.__class__.__name__
#     assert ip.name == google_name
#     await ip.drop()
#     assert ip.find_self == dict()
#     isinstance(ip._id, IPv4)
#     isinstance(ip.loc, IPLoc)
#
#     rv = await ip.update_self_aio
#     isinstance(rv['_id'], IPv4)
#     isinstance(rv['loc'], IPLoc)
#
#     assert rv['_id'].exploded == google_addr
#
#     assert isinstance(rv._id, IPv4)
#     assert isinstance(rv.loc, IPLoc)
#
#     await ip.drop()
#
#
#
# @pytest.mark.asyncio
# async def test_mongoip_sort_aio():
#     Path().cd(bapy.project)
#     sort = sorted([MongoIP()] + [MongoIP(addr=addr) for addr in [password_addr, google_addr, localhost]])
#     assert sort[0].text == google_addr
#     assert sort[1].text == password_addr
#     assert sort[2].text == IP().text
#     assert sort[3].text == localhost
#
# test_mongoip()
# asyncio.run(test_mongoip_aio(), debug=False)
# asyncio.run(test_mongoip_sort_aio(), debug=False)


