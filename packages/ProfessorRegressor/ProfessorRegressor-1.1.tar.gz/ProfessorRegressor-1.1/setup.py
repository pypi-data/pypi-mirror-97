#!/usr/bin/env python

import setuptools

with open('README.md','r') as fh:
	longDesc = fh.read()

setuptools.setup(name='ProfessorRegressor',
		version='1.1',
		description='Statistical python model for comparison of species using pairwise regression',
		long_description=longDesc,
		author='Susan & Richard Dykes',
		author_email='chdwck9@gmail.com',
		url='https://github.com/chdwck9/professorRegressor',
		packages=setuptools.find_packages(),
		classifiers=[
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent"
		],
		python_requires='>=3.0'
     )