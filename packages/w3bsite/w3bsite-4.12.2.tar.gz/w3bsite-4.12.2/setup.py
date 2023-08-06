#!/usr/bin/env python3

# Note!
# ' are required, do not use any '.

# setup.
from setuptools import setup, find_packages
setup(
	name='w3bsite',
	version='4.12.2',
	description='Some description.',
	url='http://github.com/vandenberghinc/w3bsite',
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=[
        #'ssht00ls',
        #'fil3s',
        #'encrypti0n',
        #'syst3m',
        #'netw0rk',
        #'cl1',
        #'r3sponse',
        'django',
        'xmltodict',
        #'firebase_admin',
        'stripe',
        'requests',
    ])