"""Tests for `alfred` package."""
import os
import requests
import shlex
import subprocess
import toml
import unittest

# Wgid Imports
import alfred


def test_response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    url = "https://github.com/robertvigorito/py-alfred"
    response = requests.get(url)
    assert response.status_code == 200, f"{url} doesnt exist return code {response.status_code}"


def latest_from_github():
    """Find the latest release version from github.

    Notes:
        For unauthenticated requests, the rate limit allows for up to 60
        requests per hour. Unauthenticated requests are associated with the
        originating IP address, and not the user making requests.
    Returns:
        (str) Latest version from github repo
    """
    response = requests.get("https://api.github.com/repos/robertvigorito/py-alfred/releases/latest")
    try:
        latest_release = response.json()["tag_name"].replace("v", "")
    except KeyError:
        latest_release = ""
    return latest_release


def test_version():
    """
    Version test, check pyproject.toml and python package version matches, then
    compare version is greater than latest release.
    """
    pyproject = os.path.join(os.path.dirname(os.path.dirname(__file__)), "pyproject.toml")
    latest_release = latest_from_github()

    with open(pyproject, "r", encoding="utf8") as pyproject_file:
        pyproject_data = toml.load(pyproject_file)
        toml_version = pyproject_data["project"]["version"]

    # Compare the pyproject and python module version, then current compare with the release version
    assert toml_version == alfred.__version__, "pyproject.toml and alfred.__version__ don't match"
    assert latest_release < toml_version, f"Please increment the package version, v{latest_release} release exists!"


class TestAlfred(unittest.TestCase):
    """Tests for `alfred` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_maker_short_args(self):
        """Test command-line tool maker, job/shot creator short format."""
        shot_names = " ".join(["RND_dev_comp", "RND_dev_fx", "RND_dev_pipe"])
        frame_ranges = " ".join(["1001-1024", "1001-1075", "1001-1100"])
        cmd = f"wgid-shot-create -j RND -s {shot_names} -fr {frame_ranges}"
        output = subprocess.check_call(shlex.split(cmd))

    def test_maker_long_args(self):
        """Test command-line tool maker, job/shot creator long format."""
        shot_names = " ".join(["RND_dev_comp", "RND_dev_fx", "RND_dev_pipe"])
        frame_ranges = " ".join(["1001-1024", "1001-1075", "1001-1100"])
        cmd = f"wgid-shot-create -j RND --shot-name {shot_names} --frame-range {frame_ranges}"
        output =  subprocess.check_call(shlex.split(cmd))


    def test_maker_missing_frame_range_args(self):
        """Test command-line tool maker, job/shot creator long format."""
        shot_names = " ".join(["RND_dev_comp", "RND_dev_fx", "RND_dev_pipe"])
        frame_ranges = "1001-1024"
        cmd = f"wgid-shot-create -j RND --shot-name {shot_names} --frame-range {frame_ranges}"
        output = subprocess.check_call(shlex.split(cmd))
        print(output)
