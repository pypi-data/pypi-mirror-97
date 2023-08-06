#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio


def test_daemondoc_sync():
    pass


async def test_daemondoc_async():
    pass

test_daemondoc_sync()
asyncio.run(test_daemondoc_async(), debug=False)
