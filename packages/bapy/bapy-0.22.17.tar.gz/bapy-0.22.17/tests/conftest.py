#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Examples:
    Parametrize:
        Alt 1:  pytest_generate_tests() and addr():
                    def test_all_generate_tests(addr):
                        assert IP(addr).text == addr
        Alt 2:  addr() only:
                    @pytest.mark.parametrize('addr', IPAddr._fields, indirect=True)
                    def test_all_parametrize(addr):
                        assert IP(addr).text == addr
"""
import dataclasses
import logging
from collections import namedtuple
from typing import Union

import pytest

import bapy
from bapy import IP
from bapy import IPLoc
from bapy import localhost
from bapy import MongoConn
from bapy import myip
from bapy import Path


def pytest_generate_tests(metafunc):
    if metafunc.function.__name__ in ['test_ip_sync', 'test_ip_async', 'test_ip_default'] \
            and metafunc.module.__name__ == 'test_ip':
        metafunc.parametrize(metafunc.function.__name__.removeprefix('test_'), IPAddr._fields, indirect=True)
    # if 'addr' in metafunc.fixturenames:
    #     metafunc.parametrize('addr', IPAddr._fields, indirect=True)


logging.getLogger('paramiko').setLevel(logging.NOTSET)

IPAddr = namedtuple('IPAddr', 'google localhost myip ping ssh',
                    defaults=('8.8.8.8', localhost, myip(), '24.24.23.2', '54.39.133.155'))


@dataclasses.dataclass(eq=False)
class MongoTest:
    data: Union[list, set] = None

    # noinspection PyArgumentList
    @classmethod
    def get(cls, _id=IPAddr().google, project=True, type_=list):
        mongoconn(project)
        return cls(_id, data=type_([mongoconn(project).name]))

    def asserts(self, key: str):
        d = dict(keys=['_id', 'data'], data=self.data)
        return d[key]


@dataclasses.dataclass(eq=False)
class MongoDoc(MongoTest, bapy.MongoDoc):  # Needed for mongoconn in MongoTest.
    pass


def cd(project=True):
    return Path().cd(bapy.bapy.project) if project else Path().cd(bapy.bapy.tests)


def mongoconn(project=True):
    cd(project)
    return MongoConn()


# <editor-fold desc="IP">
@pytest.fixture(scope="session")
def ip_sync(request, ips):
    return request.param, ips._asdict()[request.param]


@pytest.fixture(scope="session")
def ip_addr():
    return IPAddr._field_defaults


@pytest.fixture
async def ip_async(request):
    return request.param, IPAddr(*[await (IP(addr)).post_init_aio()
                                   for addr in IPAddr._field_defaults.values()])._asdict()[request.param]


@pytest.fixture(scope="session")
def ip_default(request):
    return request.param, IPAddr(*[IP(addr) for addr in IPAddr._field_defaults.values()])._asdict()[request.param]


@pytest.fixture(scope="session")
def ip_loc():
    return IPAddr(*[IPLoc(addr).post_init for addr in IPAddr._field_defaults.values()])._asdict()


@pytest.fixture(scope="session")
def ip_name():
    return IPAddr('dns.google', '1.0.0.127.in-addr.arpa', 'rima-tde', '24.24.23.2',
                  'ns565406.ip-54-39-133.net')._asdict()


@pytest.fixture(scope="session")
def ip_ping():
    return IPAddr(True, True, True, False, True)._asdict()


@pytest.fixture(scope="session")
def ip_ssh():
    return IPAddr(False, False, True, False, True)._asdict()


@pytest.fixture(scope="session")
def ips():
    return IPAddr(*[IP(addr).post_init() for addr in IPAddr._field_defaults.values()])
# </editor-fold>
