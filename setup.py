"""Setup file for the package."""

import sys
import pathlib
from setuptools import setup, find_packages


def get_requirements(file_name: str = "requirements.txt"):
    """Get the requirements from the requirements.txt file.
    Returns:
        list: List of requirements. as per the requirements.txt file.
    """
    if (sys.version_info.major == 3) and (6 <= sys.version_info.minor < 11):
        requires = ["tomllib"]
    else:
        requires = []
    requires.append("wheel")
    if not pathlib.Path(file_name).exists():
        return requires
    with open(file_name, "r", encoding="utf-8") as f:
        requires.extend(f.read().splitlines())
    return requires


setup(
    name="py_proj_config",
    version="0.0.2",
    author="Abel Gladstone Mangam",
    install_requires=get_requirements(),
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
)
