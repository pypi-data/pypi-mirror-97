#!/usr/bin/env python3
from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

install_requirements = [
    "nslookup",
]

setup(name='dyntwist',
      version='1.4.0',
      use_scm_version=True,
      setup_requires=['setuptools_scm'],
      description='Discover resolving dynamic DNS domains based on keywords.',
      long_description=readme,
      long_description_content_type='text/markdown',
      url='https://github.com/wesinator/dyntwist',
      author='wesinator',
      author_email='13hurdw@gmail.com',
      include_package_data=True,
      install_requires=install_requirements,
      packages=['dyntwist'],
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
          'Natural Language :: English',
          'Programming Language :: Python :: 3',
      ],
      zip_safe=False)
