#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bapy import fixture_args


@fixture_args
def dog(request, /, name, age=69):
    return f"{name} the dog aged {age}"


# noinspection PyUnusedLocal
@fixture_args
def owner(request, dog, /, name="John Doe"):
    yield f"{name}, owner of {dog}"


@dog.arguments("Buddy", age=7)
def test_with_dog(dog):
    assert dog == "Buddy the dog aged 7"


@dog.arguments("Champion")
class TestChampion:
    def test_with_dog(self, dog):
        assert dog == "Champion the dog aged 69"

    def test_with_default_owner(self, owner, dog):
        assert owner == "John Doe, owner of Champion the dog aged 69"
        assert dog == "Champion the dog aged 69"

    @owner.arguments("John Travolta")
    def test_with_named_owner(self, owner):
        assert owner == "John Travolta, owner of Champion the dog aged 69"
