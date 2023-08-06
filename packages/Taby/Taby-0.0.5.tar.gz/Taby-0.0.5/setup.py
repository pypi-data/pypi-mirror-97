from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.5'
DESCRIPTION = 'CLI for highlighting tab spaces in a file'
with open('README.md', 'r') as fh:
    long_description = fh.read()

# Setting up
setup(
    name="Taby",
    version=VERSION,

    author="Sombodee (Landon Hutchins)",
    license = 'MIT',
    description=DESCRIPTION,
    long_description = long_description,
    long_description_content_type = "text/markdown",
    
    packages=['Taby'],
    install_requires=[],
    keywords=['python', 'tabs', 'highlight', 'CLI'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)