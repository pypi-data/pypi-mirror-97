#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import collections
import dataclasses
import inspect
from typing import Any
from typing import NamedTuple

import environs
from _pytest.compat import NotSetType

from bapy import _log
from bapy import AsDict
from bapy import AttributeKind
from bapy import datafield
from bapy import LogR
from bapy import Obj
from bapy import Path
from bapy import SemEnum

Named = NamedTuple('Named', a=Any)


class DictA(AsDict):
    _a = 'a'
    c = 3
    log = _log

    __ignore_attr__ = ['b', ]
    __ignore_copy__ = [collections.OrderedDict, ]

    def __init__(self):
        # self.env = environs.Env()
        self._b = 2
        self._d = 4

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return 'b'


class DictB(AsDict):
    _b = 'b'
    dict_a = DictA()
    env = environs.Env()
    path = Path()


class DictC(AsDict):
    _a = 'a'
    c = None
    f = None
    log = _log

    __ignore_attr__ = ['b', ]
    __ignore_copy__ = [collections.OrderedDict, ]

    def __init__(self):
        # self.env = environs.Env()
        self._b = [None, None]
        self._d = {None, self.f}
        self._e = collections.OrderedDict()
        self.f = 2

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return 'b'


@dataclasses.dataclass
class DataA(AsDict):
    a: str = 'a'
    dict_a: DictA = DictA()
    dictionary: dict = datafield(default_factory=dict)
    env: environs.Env = environs.Env()
    integer: int = datafield(default=int(), init=False)
    log: LogR = _log
    path: Path = Path()


def factory():
    return [_log, DataA(), Path(), environs.Env()]


@dataclasses.dataclass
class DataB(AsDict):
    b: str = 'b'
    data_a: DataA = DataA()
    dict_a: DictA = DictA()
    dictionary: dict = datafield(default_factory=dict)
    env: environs.Env = datafield(default_factory=environs.Env)
    integer: int = datafield(default=int(), init=False)
    log: LogR = _log
    lst: list = datafield(default_factory=factory)
    named: Named = Named(DataA)
    named_data_a: Named = Named(DataA())
    path: Path = Path()

    def __post_init__(self):
        self.env.read_env()


@dataclasses.dataclass
class DataC(AsDict):
    _c: str = 'c'
    data_b: DataB = DataB()
    dict_a: DictA = DictA()
    dictionary: dict = datafield(default_factory=dict)
    env: environs.Env = datafield(default_factory=environs.Env)
    integer: int = datafield(default=int(), init=False)
    log: LogR = _log
    path: Path = Path()

    __ignore_kwarg__ = ['path', ]

    def __post_init__(self):
        self.dictionary = dict(a=dict(__a='_a', _a='__a', a='__a'))

    @property
    def c(self):
        return self._c


