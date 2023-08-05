from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='zx_forecasting_framework',
version='0.0.1',
 description='Forecasting framework for ZX projects',
 packages=['zx_forecasting_framework'],
 author='Tamojit Maiti, Shashi Bhushan Singh',
 author_email='shashi.bhushansingh@ab-inbev.com',
 long_description=long_description,
    long_description_content_type='text/markdown'
 ,zip_safe=False)