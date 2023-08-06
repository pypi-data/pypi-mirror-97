#!/usr/bin/env python3

# Note!
# ' are required, do not use any '.

# setup.
from setuptools import setup, find_packages
setup(
	name='imag3',
	version='1.0.7',
	description='Some description.',
	url='http://github.com/vandenberghinc/imag3',
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=find_packages(),
	include_package_data=True,
	zip_safe=False,
	install_requires=[
            'cl1>=1.12.1',
            'fil3s>=2.13.2',
            'syst3m>=2.14.7',
            'r3sponse>=2.8.9',
            'netw0rk>=1.7.8',
        ],)