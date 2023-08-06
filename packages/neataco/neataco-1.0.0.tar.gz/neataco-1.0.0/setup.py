import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()


setup(
    name='neataco',
    version='1.0.0',
    description='Neat ACO is an Ant Colony Optimization algorithm written in pure Python.',
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'License :: OSI Approved :: GNU Affero General Public License v3'
    ],
    author='Landreville',
    url='https://gitlab.com/landreville/neataco',
    packages=find_packages(),
    install_requires=[],
)
