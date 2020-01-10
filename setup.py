#
# -*- coding: utf-8 -*-
"""setuptools based setup for pyvb

"""

from os import path

from setuptools import setup, find_packages

#
# get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyvb',
    use_scm_version=True,

    description='A command line tool for building python virtual environments.',
    long_description=long_description,

    author='Jared Crapo',
    author_email='jared@kotfu.net',
    url='https://github.com/kotfu/pyvb',
    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    keywords='pyenv virtualenv',

    packages=find_packages(where="src"),
    package_dir={'':'src'},

    python_requires='>=3.5',

    setup_requires=['setuptools_scm'],

    # dependencies for development and testing
    # $ pip install -e .[dev]
    extras_require={
        'dev': ['pylint', 'flake8',
                'setuptools_scm', 'wheel', 'twine', 'rope', 'invoke',
                ],
    },

    # define the scripts that should be created on installation
    entry_points={
        'console_scripts': [
            'pyvb=pyvb.__main__:main',
        ],
    },

)
