"""
 * $Id:$
 *
 * This file is part of the Cloud Services Integration Platform (CSIP),
 * a Model-as-a-Service framework, API and application suite.
 *
 * 2012-2017, Olaf David and others, OMSLab, Colorado State University.
 *
 * OMSLab licenses this file to you under the MIT license.
 * See the LICENSE file in the project root for more information.
"""

from setuptools import setup, find_packages

setup(name='csip',
      version=open('v.txt').read().strip(),
      url='http://alm.engr.colostate.edu/cb/project/csip',
      license='MIT',
      author='Olaf David',
      author_email='odavid@colostate.edu',
      description='CSIP client library',
      packages=find_packages(include=['csip']),
      long_description=open('README.md').read(),
      data_files=[('', ['v.txt'])],
      install_requires=['requests'],
      zip_safe=False
)
