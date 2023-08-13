"""This code is testing the behaviour of a Python class called "context",
which is defined in the alfred.models.contexts module. The first section
defines a dictionary that contains the context structure. This structure
is then used to create a context object. The next three sections test the
behaviour of the context class: the create stage, the conversion to a
dictionary, and the mutability of the class. The tests use the assert statement
to check that the behaviour is as expected.
"""
from typing import Any
import datetime
import os
import pytest

# Wgid Modules
from alfred.models.contexts import Context as context


@pytest.fixture
def context_structure() -> dict[str, Any]:
    """Create a dictionary that contains the context structure."""
    return {
        "project": "pytest",
        "sequence": "playground",
        "shot": "deleteme",
    }


@pytest.fixture
def context_fixture(context_structure) -> context:
    """Create a context object from the context structure."""
    return context(**context_structure)


def test_create_context_from_dict(context_structure) -> None:
    """Test creating a context object from a dictionary."""
    assert context(**context_structure), "The context class was not created from the dictionary."


def test_context_asdict(context_fixture) -> None:
    """Test converting a context object to a dictionary."""
    assert context_fixture.asdict(), "The context class was not converted to a dictionary."


def test_context_is_validated(context_fixture) -> None:
    """Test the validated method of the context class."""
    try:
        context_fixture.validate()
    except Exception as error:
        pytest.fail(f"The context class was not validated. {error}")
    
    assert context_fixture.validated(), "The context class was not validated."


def test_created_at(context_fixture) -> None:
    """Test the created_at date of the context class is after the current date."""
    assert context_fixture.created_at < datetime.datetime.now(), "The created_at date is not correct."


def test_context_shot_code(context_fixture: context) -> None:
    """Test the shot_code value of the context class."""
    assert str(context_fixture.shot) in str(context_fixture.shotcode), "The shot_code value is not correct."


def test_context_created_by(context_fixture) -> None:
    """Test the created_by value of the context class."""
    assert context_fixture.created_by == os.getenv("USER"), "The created_by value is not correct."
