#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest

from bapy import IP
from bapy import IPv4
from bapy import IPLoc


# noinspection DuplicatedCode
def test_ip_sync(ip_addr, ip_sync, ip_loc, ip_name, ip_ping, ip_ssh):
    assert isinstance(ip_sync[1], IP)
    assert isinstance(ip_sync[1].ip, IPv4)
    assert isinstance(ip_sync[1].loc, IPLoc)
    assert ip_sync[1].text == ip_addr[ip_sync[0]]
    assert ip_sync[1].loc == ip_loc[ip_sync[0]]
    assert ip_name[ip_sync[0]] in ip_sync[1].name
    assert ip_sync[1].ping is ip_ping[ip_sync[0]]
    assert ip_sync[1].ssh is ip_ssh[ip_sync[0]]


def test_ip_default(ip_addr, ip_default, ip_loc, ip_name, ip_ping, ip_ssh):
    assert isinstance(ip_default[1], IP)
    assert isinstance(ip_default[1].ip, IPv4)
    assert ip_default[1].text == ip_addr[ip_default[0]]
    assert ip_default[1].loc is None
    assert ip_default[1].name is None
    assert ip_default[1].ping is None
    assert ip_default[1].ssh is None


# noinspection DuplicatedCode,PyUnresolvedReferences
@pytest.mark.asyncio
async def test_ip_async(ip_addr, ip_async, ip_loc, ip_name, ip_ping, ip_ssh, ips):
    assert isinstance(ip_async[1], IP)
    assert isinstance(ip_async[1].ip, IPv4)
    assert isinstance(ip_async[1].loc, IPLoc)
    assert ip_async[1].text == ip_addr[ip_async[0]]
    assert ip_async[1].loc == ip_loc[ip_async[0]]
    assert ip_name[ip_async[0]] in ip_async[1].name
    assert ip_async[1].ping is ip_ping[ip_async[0]]
    if ip_async[1].name != ips.myip.name:
        assert ip_async[1].ssh is ip_ssh[ip_async[0]]


def test_sort(ips):
    assert sorted([ips.localhost, ips.myip, ips.ssh, ips.google, ips.ping]) == \
           [ips.google, ips.ping, ips.ssh, ips.myip, ips.localhost]
