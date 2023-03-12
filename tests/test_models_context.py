"""This code is testing the behaviour of a Python class called "context",
which is defined in the alfred.models.contexts module. The first section
defines a dictionary that contains the context structure. This structure
is then used to create a context object. The next three sections test the
behaviour of the context class: the create stage, the conversion to a
dictionary, and the mutability of the class. The tests use the assert statement
to check that the behaviour is as expected.
"""
from dataclasses import (
    asdict,
    FrozenInstanceError
)
from typing import Any

# Wgid Modules
from alfred.models.contexts import context


test_context_structure: dict[str, Any] = {
    "id": 0,
    "job": "test",
    "sequence": "case",
    "shot": 1010,
    "shotcode": "case1010",
    "created_at": 0,
    "created_by": "tester",
}

test_context: context = context(**test_context_structure)


def test_create_context_from_dict() -> None:
    assert context(**test_context_structure), "The context object failed the create stage"


def test_context_to_dict() -> None:
    test_context_as_dict = asdict(test_context)
    assert test_context_as_dict == test_context_structure, "The context vars are not the same from its original structure"


def test_context_is_mutable() -> None:
    try:
        test_context.id = 0
    except (TypeError, FrozenInstanceError):
        pass
    else:
        assert False, "The context class should be frozen and mutable."