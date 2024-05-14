# add setup.py file to the project root directory
# add the following code to setup.py:

from setuptools import setup, find_packages
import sys

if sys.version_info <= (3, 11):
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
)
# run the following command to install the package:
# python setup.py install
# Now you can import the package in your code like this:
