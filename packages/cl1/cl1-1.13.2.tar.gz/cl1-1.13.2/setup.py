#!/usr/bin/env python3

# Note!
# ' are required, do not use any '.

# setup.
from setuptools import setup, find_packages
setup(
	name='cl1',
	version='1.13.2',
	description='Some description.',
	url='http://github.com/vandenberghinc/cl1',
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
    install_requires=[
            'fil3s>=2.15.7',
            'r3sponse>=2.10.3',
        ])