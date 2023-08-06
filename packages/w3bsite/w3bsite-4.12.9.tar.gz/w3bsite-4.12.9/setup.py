#!/usr/bin/env python3

# Note!
# ' are required, do not use any '.

# setup.
from setuptools import setup, find_packages
setup(
	name='w3bsite',
	version='4.12.9',
	description='Some description.',
	url='http://github.com/vandenberghinc/w3bsite',
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=[
            'syst3m>=2.12.9',
            'cl1>=1.11.5',
            'fil3s>=2.12.4',
            'r3sponse>=2.8.3',
            'netw0rk>=1.7.2',
            'ssht00ls>=3.18.1',
        ])