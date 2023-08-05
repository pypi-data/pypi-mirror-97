#!/usr/bin/env python

import os

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['barbell2', 'pytest', 'numpy', 'bokeh']

setup_requirements = []

test_requirements = []

setup(
    author="Ralph Brecheisen",
    author_email='ralph.brecheisen@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Dashboard application that extracts data from Castor and displays it",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='castordashboard',
    name='castordashboard',
    packages=find_packages(include=['castordashboard', 'castordashboard.*']),
    setup_requires=setup_requirements,
    entry_points={
        'console_scripts': [
            'demo.etl=castordashboard.etl.script_runner:main',
            'demo.dashboard=castordashboard.dashboard.main:main',
        ],
    },
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/rbrecheisen/castordashboard',
    version=os.environ['VERSION'],
    zip_safe=False,
)
