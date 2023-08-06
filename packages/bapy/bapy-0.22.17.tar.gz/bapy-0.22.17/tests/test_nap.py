#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import socket

import pytest
import time
from bapy import Nap
from bapy import MinMax
from bapy import NapArgs

times = 0


@Nap.MONGO.retry(NapArgs(socket.gaierror, 0, MinMax(0.1, 0.2)))
def while_true(total, first_exc, duration, second_exc=None):
    global times
    while times < total:
        time.sleep(duration)
        times += 1
        raise first_exc
    if second_exc and times == total:
        raise second_exc
    return times


@Nap.HTTPJSON.retry()
def retries(total, duration):
    global times
    while times < total:
        time.sleep(duration)
        times += 1
        raise json.decoder.JSONDecodeError(str(times), 'hola', 1)
    return times


def test_retries_no():
    global times
    times = 0
    duration = 0.1
    total = Nap.HTTPJSON.value.retries
    # json.decoder.JSONDecodeError: 4: line 1 column 2 (char 1)
    with pytest.raises(json.decoder.JSONDecodeError, match=rf".*{total}:.*"):
        assert retries(total, duration) == total


def test_retries_ok():
    global times
    times = 0
    duration = 0.1
    total = Nap.HTTPJSON.value.retries - 1
    assert retries(total, duration) == total


def test_retries_timeout_ok():
    global times

    times = 0
    duration = 3.5
    total = 1
    assert retries(total, duration) == 1


def test_while_true_exception():
    global times
    times = 0
    duration = 0.1
    total = 10

    with pytest.raises(KeyboardInterrupt):
        while_true(total, socket.gaierror, duration, KeyboardInterrupt)


def test_while_true_ok():
    global times
    times = 0
    duration = 0.1
    total = 10
    assert while_true(total, socket.gaierror, duration) == total
