#!/usr/bin/env python3

# Note!
# ' are required, do not use any '.

# setup.
from setuptools import setup, find_packages
setup(
	name='syst3m',
	version='2.15.8',
	description='Some description.',
	url='http://github.com/vandenberghinc/syst3m',
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=find_packages(),
	zip_safe=False,
	install_requires=[
            'requests',
            'flask',
            'pathlib',
            'selenium',
            'cl1>=1.12.8',
            'fil3s>=2.15.1',
            'r3sponse>=2.9.9',
            'netw0rk>=1.8.6',
        ])