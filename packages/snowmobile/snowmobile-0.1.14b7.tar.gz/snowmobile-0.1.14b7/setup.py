import pathlib
import subprocess

from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


setup(
    description="An analytics-focused wrapper around the snowflake-connector-python",
)
