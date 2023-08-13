"""The test module for alfred.structure.generate module.
"""
from alfred.structure.generate import generate_random_sequence


def test_generate_random_sequence():
    """Test generate_random_sequence function."""
    sequences = generate_random_sequence(5, length=3)
    assert len(sequences) == 5
    assert all(len(seq) == 3 for seq in sequences)


def test_generate_random_numeric_sequence():
    """Test generate_random_sequence function with numeric_only=True."""
    sequences = generate_random_sequence(10, length=5, numeric_only=True)
    assert len(sequences) == 10
    assert all(seq.isnumeric() for seq in sequences)


def test_generate_random_string_sequence():
    """Test generate_random_sequence function with string_only=True."""
    sequences = generate_random_sequence(3, length=4, string_only=True)
    assert len(sequences) == 3
    assert all(seq.isalpha() and seq.isupper() for seq in sequences)


def test_raise_value_error():
    """Test generate_random_sequence function with numeric_only=True."""
    try:
        generate_random_sequence(10, length=5, numeric_only=True, string_only=True)
    except ValueError:
        pass
    else:
        raise AssertionError("ValueError not raised.")
