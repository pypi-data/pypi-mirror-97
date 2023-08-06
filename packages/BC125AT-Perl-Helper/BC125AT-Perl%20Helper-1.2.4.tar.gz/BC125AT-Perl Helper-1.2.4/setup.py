from setuptools import setup
import bc125at_perl_helper as b

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name=b.PROGRAM_NAME,
	version=b.PROGRAM_VERSION,
	packages=['bc125at_perl_helper'],
	url=b.PROGRAM_URL,
	license='Mozilla Public License version 2.0',
	author=b.PROGRAM_AUTHOR,
	author_email='',
	description='A tool to convert bc125at-perl\'s output to CSV and back.',
	long_description=long_description,
	long_description_content_type="text/markdown",
	entry_points={
		'console_scripts': ['bc125at-perl-helper=bc125at_perl_helper:_main']
	},
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6'
)
