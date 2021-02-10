"""Tests for `alfred` package."""

import pytest
import subprocess
import unittest


def test_response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    import requests
    url = "https://github.com/robertvigorito/alfred"
    response = requests.get(url)
    assert response.status_code == 200, f"{url} doesnt exist return code {response.status_code}"


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
        cmd = f"poetry run wg-shot-create -j RND -s {shot_names} -fr {frame_ranges}"
        # subprocess.check_call(cmd, shell=True)

    def test_maker_long_args(self):
        """Test command-line tool maker, job/shot creator long format."""
        shot_names = " ".join(["RND_dev_comp", "RND_dev_fx", "RND_dev_pipe"])
        frame_ranges = " ".join(["1001-1024", "1001-1075", "1001-1100"])
        cmd = f" poetry run wg-shot-create -j RND --shot-name {shot_names} --frame-range {frame_ranges}"
        # subprocess.check_call(cmd, shell=True)

    def test_maker_missing_frame_range_args(self):
        """Test command-line tool maker, job/shot creator long format."""
        shot_names = " ".join(["RND_dev_comp", "RND_dev_fx", "RND_dev_pipe"])
        frame_ranges = "1001-1024"
        cmd = f" poetry run wg-shot-create -j RND --shot-name {shot_names} --frame-range {frame_ranges}"
        # subprocess.check_call(cmd, shell=True)

