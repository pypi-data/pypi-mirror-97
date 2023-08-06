#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bapy import ic
from conftest import *


Path().cd(bapy.project)

def test_mongo():
    client = MongoTest(_id=ObjectId())
    data = {module: client.col.name}
    client.data = data
    doc = client.update_self
    assert doc['data'] == data
    with pytest.raises(InvalidDocument, match=rf".*set().*"):
        client.data = set()
        _ = client.update_self
    assert client.dump['data'][0] == data
    assert len(client.unique()) == client.count_documents({})
    assert list(client.dump_dict.keys()) == client.unique()
    assert '_id' not in client.dump_dict.values()
    client.drop()


# # noinspection DuplicatedCode
@pytest.mark.asyncio
async def test_mongo_aio():
    client = MongoTest()
    data = {module, client.col.name}
    client.data = data
    doc = await client.update_self_aio
    assert isinstance(doc['data'], set)
    assert doc['data'] == data
    assert (await client.dump_aio)['data'][0] == data
    assert len(await client.unique_aio()) == await client.count_documents({})
    assert list((await client.dump_dict_aio).keys()) == await client.unique_aio()
    assert '_id' not in (await client.dump_dict_aio).values()
    await client.drop()
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


