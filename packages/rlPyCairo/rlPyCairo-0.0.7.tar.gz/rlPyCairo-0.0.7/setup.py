#!/usr/bin/env python
from setuptools import setup, find_packages
from rlPyCairo import __version__ as version

setup(
    name=str('rlPyCairo'),
    description=str('''Plugin backend renderer for reportlab.graphics.renderPM'''),
    version=version,
    author=str('Robin Becker'),
    author_email=str('robin@reportlab.com'),
    url=str('https://hg.reportlab.com/hg-public/rlPyCairo'),
    long_description=open('README.txt').read(),
    keywords=str('reportlab renderPM'),
    packages=find_packages(exclude=['test']),
    license="BSD license, Copyright (c) 2000-2021, ReportLab Inc.",

    include_package_data=True,
    classifiers=[
        str('Development Status :: 2 - Pre-Alpha'),
        str('Environment :: Web Environment'),
        str('Intended Audience :: Developers'),
        str('License :: OSI Approved :: BSD License'),
        str('Operating System :: OS Independent'),
        str('Programming Language :: Python'),
        str('Programming Language :: Python :: 2'),
        str('Programming Language :: Python :: 2.7'),
        str('Programming Language :: Python :: 3'),
        str('Programming Language :: Python :: 3.6'),
        str('Programming Language :: Python :: 3.7'),
        str('Programming Language :: Python :: 3.8'),
        str('Programming Language :: Python :: 3.9'),
        str('Topic :: Utilities'),
    ],
    python_requires='>=2.7, >=3.6, <4',
    install_requires=['pycairo>=1.20.0','reportlab>=3.5.61'],
    )
