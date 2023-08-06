import io
import os
import re

from setuptools import find_packages
from setuptools import setup

from sonos_extras import __version__

def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="sonos_extras",
    version=__version__,
    url="https://pypi.org/project/sonos-extras/",
    license='MIT',

    author="MaziarA",
    author_email="maziara2@gmail.com",

    description="Some extra useful commands for Sonos systems, based on SoCo.",
    long_description=read("sonos_extras/README.rst"),

    packages=find_packages(exclude=('tests',)),

    install_requires=["soco==0.19", "python-dateutil"],

    entry_points = {
            'console_scripts': ['SonosExtrasCLI=sonos_extras.bin.SonosExtrasCLI:main'],
        },

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
    ],
)
