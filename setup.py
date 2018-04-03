from setuptools import setup, find_packages
import sys


with open('requirements.txt') as f:
    reqs = f.read()

reqs = reqs.strip().split('\n')

install = [req for req in reqs if not req.startswith("git+git://")]
depends = [req.replace("git+git://","git+http://") for req in reqs if req.startswith("git+git://")]

setup(
    name='fever-scorer',
    version='1.0',
    description='Fact Extraction and VERification scorer',
    long_description="readme",
    license=license,
    python_requires='>=3.6',
    packages=find_packages(exclude=('data')),
    install_requires=install,
    dependency_links=depends,
)