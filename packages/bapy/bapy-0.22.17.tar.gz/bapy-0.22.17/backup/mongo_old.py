#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module."""
import asyncio
import collections
import dataclasses
import inspect
import random
import socket
import typing

import decorator

import bapy

import pymongo.errors
@dataclasses.dataclass
class MongoBase1(bapy.SemSpare):
    """MongoOld DB Base Helper Class."""
    connect_timeout: int = 200000
    _db_name: str = 'test'
    env_filename: str = '.mongo'
    host: str = '127.0.0.1'
    max_pool: int = bapy.SemBase.atlas + bapy.SemBase.atlas_new
    password: bapy.NameDefault = None
    port: int = None
    retry: bool = True
    server_timeout: int = 300000
    srv: bool = True
    username: bapy.NameDefault = None
    log: typing.Any = dataclasses.field(default=None, init=False)

    FiltersBase = collections.namedtuple('FiltersBase', 'col_names')
    filters_base = FiltersBase({"name": {"$regex": r"^(?!system\.|.*file|.*glob|.*invalid)"}})
    mongo_exceptions = (socket.gaierror, pymongo.errors.ConnectionFailure, pymongo.errors.AutoReconnect,
                        pymongo.errors.ServerSelectionTimeoutError, pymongo.errors.ConfigurationError,)
    Naps = collections.namedtuple('Naps', 'lock mongo os queue')
    naps = Naps(5, 10, (0.1, 2.1,), 2)

    async def client_aio(self, spare: str = str()) -> bapy.MongoClientMotor:
        args = bapy.Frame.args()
        task = asyncio.current_task().get_name()
        await self.log.adebug('Start', f'{args=}', f'{task=}')
        sem_name = bapy.SemSpare.sem_name.atlas if self.srv else bapy.SemSpare.sem_name.db
        await self.log.awarning(args, f'{task=}', f'{self.sems(sem_name)=}', f'{sem_name.capitalize()} - Waiting')
        async with self.sem(sem_name, spare):
            await self.log.anotice(args, f'{task=}', f'{self.sems(sem_name)=}', f'{sem_name.capitalize()} - Acquired')
            while True:
                try:
                    uri, kwargs = self.connection
                    rv = bapy.MongoClientMotor(uri, **kwargs)
                    await self.log.ainfo(args, f'{task=}', f'{self.sems(sem_name)=}',
                                         f'{sem_name.capitalize()} - Released')
                    await self.log.adebug('End', f'{args=}', f'{task=}')
                    return rv
                except self.mongo_exceptions as exception:
                    await self.log.awarning(
                        f'Waiting for connection: {args}, {task=}, {self.sems(sem_name)=} {repr(exception)}')
                    await self.anap()
                    continue

    async def db_aio(self, spare: str = str()) -> bapy.MongoDBMotor:
        return (await self.client_aio(spare)).get_database(self.db_name)

    @property
    def col_names(self) -> list[str]:
        return self.db.list_collection_names(filter=self.filters_base.col_names)

    async def col_names_aio(self, spare: str = str()) -> list[str]:
        return await (await self.db_aio(spare)).list_collection_names(filter=self.filters_base.col_names)

    async def db_default_aio(self, spare: str = str()) -> bapy.MongoDB:
        return await self.client_aio(spare).get_default_database()


