#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
from bson import InvalidDocument

from bapy import IP
from bapy import IPLoc
from bapy import MongoDocIP
from conftest import mongoconn


# noinspection DuplicatedCode
def test_mongodoc_ip_sync(ips, ip_loc, ip_name, ip_ping, ip_ssh):
    mongoconn(project=False)
    c = MongoDocIP(**ips.ping.kwargs)
    c.drop()
    with pytest.raises(InvalidDocument, match=rf".*cannot encode object.*"):
        doc_obj = c.update_sync()


# noinspection DuplicatedCode
@pytest.mark.asyncio
async def test_mongodoc_ip_async(ips, ip_loc, ip_name, ip_ping, ip_ssh):
    mongoconn()
    c = MongoDocIP(**ips.google.kwargs)
    await c.drop()
    doc_obj = await c.update_async()
    doc_dict = await c.update_async(instance=False)
    find_obj = await c.find_async()
    find_dict = await c.find_async(instance=False)
    assert isinstance(doc_obj, MongoDocIP) and isinstance(doc_dict, dict)
    assert isinstance(doc_obj._id, IP) is isinstance(doc_dict['_id'], IP)
    assert isinstance(doc_obj.ip, IP) is isinstance(doc_dict['_id'], IP)
    assert isinstance(doc_obj.loc, IPLoc) is isinstance(doc_dict['loc'], IPLoc)
    assert isinstance(find_obj, MongoDocIP) and isinstance(find_dict, dict)
    assert isinstance(find_obj._id, IP) is isinstance(find_dict['_id'], IP)
    assert isinstance(find_obj.ip, IP) is isinstance(find_dict['_id'], IP)
    assert isinstance(find_obj.loc, IPLoc) is isinstance(find_dict['loc'], IPLoc)
    assert str(doc_obj) == str(find_obj) == doc_obj.text == find_obj.text == ips.google.text
    assert find_obj.loc.country_name == ip_loc['google'].country_name
    assert find_obj.name == ip_name['google']
    assert find_obj.ping == ip_ping['google']
    assert find_obj.ssh == ip_ssh['google']
