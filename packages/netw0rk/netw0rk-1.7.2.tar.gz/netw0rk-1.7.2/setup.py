#!/usr/bin/env python3

# Note!
# ' are required, do not use any '.

# setup.
from setuptools import setup, find_packages
setup(
	name='netw0rk',
	version='1.7.2',
	description='Some description.',
	url='http://github.com/vandenberghinc/netw0rk',
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=find_packages(),
	zip_safe=False,
    install_requires=[
    ])