@dataclasses.dataclass
class Mongo1(MongoBase):
    """MongoOld Helper Class."""
    _col_name_default: str = MongoBase._db_name
    col_test_prefix: str = dataclasses.field(default=f'{MongoBase._db_name}_', init=False)
    test: bool = False

    def __post_init__(self):
        super(Mongo, self).__post_init__()

    def col(self, name: str = None) -> MongoCol:
        args = Frame.args()
        name = name if name else self.col_name_default
        name = f'{self.col_test_prefix}{name}' if self.test or MongoBase._db_name not in name else name
        return self.db.get_collection(name)

    async def col_aio(self, spare: str = str(), name: str = None) -> MongoCol:
        args = Frame.args()
        name = name if name else self.col_name_default
        name = f'{self.col_test_prefix}{name}' if self.test or MongoBase._db_name not in name else name
        return (await self.db_aio(spare)).get_collection(name)

    @property
    def col_name_default(self) -> str:
        return self._col_name_default

    @col_name_default.setter
    def col_name_default(self, value: str):
        self._col_name_default = value

    def col_find(self, find: dict = None, name: str = None) -> MongoCursosPy:
        return self.col(name=name).find(find if find else dict())

    def estimated_document_count(self, name: str = None) -> dict:
        return self.col(name).estimated_document_count()

    async def estimated_document_count_aio(self, spare: str = str(), name: str = None) -> dict:
        return (await self.col(spare, name)).estimated_document_count()

        return {item.name: await item.estimated_document_count() for item in await self.cols_list_async}

    def cols_unique(self, field: str = '_id') -> dict:
        return {item.name: item.distinct(field) for item in self.cols_list}

    async def cols_unique_async(self, field: str = '_id', spare: str = str()) -> dict:
        return {item.name: item.distinct(field) for item in await self.cols_list_async}

    def count(self, find: dict = None, col: str = None) -> int:
        return self.col(name=col).count_documents(find if find else dict())

    @property
    async def count_async(self, find: dict = None, col: str = None) -> int:
        return await self.col(True, name=col).count_documents(find if find else dict())

    def count_estimated(self, col: str = None) -> list:
        return self.col(name=col).estimated_document_count()

    async def count_estimated_async(self, col: str = None) -> list:
        return await self.col(True, name=col).estimated_document_count()

    @property
    def count_estimated_default(self) -> list:
        return self.col().estimated_document_count()

    @property
    async def count_estimated_default_async(self) -> list:
        return await self.col(True).estimated_document_count()

    def delete(self, ip: str, col: str = None):
        args = Frame.args()
        self.log.debug('Start', args)
        self.col(True, name=col).delete_one({'_id': ip})
        self.log.debug('End', args)

    async def delete_async(self, ip: str, col: str = None):
        args = Frame.args()
        task = asyncio.current_task().get_name()
        await self.log.adebug('Start', args, f'{task=}')
        await self.col(True, name=col).delete_one({'_id': ip})
        await self.log.adebug('End', args, f'{task=}')

    async def delete_many_async(self, value: dict, col: str = None):
        args = Frame.args()
        del args['value']
        await self.log.adebug('Start', args)
        rv = await self.col(True, name=col).delete_many(value)
        await self.log.adebug('End', f'{args=}')
        return rv

    @property
    async def dump_async(self, col: str = None) -> list:
        await self.log.adebug('Start')
        rv = await self.col(True, name=col).find().to_list(None)
        await self.log.adebug('End')
        return rv

    async def find_async(self, field: str, id_key: bool = True, col: str = None) -> Union[dict[str, dict], list[dict]]:
        args = Frame.args()
        await self.log.adebug('Start', args)
        rv = await self.col(True, name=col).find({field: True}, {'_id': 1, field: 1}).to_list(None)
        if id_key:
            col = dict()
            for item in rv:
                if (value := item.get(field, None)) is not None:
                    rv[item['_id']] = value
            rv = col
        await self.log.adebug('End', args)
        return rv

    def find_field(self, field: str, filtering: typing.Any = None, rv_dict: bool = False,
                   col: str = None) -> Union[dict, list]:
        args = Frame.args()
        self.log.debug('Start', args)
        rv = dict()
        for item in self.col(True, name=col).find({field: True}, {'_id': 1, field: 1}):
            if (value := item.get(field, None)) is not None:
                rv[item['_id']] = value
                if filtering and filtering == value:
                    del rv[item['_id']]
        self.log.debug('End', args)
        if rv_dict:
            return rv
        return list(rv.values())

    async def find_field_async(self, field: str, filtering: typing.Any = None,
                               rv_dict: bool = True, col: str = None) -> Union[dict, list]:
        args = Frame.args()
        await self.log.adebug('Start', args)
        rv = dict()
        for item in await self.col(True, name=col).find({field: True}, {'_id': 1, field: 1}).to_list(None):
            if (value := item.get(field, None)) is not None:
                rv[item['_id']] = value
                if filtering and filtering == value:
                    del rv[item['_id']]
        await self.log.adebug('End', args)
        if rv_dict:
            return rv
        return list(rv.values())

    async def find_one(self, _id: Any, fields: Iterable = None, col: str = None):
        args = Frame.args()
        await self.log.adebug('Start', args)
        rv = await self.col(True, name=col).find_one(
            {'_id': _id}, {'_id': 0} | {field: True for field in iter_split(data=fields)})
        await self.log.adebug('End', args)
        return rv

    async def insert_many_async(self, value: list[dict], col: str = None):
        args = Frame.args()
        del args['value']
        await self.log.adebug('Start', args)
        rv = await self.col(True, name=col).insert_many(value)
        await self.log.adebug('End', f'{args=}')
        return rv

    def unique(self, field: str = '_id', col: str = None) -> list:
        args = Frame.args()
        self.log.debug('Start', args)
        rv = self.col(name=col).distinct(field)
        self.log.debug('End', args)
        return rv

    async def unique_async(self, field: str = '_id', col: str = None) -> list:
        await self.log.adebug('Start')
        rv = await self.col(True, name=col).distinct(field)
        await self.log.adebug('End')
        return rv


__all__ = [item for item in globals() if not item.startswith('_') and not inspect.ismodule(globals().get(item))]
