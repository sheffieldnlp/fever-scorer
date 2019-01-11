from setuptools import setup, find_packages
import sys


with open('requirements.txt') as f:
    reqs = f.read()

reqs = reqs.strip().split('\n')

install = [req for req in reqs if not req.startswith("git+git://")]
depends = [req.replace("git+git://","git+http://") for req in reqs if req.startswith("git+git://")]

setup(
    name='fever-scorer',
    version='1.1.3',
    description='Fact Extraction and VERification scorer',
    long_description="readme",
    license=license,
    package_dir={'fever': 'src/fever'},
    packages=['fever'],
    install_requires=install,
    dependency_links=depends,
)
