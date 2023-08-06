# -*- coding: utf-8 -*-
"""Set up copy-environment package."""


from setuptools import setup, find_packages
import os


with open(os.path.join(os.path.dirname(__file__), 'README.md'),
          'r') as objFile:
    long_desc: str = objFile.read()
__doc__ = long_desc
short_desc: str = long_desc.split('Short Description')[1].split('\n')[1]


setup(name='copy_env',
      version='0.1.2',
      author='Dan Eschman',
      author_email='deschman007@gmail.com',
      url='https://github.com/deschman/reporting',
      classifiers=[
          'Natural Language :: English',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Programming Language :: Python :: 3',
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
      python_requires='~=3.8',
      # TODO: find version dependancies for all of these
      install_requires=['pytest', 'pytest-virtualenv'],
      description=short_desc,
      long_description=long_desc,
      long_description_content_type='text/markdown',
      packages=find_packages())
