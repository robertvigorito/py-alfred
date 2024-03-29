"""
Showtime

Startup tool, setting configs environments per show needs

# usage
# showtime {shot_name}
# showtime -h --help  # Display tree of current shots
"""
import os
import argparse
import sys

from anytree import Node, RenderTree
from wgid.alfred import search

# Creating the arg parser
parser = argparse.ArgumentParser()
parser.add_argument("code", help="Show name or shot code")
parser.add_argument("-t", "--tree", nargs="?", const=True, help="Display the all shots of the show")
args = parser.parse_args()
code = args.code


def show_tree(job):
    """
    Show tree, displays the shots of the show in a tree view manner.
    Usage to aid artist when referencing assigned shots.

    Examples:
        show
            - scene
                - shot-names
    Args:
        job (str):       Job name
    """
    print("# " + "-" * 50)
    print(f"Showtime shots list for `{job.upper()}`\n")
    query = search.scenes_shots(args.code)
    job_node = Node(job)

    for scene, shots in sorted(query.items()):
        scene = Node(scene, parent=job_node)
        for shot in sorted(shots):
            Node(shot, parent=scene)

    for parent, _, node in RenderTree(job_node):
        print(f"{parent}{node.name}")

    print("\nExample:\nshowtime {show} {shot-name}")


def its_showtime():
    """
    Well its showtime, upon user arguments, validate code or shot name,
    set environment and show configs.
    """
    # Attributes
    job, scene, shot = "", "", ""
    # Validate the code if job or shot name
    shot_data = search.shots(shot_name=code)
    if search.jobs(code):
        job = code

    elif shot_data:
        job, scene, shot = shot_data.get("job"), shot_data.get("scene"), code

    else:
        print("Wrong job code provide, try again with correct code...")
        sys.exit(1)

    # Display project tree
    if args.tree and not shot_data:
        show_tree(job)
        sys.exit(1)

    # Set the environment
    os.environ["JOB"] = job.upper()
    os.environ["SCENE"] = scene.upper()
    os.environ["SHOT"] = shot.upper()

    print("# " + "-" * 50)
    print(f"Showtime: {shot.upper() or job.upper()}!")
    return True
