#!/usr/bin/env python

from setuptools import setup, find_packages


setup(name='kpl-helper',
      version='0.0.7',
      platforms='any',
      packages=find_packages(),
      install_requires=[
          'requests',
          'PyYAML',
          'kpl-dataset',
          'requests_toolbelt',
      ],
      entry_points={
          "console_scripts": [
              "khelper = kpl_helper.cli.main:main",
          ],
      },
      classifiers=[
          'Programming Language :: Python',
          'Operating System :: OS Independent',
      ])
