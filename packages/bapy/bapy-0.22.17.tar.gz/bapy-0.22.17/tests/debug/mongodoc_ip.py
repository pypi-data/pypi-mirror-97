#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio

from bapy import IP
from conftest import IPAddr
from conftest import ips
from conftest import MongoIPDoc


# noinspection DuplicatedCode,PyArgumentList
def test_mongodoc_ip_sync():
    c = MongoIPDoc.get(ips()['ping'])
    c.drop()
    doc_obj = c.update_sync()
    doc_dict = c.update_sync(instance=False)
    find_obj = c.find_sync()
    find_dict = c.find_sync(instance=False)
    assert isinstance(doc_obj, MongoIPDoc) and isinstance(doc_dict, dict)
    assert isinstance(doc_obj._id, str) is isinstance(doc_dict['_id'], str)
    assert isinstance(find_obj, MongoIPDoc) and isinstance(find_dict, dict)
    assert isinstance(find_obj._id, str) is isinstance(find_dict['_id'], str)
    assert str(doc_obj) == str(find_obj) == doc_obj.text == find_obj.text == IPAddr().ping
    assert c.data == doc_obj.data == find_obj.data
    assert c.data == doc_dict['data'] == find_dict['data']


# noinspection PyArgumentList
async def test_mongodoc_ip_async():
    c = MongoIPDoc.get(ips()['google'])
    await c.drop()
    doc_obj = await c.update_async()
    doc_dict = await c.update_async(instance=False)
    find_obj = await c.find_async()
    find_dict = await c.find_async(instance=False)
    assert isinstance(doc_obj, MongoIPDoc) and isinstance(doc_dict, dict)
    assert isinstance(doc_obj._id, IP) is isinstance(doc_dict['_id'], IP)
    assert isinstance(doc_obj.ip, IP) is isinstance(doc_dict['_id'], IP)
    assert isinstance(find_obj, MongoIPDoc) and isinstance(find_dict, dict)
    assert isinstance(find_obj._id, IP) is isinstance(find_dict['_id'], IP)
    assert isinstance(find_obj.ip, IP) is isinstance(find_dict['_id'], IP)
    assert str(doc_obj) == str(find_obj) == doc_obj.text == find_obj.text == IPAddr().google
    assert c.data == doc_obj.data == find_obj.data
    assert c.data == doc_dict['data'] == find_dict['data']

test_mongodoc_ip_sync()
asyncio.run(test_mongodoc_ip_async(), debug=False)


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


