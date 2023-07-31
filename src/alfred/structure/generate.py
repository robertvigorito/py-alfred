"""The `generate` module provides functions for generating Alfred data structures, such as sequence and shot names, 
for use in context construction.


Example usage:
    >>> from generate import generate_sequence_name, generate_shot_name, parse_shot_name
    >>> generate_sequence_name("my_project", 1)
    >>> "my_project_s001"
    >>> generate_shot_name("my_project_s001", 10)
    >>> "my_project_s001_010"
    >>> parse_shot_name("my_project_s001_010")
    >>> ("my_project_s001", 10)
"""
from math import ceil as _ceil
import random as _random
import string as _string


def generate_random_sequence(count, length=3, numeric_only=False, string_only=False):
    """Generates random sequences.

    Args:
        count (int): The number of sequences to generate.
        length (int): The length of each sequence, default is 3.

    Returns:
        list: A sorted list of randomly generated sequences.
    """
    random_sequences: list = []
    first_slice = _ceil(length / 2)
    second_slice = (length - first_slice) * -1
    if numeric_only and string_only:
        raise ValueError("Only one of numeric_only or string_only can be True.")

    for _ in range(count):
        if numeric_only:
            random_sequence = "".join(_random.choices(_string.digits, k=length))
        elif string_only:
            random_sequence = "".join(_random.choices(_string.ascii_uppercase, k=length))
        else:
            random_sequence = "".join(_random.choices(_string.ascii_uppercase, k=length))
            random_sequence += "".join(_random.choices(_string.digits, k=length))
            random_sequence = random_sequence[first_slice:second_slice]
        random_sequences.append(random_sequence)
    random_sequences.sort()
    return random_sequences
