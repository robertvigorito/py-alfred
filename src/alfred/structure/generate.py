"""A module that assist in generate alfred data structures.
"""
import random
import string


def generate_random_sequence(count, length=3):
    """Generates random sequences.

    Args:
        count (int): The number of sequences to generate.
        length (int): The length of each sequence, default is 3.

    Returns:
        list: A sorted list of randomly generated sequences.
    """
    random_sequences: list = []

    for _ in range(count):
        random_sequence = "".join(random.choices(string.ascii_uppercase, k=length))
        random_sequences.append(random_sequence)
    random_sequences.sort()
    return random_sequences



for random_sequence in generate_random_sequence(count=sequence):
    for shot_number in range(shot_count):
        shot_number *= 10
        shot_number += 10
        shot_number = f"{shot_number:04d}"

        shotcode = f"{random_sequence}{shot_number}"
        new_context_structure: _Dict[str, str] = {
            "job": project,
            "sequence": "RD",
            "shot": shot_number,
            "shotcode": shotcode,
            "created_at": _datetime.datetime.now()
        }
        new_context_structure: _Dict[str, dict] = {"$set": new_context_structure}
        update_many_object = _pymongo.UpdateOne({"job": project}, new_context_structure, upsert=True)
        insert_many.append(update_many_object)


_wgid_context_collection.bulk_write(insert_many)