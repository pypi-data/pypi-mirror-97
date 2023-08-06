#!/usr/bin/env python3

# Note!
# ' are required, do not use any '.

# setup.
from setuptools import setup, find_packages
setup(
	name='syst3m',
	version='2.14.7',
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
            'cl1>=1.12.1',
            'fil3s>=2.13.2',
            'r3sponse>=2.8.9',
            'netw0rk>=1.7.8',
        ])