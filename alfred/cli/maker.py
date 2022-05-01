"""
Command-line tool that create(s) job and shows structure!

optional arguments:
  -h, --help            show this help message and exit
  -j JOB, --job JOB     job where the shot will be created
  -s SHOT_NAMES [SHOT_NAMES ...], --shot_names SHOT_NAMES [SHOT_NAMES ...]
                        List of shot()s to create.
  -fr FRAME_RANGE [FRAME_RANGE ...], --frame-range FRAME_RANGE [FRAME_RANGE ...]
                        Frame range of the shots ingested
"""
import argparse

from wgid import alfred


DATABASE_KWARGS = {}
# TODO: Configurable  # pylint: disable=fixme
DEFAULT_FRAME_RANGE = "1001-1100"

parser = argparse.ArgumentParser(description="Command-line tool that create(s) job and shows structure!")
parser.add_argument(
    "-j", "--job", default="RND", type=str, help="job where the shot will be created"
)
parser.add_argument(
    "-s", "--shot-name", nargs="+", required=True, type=str, help="List of shot()s to create."
)
parser.add_argument(
    "-fr", "--frame-range", nargs="+", default="1001-1100", type=str, help="Frame range of the shots ingested"
)


def create():
    """
    Parse the system arguments, zip the shots and frame range,
    create the folder structure and database entry.

    Returns:
        True is successful
    """
    args = parser.parse_args()
    structure = args.__dict__.copy()

    for i, shot in enumerate(structure.get("shot_name")):
        try:
            frame_range = args.frame_range[i]
        except IndexError:
            frame_range = DEFAULT_FRAME_RANGE
        DATABASE_KWARGS[shot] = {"frame_range": frame_range}

    # Create the folder structure and database entry
    alfred.create.construct(job=structure["job"], shot_names=structure["shot_name"])
    alfred.create.shots(**DATABASE_KWARGS)

    return True


if __name__ == '__main__':
    create()
