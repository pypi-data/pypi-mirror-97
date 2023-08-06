"""Setup the package with pip."""
import os
import setuptools


# https://packaging.python.org/guides/making-a-pypi-friendly-readme/
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()


setuptools.setup(
    name='graph-compression-google-research',
    version='0.0.3',
    license='Apache 2.0',
    author='Google',
    author_email='rinap@google.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='Matrix compression for neural networks.',
    packages=setuptools.find_packages(),
    python_requires='>=3.6')

