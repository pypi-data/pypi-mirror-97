import os
from setuptools import setup, find_packages


def read_file(filename):
    basepath = os.path.dirname(os.path.dirname(__file__))
    filepath = os.path.join(basepath, filename)

    if os.path.exists(filepath):
        return open(filepath, encoding='utf8').read()
    else:
        return ''


setup(
    name='pylibwrite',
    version='1.0.1',
    packages=find_packages(),
    include_package_data=True,
    entry_points="""
        [console_scripts]
        pylibwrite=pylibwrite:main
    """,
    description='A library that creates a requirements.txt file using only the libraries listed in the python file directly below it．',
    long_description=read_file('README.rst'),
    author='Shimasan',
    url='https://github.com/Villager-B/pylibwrite',
    keywords=['requirements.txt'])
