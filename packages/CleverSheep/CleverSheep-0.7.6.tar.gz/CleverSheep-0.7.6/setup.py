#!/usr/bin/env python3
"""Setup script for the CleverSheep."""

import setuptools

import CleverSheep

packages = ['CleverSheep',
            'CleverSheep.App',
            'CleverSheep.Extras',
            'CleverSheep.Log',
            'CleverSheep.Prog',
            'CleverSheep.Sys',
            'CleverSheep.TTY_Utils',
            'CleverSheep.Test',
            'CleverSheep.Test.Tester',
            'CleverSheep.Test.Mock',
            'CleverSheep.TextTools',
            'CleverSheep.VisTools',
            ]

# Note python_requires should be set such that python 2.7 or 3.6+ are supported
setuptools.setup(
    name='CleverSheep',
    version=CleverSheep.version_string,
    description='A collection of packages for high level asynchronous testing.',
    author='Paul Ollis, Laurence Caraccio',
    author_email='cleversheepframework@gmail.com',
    url='https://lcaraccio.gitlab.io/clever-sheep/api/index.html',
    packages=packages,
    py_modules=[],
    scripts=[],
    long_description=CleverSheep.__doc__,
    license="MIT License",
    install_requires=["six", "decorator"],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Natural Language :: English'
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, <4',
)
