import os
import sys

from setuptools import setup, find_packages
from setuptools.command.install import install

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = '0.0.14'


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches package version.
    git tag looks like zl-py-0.0.1
    """
    description = 'verify that the git tag matches package version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')
        tag_version = tag.split('-')[-1]
        if tag_version != VERSION:
            info = "Git tag version: {0} does not match the version of this app: {1}".format(
                tag_version, VERSION
            )
            sys.exit(info)



setup(
    name='zipline-ai',
    version=VERSION,
    author='Nikhil Simha, Patrick Yoon, Pengyu Hou, Varant Zanoyan',
    author_email='patrick.yoon@airbnb.com',
    packages=find_packages(),
    install_requires=[
        'click==7.0',
        'thrift==0.11',
        'thrift_json==0.1.0',
    ],
    tests_requires=[
        'nose>=1.3.7',
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    scripts=['zipline/repo/materialize.py'],
    description="Zipline python library in bighead package",
    python_requires='>=3.7',  # dataclasses
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)
