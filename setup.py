# add setup.py file to the project root directory
# add the following code to setup.py:

from setuptools import setup, find_packages

setup(
    name="py_proj_config",
    version="0.1",
    packages=find_packages(),
)
# run the following command to install the package:
# python setup.py install
# Now you can import the package in your code like this:
