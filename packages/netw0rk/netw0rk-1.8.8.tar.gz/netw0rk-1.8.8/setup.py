#!/usr/bin/env python3

# Note!
# ' are required, do not use any '.

# setup.
from setuptools import setup, find_packages
setup(
	name='netw0rk',
	version='1.8.8',
	description='Some description.',
	url='http://github.com/vandenberghinc/netw0rk',
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=find_packages(),
	zip_safe=False,
    install_requires=[
            'fil3s>=2.15.3',
            'r3sponse>=2.10.1',
            'cl1>=1.13.0',
        ])