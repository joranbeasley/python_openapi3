import sys
sys.path.insert(0,"./src")
from python_openapi3 import VERSION

from setuptools import setup

setup(
    name='python-openapi3',
    version=VERSION,
    packages=['python_openapi3', 'python_openapi3.openapi_specification'],
    package_dir={'': 'src'},
    url='http://github.com/joranbeasley/python-openapi',
    license='GPL',
    author='Joran Beasley',
    author_email='joranbeasley@gmail.com',
    description='attempts to provide python binding and validation to all of OAS3.0 spec'
)