# noinspection DuplicatedCode
def test_asdict():
    assert DictA().asdict == {'_a': 'a', '_b': 2, '_d': 4, 'a': 'a', 'c': 3, 'log': dict(name=_log.name,
                                                                                         level=_log.level)}
    assert DictB().asdict == {
        '_b': 'b',
        'dict_a': {
            '_a': 'a',
            '_b': 2,
            '_d': 4,
            'a': 'a',
            'c': 3,
            'log': dict(name=_log.name, level=_log.level)
        },
        'env': {},
        'path': '.'
    }

    assert DictC().asdict == {
        '_a': 'a', 'c': None, 'f': 2, 'log': dict(name=_log.name, level=_log.level), '_b': [None, None], '_d': {None},
        '_e': collections.OrderedDict(), 'a': 'a'
    }

    assert DataA().asdict == {
        'a': 'a',
        'dict_a': {
            '_a': 'a',
            '_b': 2,
            '_d': 4,
            'a': 'a',
            'c': 3,
            'log': dict(name=_log.name, level=_log.level)
        },
        'dictionary': {},
        'env': {},
        'integer': 0,
        'log': dict(name=_log.name, level=_log.level),
        'path': '.'
    }

    assert DataB().asdict == {
        'b': 'b',
        'data_a': {
            'a': 'a',
            'dict_a': {
                '_a': 'a',
                '_b': 2,
                '_d': 4,
                'a': 'a',
                'c': 3,
                'log': dict(name=_log.name, level=_log.level)
            },
            'dictionary': {},
            'env': {},
            'integer': 0,
            'log': dict(name=_log.name, level=_log.level),
            'path': '.'
        },
        'dict_a': {
            '_a': 'a',
            '_b': 2,
            '_d': 4,
            'a': 'a',
            'c': 3,
            'log': dict(name=_log.name, level=_log.level)
        },
        'dictionary': {},
        'env': {},
        'integer': 0,
        'log': dict(name=_log.name, level=_log.level),
        'lst': [dict(name=_log.name, level=_log.level),
                {
                    'a': 'a',
                    'dict_a': {
                        '_a': 'a',
                        '_b': 2,
                        '_d': 4,
                        'a': 'a',
                        'c': 3,
                        'log': dict(name=_log.name, level=_log.level)
                    },
                    'dictionary': {},
                    'env': {},
                    'integer': 0,
                    'log': dict(name=_log.name, level=_log.level),
                    'path': '.'
                },
                '.',
                {}],
        'named': {},
        'named_data_a': {
            'a': {
                'a': 'a',
                'dict_a': {
                    '_a': 'a',
                    '_b': 2,
                    '_d': 4,
                    'a': 'a',
                    'c': 3,
                    'log': dict(name=_log.name, level=_log.level)
                },
                'dictionary': {},
                'env': {},
                'integer': 0,
                'log': dict(name=_log.name, level=_log.level),
                'path': '.'
            }
        },
        'path': '.'
    }

    assert DataC().asdict == {
        '_c': 'c',
        'c': 'c',
        'data_b': {
            'b': 'b',
            'data_a': {
                'a': 'a',
                'dict_a': {
                    '_a': 'a',
                    '_b': 2,
                    '_d': 4,
                    'a': 'a',
                    'c': 3,
                    'log': dict(name=_log.name, level=_log.level)
                },
                'dictionary': {},
                'env': {},
                'integer': 0,
                'log': dict(name=_log.name, level=_log.level),
                'path': '.'
            },
            'dict_a': {
                '_a': 'a',
                '_b': 2,
                '_d': 4,
                'a': 'a',
                'c': 3,
                'log': dict(name=_log.name, level=_log.level)
            },
            'dictionary': {},
            'env': {},
            'integer': 0,
            'log': dict(name=_log.name, level=_log.level),
            'lst': [dict(name=_log.name, level=_log.level),
                    {
                        'a': 'a',
                        'dict_a': {
                            '_a': 'a',
                            '_b': 2,
                            '_d': 4,
                            'a': 'a',
                            'c': 3,
                            'log': dict(name=_log.name, level=_log.level)
                        },
                        'dictionary': {},
                        'env': {},
                        'integer': 0,
                        'log': dict(name=_log.name, level=_log.level),
                        'path': '.'
                    },
                    '.',
                    {}],
            'named': {},
            'named_data_a': {
                'a': {
                    'a': 'a',
                    'dict_a': {
                        '_a': 'a',
                        '_b': 2,
                        '_d': 4,
                        'a': 'a',
                        'c': 3,
                        'log': dict(name=_log.name, level=_log.level)
                    },
                    'dictionary': {},
                    'env': {},
                    'integer': 0,
                    'log': dict(name=_log.name, level=_log.level),
                    'path': '.'
                }
            },
            'path': '.'
        },
        'dict_a': {
            '_a': 'a',
            '_b': 2,
            '_d': 4,
            'a': 'a',
            'c': 3,
            'log': dict(name=_log.name, level=_log.level)
        },
        'dictionary': {'a': {'_a': '__a', 'a': '__a'}},
        'env': {},
        'integer': 0,
        'log': dict(name=_log.name, level=_log.level),
        'path': '.'
    }


def test_attrs():
    assert DictA().attrs == ['_a', '_b', '_d', 'a', 'c', 'log']
    assert DataC().attrs == ['_c', 'c', 'data_b', 'dict_a', 'dictionary', 'env', 'integer', 'log', 'path']


