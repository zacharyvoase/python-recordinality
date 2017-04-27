# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='recordinality',
    version='0.0.1',
    description='A Python implementation of the Recordinality sketch',
    long_description=long_description,
    url='https://github.com/zacharyvoase/recordinality',
    author='Zachary Voase',
    author_email='zack@meat.io',
    license='Unlicense',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],

    py_modules=['recordinality'],

    install_requires=[
        'csiphash>=0.0.5',
        'cskipdict>=0.0.1'
    ],
    extras_require={
        'test': ['coverage'],
    },

    entry_points={
        'console_scripts': [
            'recordinality=recordinality:main',
        ],
    },
)
