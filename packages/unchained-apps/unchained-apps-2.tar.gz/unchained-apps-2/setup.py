import os
from setuptools import find_packages, setup



# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    install_requires=['unchained-utils'],
    package_dir={'': 'src'},
    packages=find_packages('src'),
)