# noinspection DuplicatedCode
def test_defaults():
    assert DictA.defaults(nested=False) == DictA().defaults(nested=False)
    assert DictA.defaults(nested=False) == {'_a': 'a', 'c': 3, 'log': _log}

    assert DataA.defaults() == {
        'a': 'a',
        'dict_a': {'_a': 'a', 'c': 3, 'log': dict(name=_log.name, level=_log.level)},
        'dictionary': {},
        'env': {},
        'integer': 0,
        'log': dict(name=_log.name, level=_log.level),
        'path': '.'
    }

    # noinspection DuplicatedCode
    assert DataB.defaults() == {
        'b': 'b',
        'data_a': {
            'a': 'a',
            'dict_a': {'_a': 'a', 'c': 3, 'log': dict(name=_log.name, level=_log.level)},
            'dictionary': {},
            'env': {},
            'integer': 0,
            'log': dict(name=_log.name, level=_log.level),
            'path': '.'
        },
        'dict_a': {'_a': 'a', 'c': 3, 'log': dict(name=_log.name, level=_log.level)},
        'dictionary': {},
        'env': {},
        'integer': 0,
        'log': dict(name=_log.name, level=_log.level),
        'lst': [dict(name=_log.name, level=_log.level),
                {
                    'a': 'a',
                    'dict_a': {'_a': 'a', 'c': 3, 'log': dict(name=_log.name, level=_log.level)},
                    'dictionary': {},
                    'env': {},
                    'integer': 0,
                    'log': dict(name=_log.name, level=_log.level),
                    'path': '.'
                },
                '.',
                {}],
        'named': {},
        'named_data_a': {
            'a': {
                'a': 'a',
                'dict_a': {
                    '_a': 'a',
                    'c': 3,
                    'log': dict(name=_log.name, level=_log.level)
                },
                'dictionary': {},
                'env': {},
                'integer': 0,
                'log': dict(name=_log.name, level=_log.level),
                'path': '.'
            }
        },
        'path': '.'
    }

    assert DataC.defaults() == {
        '_c': 'c',
        'data_b': {
            'b': 'b',
            'data_a': {
                'a': 'a',
                'dict_a': {
                    '_a': 'a',
                    'c': 3,
                    'log': dict(name=_log.name, level=_log.level)
                },
                'dictionary': {},
                'env': {},
                'integer': 0,
                'log': dict(name=_log.name, level=_log.level),
                'path': '.'
            },
            'dict_a': {'_a': 'a', 'c': 3, 'log': dict(name=_log.name, level=_log.level)},
            'dictionary': {},
            'env': {},
            'integer': 0,
            'log': dict(name=_log.name, level=_log.level),
            'lst': [dict(name=_log.name, level=_log.level),
                    {
                        'a': 'a',
                        'dict_a': {
                            '_a': 'a',
                            'c': 3,
                            'log': dict(name=_log.name, level=_log.level)
                        },
                        'dictionary': {},
                        'env': {},
                        'integer': 0,
                        'log': dict(name=_log.name, level=_log.level),
                        'path': '.'
                    },
                    '.',
                    {}],
            'named': {},
            'named_data_a': {
                'a': {
                    'a': 'a',
                    'dict_a': {
                        '_a': 'a',
                        'c': 3,
                        'log': dict(name=_log.name, level=_log.level)
                    },
                    'dictionary': {},
                    'env': {},
                    'integer': 0,
                    'log': dict(name=_log.name, level=_log.level),
                    'path': '.'
                }
            },
            'path': '.'
        },
        'dict_a': {'_a': 'a', 'c': 3, 'log': dict(name=_log.name, level=_log.level)},
        'dictionary': {},
        'env': {},
        'integer': 0,
        'log': dict(name=_log.name, level=_log.level),
        'path': '.'
    }


def test_depth():
    assert Obj(DataC.defaults()['dict_a']).dict
    assert not Obj(DataC.defaults(nested=False)['dict_a']).dict
    assert isinstance(DataC.defaults(nested=False)['dict_a'], DictA)
    assert isinstance(Obj(DictB, depth=1).asdict()['dict_a'].log, LogR)
    assert isinstance(Obj(DataC(), depth=2).asdict()['data_b']['data_a'], DataA)


def test_enum():
    assert Obj(NotSetType).enumcls
    assert not Obj(NotSetType).enuminstance
    assert not Obj(NotSetType).enumdictcls
    assert not Obj(NotSetType).enumdictinstance

    assert not Obj(NotSetType.token).enumcls
    assert Obj(NotSetType.token).enuminstance
    assert not Obj(NotSetType.token).enumdictcls
    assert not Obj(NotSetType.token).enumdictinstance

    assert Obj(AttributeKind).enumcls
    assert not Obj(AttributeKind).enuminstance
    assert Obj(AttributeKind).enumdictcls
    assert not Obj(AttributeKind).enumdictinstance

    assert not Obj(AttributeKind.DATA).enumcls
    assert Obj(AttributeKind.DATA).enuminstance
    assert not Obj(AttributeKind.DATA).enumdictcls
    assert Obj(AttributeKind.DATA).enumdictinstance

    assert Obj(SemEnum).enumcls
    assert not Obj(SemEnum).enuminstance


