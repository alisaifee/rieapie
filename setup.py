"""
setup.py for rieapie

"""
__author__ = "Ali-Akber Saifee"
__email__ = "ali@indydevs.org"
__copyright__ = "Copyright 2013, Ali-Akber Saifee"

from setuptools import setup, find_packages
import os
import sys
import rieapie
this_dir = os.path.abspath(os.path.dirname(__file__))
REQUIREMENTS = filter(None, open(os.path.join(this_dir, 'requirements.txt')).read().splitlines())
extra = {}
if sys.version_info >= (3, ):
    extra['use_2to3'] = True

setup(
    name='rieapie',
    author=__author__,
    author_email=__email__,
    license=open('LICENSE.txt').read(),
    url="http://github.com/alisaifee/rieapie",
    zip_safe=False,
    version=rieapie.version,
    classifiers=[k for k in open('CLASSIFIERS').read().split('\n') if k],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    description='Easy REST api wrapper',
    long_description=open('README.rst').read(),
    packages=find_packages(),
    **extra
)
