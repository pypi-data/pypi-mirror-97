# coding=utf-8
import asyncio
import inspect
from icecream import ic

from bapy import AsDict
from bapy import caller
from bapy import runwarning

ic.enable()


def exclude(d, data_attrs: tuple[str, tuple] = None):
    if isinstance(d, str):
        if d.startswith('__'):
            return True

    if data_attrs:
        if data_attrs[0] not in data_attrs[1]:
            return True

    if any([inspect.ismodule(d), inspect.isroutine(d), isinstance(d, property)]):
        return True

# v = {
#     'open': {
#         'ip': {},
#         'sctp': {},
#         'tcp': {
#             80: {'open': True, 'script': {}, 'service': 'http'},
#             443: {'open': True, 'script': {}, 'service': 'https'}
#         },
#         'udp': {}
#     },
#     'filtered': {
#         'ip': {},
#         'sctp': {1: 'http'},
#         'tcp': {
#             80: {'open': True, 'script': {}, 'service': 'http'},
#             443: {'open': True, 'script': {}, 'service': 'https'}
#         },
#         'udp': {
#             80: {'open': True, 'script': {}, 'service': 'https'},
#             72: {'open': True, 'script': {'a': 4}, 'service': 'https'}
#         }
#     }
# }
# ic(Nested(v, 0, 'service'))
# assert not Nested(v, 0, 'service').values('x')
# assert Nested(v, 0, 'service').exclude('service')
# assert not dpath.util.search(Nested(v, 0, 'service').run(), '**/service')
# assert not dpath.util.search(Nested(v, 0, values='http').run(), '**', afilter=lambda x: 'http' == x)
# assert not dpath.util.search(Nested(v, 0, 'service', values='http').run(), '**', afilter=lambda x: 'http' == x)


# noinspection PyUnusedLocal
def arg(b, x=1, *args, **kwargs):
    return caller(1, depth=1)


@runwarning
def test_caller():
    class A(AsDict):
        g = 1

        def __init__(self):
            self.a_1 = 1

        def a(self):
            self.a_1 = 2
            index = 2
            c = caller(index, glob=True, loc=True, depth=2, _vars=True)
            assert not c.coro
            assert c.funcname == 'test_caller'
            assert c.qual == 'test_caller'

        async def c(self):
            index = 2
            c = caller(index, _vars=True)
            if c.funcname == '_run':
                assert not c.coro
                assert not c.vars.glob
                assert not c.vars.loc
            if c.funcname == 'f':
                assert c.coro
            self.d()
            return c

        @classmethod
        def d(cls):
            index = 2
            c = caller(index, _vars=True)
            if c.funcname == 'c':
                assert c.coro
                assert 'Task' in c.task
            return c

        @property
        async def f(self):
            index = 2
            c = caller(index, _vars=True)
            await self.c()
            return c

    obj = A()
    obj.a()
    asyncio.run(obj.c(), debug=False)


def test_arg():
    arg_caller_local = arg(2)
    assert arg_caller_local.funcname == arg.__name__
    assert arg_caller_local.coro is None
    assert arg_caller_local.args == {'b': 2, 'x': 1}
    assert arg(3, 7, 9).args == {'args': (9,), 'b': 3, 'x': 7}
    assert arg(3, 7, 9, first=2, second=3).args == {'args': (9,), 'b': 3, 'first': 2, 'second': 3, 'x': 7}
    assert arg(3, 8, 7, first=2, second=3).args == {'args': (7,), 'b': 3, 'first': 2, 'second': 3, 'x': 8}
    assert arg(3, 8, first=2, second=3).args == {'b': 3, 'first': 2, 'second': 3, 'x': 8}
