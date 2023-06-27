"""Pytest module for testing alfred.structure.project module.
"""
import os
from pathlib import Path

import pytest

# Wgid Imports
from alfred import structure


project = "pytest"
sequence = "rnd"
shot = "deleteme"
wgid_structure_schema = structure.wgid_schema()
wgid_reclusive_structure = structure.recursive_structure(wgid_structure_schema, structure.Root.FACILITY.value)


def test_root_enum():
    """Test Root enum."""
    assert structure.Root.FACILITY.value == "/vfx/projects"
    assert structure.Root.JOB.value == "{job}"
    assert structure.Root.SEQUENCE.value == "{sequence}"
    assert structure.Root.SHOT.value == "{shot}"
    assert structure.Root.ADJOINT_JOB.value == Path("/vfx/projects/{job}")
    assert structure.Root.ADJOINT_SEQUENCE.value == Path("/vfx/projects/{job}/{sequence}")
    assert structure.Root.ADJOINT_SHOT.value == Path("/vfx/projects/{job}/{sequence}/{shot}")


def test_create_one():
    """Test create_one function."""
    context_root = structure.create_one(project, sequence, shot)
    # Check if the whole wgid structure is created
    for path in wgid_reclusive_structure:
        constructed_path = path.format(job=project, sequence=sequence, shot=shot)
        assert os.path.exists(constructed_path)

    formatted_shot_context_root = str(structure.Root.ADJOINT_SHOT.value).format(
        job=project, sequence=sequence, shot=shot
    )
    print(context_root, formatted_shot_context_root)
    assert context_root == formatted_shot_context_root


def test_clean_up():
    """Test clean up function."""
    for path in wgid_reclusive_structure:
        constructed_path = path.format(job=project, sequence=sequence, shot=shot)
        if not os.path.exists(constructed_path):
            continue
        os.rmdir(constructed_path)


if __name__ == "__main__":
    pytest.main(
        [__file__, "-s", "-v", "--cov", "--cov-report=term-missing"],
    )
