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

