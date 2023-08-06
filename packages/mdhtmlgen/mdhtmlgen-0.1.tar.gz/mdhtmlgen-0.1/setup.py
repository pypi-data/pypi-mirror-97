#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
	name='mdhtmlgen',
	version='0.1',
	description='Markdown based html generator.',
	long_description='Markdown based html generator. Generation requires: HTML template and markdown template, and additional meta-extensions allow you to add metaprogramming to this process',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Environment :: Console',
		'Intended Audience :: End Users/Desktop',
		'Intended Audience :: Developers',
		'Intended Audience :: System Administrators',
		'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
		'Topic :: Text Processing :: Markup :: HTML',
	],
	keywords='markdown html generator template metaprogramming',
	url='https://github.com/mega-t72/mdhtmlgen',
	author='Fedor Laktionov',
	author_email='f.laktionov@gmail.com',
	license='BSD',
	license_files = ('LICENSE.txt',),
	packages=find_packages(),
	install_requires=['optparse-pretty', 'markdown'],
	include_package_data=True,
	zip_safe=False
)
