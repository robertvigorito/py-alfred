"""This code is testing the behaviour of a Python class called "context",
which is defined in the alfred.models.contexts module. The first section
defines a dictionary that contains the context structure. This structure
is then used to create a context object. The next three sections test the
behaviour of the context class: the create stage, the conversion to a
dictionary, and the mutability of the class. The tests use the assert statement
to check that the behaviour is as expected.
"""
from ast import main
from dataclasses import asdict, FrozenInstanceError
import datetime
from typing import Any

# Wgid Modules
from alfred.models.contexts import context
import pytest


@pytest.fixture
def context_structure() -> dict[str, Any]:
    return {
        "job": "pytest",
        "sequence": "playground",
        "shot": "deleteme",
    }


@pytest.fixture
def context_fixture(context_structure) -> context:
    return context(**context_structure)


def test_create_context_from_dict(context_structure) -> None:
    assert context(
        **context_structure
    ), "The context class was not created from the dictionary."


def test_context_asdict(context_fixture) -> None:
    assert asdict(
        context_fixture
    ), "The context class was not converted to a dictionary."


def test_context_is_validated(context_fixture) -> None:
    assert context_fixture.validated(), "The context class was not validated."


def test_created_at(context_fixture) -> None:
    assert context_fixture.created_at < datetime.datetime.now(), "The created_at date is not correct."


def test_context_asdict(context_fixture) -> None:
    
    
if __name__ == "__main__":
    # run this pytest file in isolation, show the code lines that are missing coverage
    pytest.main([__file__, "--cov=alfred.models.contexts", "--cov-report=html", "--cov-report=term-missing"])