def test_get():
    assert Obj(DataA).getcls == Obj(DataA()).getcls
    assert Obj(DataB()).mro == (Obj(DataB).getcls, Obj(AsDict).getcls, type(object()))
    assert Obj('__s__').getmodule == inspect.getmodule('__s__')


def test_is():
    assert Obj(True).bool
    assert Obj(b'a').bytes
    assert Obj(lambda x: True).callable
    assert Obj(Obj).cls
    assert Obj(DataA).dataclass
    assert not Obj(DataA()).dataclass
    assert not Obj(DataA).dataclass_instance
    assert Obj(DataA()).dataclass_instance
    assert Obj(collections.defaultdict()).defaultdict
    assert Obj({}).dict
    assert not Obj(Named('a')).dict_instance
    assert Obj(DataA()).dict_instance
    assert not Obj(DataB).dict_instance
    assert Obj(DataB()).dict_instance
    assert Obj({}).dlst
    assert Obj(list()).dlst
    assert Obj(set()).dlst
    assert Obj(tuple()).dlst
    assert Obj('__s__').end
    assert Obj(1.1).float
    assert Obj(1).int
    assert Obj('__s__').iterable
    assert Obj(list()).lst
    assert Obj(set()).lst
    assert Obj(tuple()).lst
    assert not Obj(dict()).lst
    assert Obj(list()).mlst
    assert Obj(set()).mlst
    assert Obj(tuple()).mlst
    assert Obj(dict()).mlst
    assert not Obj(1).mlst
    assert Obj(dict()).mlst
    assert Obj(collections).module
    assert Obj(collections.UserDict({})).mutablemapping
    assert Obj(Named('a')).namedtuple
    assert Obj(collections.OrderedDict({})).ordereddict
    assert Obj(lambda x: True).routine
    assert Obj(set()).set
    assert not Obj('').set
    assert Obj('__s__').start
    assert Obj('_s__', swith='_').start
    assert Obj('__s__').str
    assert not Obj('__s__').tuple
    assert Obj(Named('a')).tuple


def test_kwargs():
    assert isinstance(DataC().kwargs['data_b'], DataB)
    assert isinstance(DataC().kwargs['env'], environs.Env)
    assert isinstance(DataC().kwargs['log'], LogR)
    assert DataC().kwargs.get('path') is None


def test_kwargs_dict():
    assert isinstance(DataC().kwargs_dict['data_b'], dict)
    assert isinstance(DataC().kwargs_dict['env'], dict)
    assert isinstance(DataC().kwargs_dict['log'], dict)
    assert DataC().kwargs_dict.get('path') is None


def test_public():
    assert DataC().public == {
        'c': 'c',
        'data_b': {
            'b': 'b',
            'data_a': {
                'a': 'a',
                'dict_a': {
                    'a': 'a',
                    'c': 3,
                    'log': dict(name=_log.name, level=_log.level)
                },
                'dictionary': {},
                'env': {},
                'integer': 0,
                'log': dict(name=_log.name, level=_log.level),
                'path': '.'
            },
            'dict_a': {'a': 'a', 'c': 3, 'log': dict(name=_log.name, level=_log.level)},
            'dictionary': {},
            'env': {},
            'integer': 0,
            'log': dict(name=_log.name, level=_log.level),
            'lst': [dict(name=_log.name, level=_log.level),
                    {
                        'a': 'a',
                        'dict_a': {
                            'a': 'a',
                            'c': 3,
                            'log': dict(name=_log.name, level=_log.level)
                        },
                        'dictionary': {},
                        'env': {},
                        'integer': 0,
                        'log': dict(name=_log.name, level=_log.level),
                        'path': '.'
                    },
                    '.',
                    {}],
            'named': {},
            'named_data_a': {
                'a': {
                    'a': 'a',
                    'dict_a': {
                        'a': 'a',
                        'c': 3,
                        'log': dict(name=_log.name, level=_log.level)
                    },
                    'dictionary': {},
                    'env': {},
                    'integer': 0,
                    'log': dict(name=_log.name, level=_log.level),
                    'path': '.'
                }
            },
            'path': '.'
        },
        'dict_a': {'a': 'a', 'c': 3, 'log': dict(name=_log.name, level=_log.level)},
        'dictionary': {'a': {'a': '__a'}},
        'env': {},
        'integer': 0,
        'log': dict(name=_log.name, level=_log.level),
        'path': '.'
    }
