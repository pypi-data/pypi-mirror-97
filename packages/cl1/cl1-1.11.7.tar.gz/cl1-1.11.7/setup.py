#!/usr/bin/env python3

# Note!
# ' are required, do not use any '.

# setup.
from setuptools import setup, find_packages
setup(
	name='cl1',
	version='1.11.7',
	description='Some description.',
	url='http://github.com/vandenberghinc/cl1',
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=find_packages(),
	zip_safe=False,
    install_requires=[
            'fil3s>=2.12.7',
            'r3sponse>=2.8.5',
        ])