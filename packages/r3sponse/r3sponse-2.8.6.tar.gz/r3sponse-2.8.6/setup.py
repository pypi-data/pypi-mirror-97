#!/usr/bin/env python3

# Note!
# ' are required, do not use any '.

# setup.
from setuptools import setup, find_packages
setup(
	name='r3sponse',
	version='2.8.6',
	description='Some description.',
	url='http://github.com/vandenberghinc/r3sponse',
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=find_packages(),
	zip_safe=False,
	install_requires=[
            'requests',
            'pathlib',
            'django',
            'fil3s>=2.12.8',
        ])