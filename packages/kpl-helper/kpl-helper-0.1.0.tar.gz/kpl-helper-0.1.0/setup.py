#!/usr/bin/env python

from setuptools import setup, find_packages


setup(name='kpl-helper',
      version='0.1.0',
      platforms='any',
      packages=find_packages(),
      install_requires=[
          'requests',
          'requests_toolbelt',
          'flask',
          'flask-cors',
          'PyYAML',
          'kpl-dataset',
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
