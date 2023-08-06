#!/usr/bin/env python3

# Note!
# ' are required, do not use any '.

# setup.
from setuptools import setup, find_packages
setup(
	name='syst3m',
	version='2.16.4',
	description='Some description.',
	url='http://github.com/vandenberghinc/syst3m',
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=[
            'requests',
            'flask',
            'pathlib',
            'selenium',
            'pexpect',
            'cl1>=1.13.2',
            'fil3s>=2.15.7',
            'r3sponse>=2.10.3',
            'netw0rk>=1.9.0',
        ])