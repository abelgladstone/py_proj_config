"""Setup file for the package."""

import sys
from setuptools import setup, find_packages

if (sys.version_info.major == 3) and (6 <= sys.version_info.minor < 11):
    requires = ["tomllib"]
else:
    requires = []

setup(
    name="py_proj_config",
    version="0.0.2",
    author="Abel Gladstone Mangam",
    install_requires=requires,
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
)
