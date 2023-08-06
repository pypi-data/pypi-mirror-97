# !/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages


__author__ = ["Felix Nitsch", "Christoph Schimeczek", "Ulrich Frey", "Marc Deissenroth-Uhrig", "Benjamin Fuchs"]
__copyright__ = "Copyright 2020, German Aerospace Center (DLR)"
__credits__ = ["Kristina Nienhaus", "Evelyn Sperber", "Seyedfarzad Sarfarazi"]

__license__ = "Apache License 2.0"
__maintainer__ = "Felix Nitsch"
__email__ = "fame@dlr.de"
__status__ = "Production"


def readme():
      with open('README.md') as f:
            return f.read()


setup(name='fameio',
      version='1.1.1',
      description='Python scripts for operation of FAME models',
      long_description='''
                       Python scripts for FAME models, generation of protobuf input files and conversion of protobuf 
                       output files. 
                       ''',
      keywords=['FAME', 'agent-based modelling'],
      url='https://gitlab.com/fame-framework/fame-io',
      author=', '.join(__author__),
      author_email=__email__,
      license=__license__,
      package_dir={'': 'src'},
      packages=find_packages(where='src'),
      entry_points={
            'console_scripts': [
                  'makeFameRunConfig=famepy.scripts:makeFameRunConfig',
                  'convertFameResults=famepy.scripts:convertFameResults',
            ],
      },
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
      ],
      install_requires=['pandas', 'protobuf', 'pyyaml'],
      include_package_data=True,
      zip_safe=False,
      python_requires='>=3.6',
      )
