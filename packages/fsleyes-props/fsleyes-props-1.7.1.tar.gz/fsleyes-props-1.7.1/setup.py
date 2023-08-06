#!/usr/bin/env python
#
# setup.py - setuptools configuration for installing the fsleyes-props
# package.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#


from __future__ import print_function

import os.path as op
import            shutil
from io import    open

from setuptools import setup
from setuptools import find_packages
from setuptools import Command


basedir = op.dirname(__file__)

# Dependencies are listed in requirements.txt
with open(op.join(basedir, 'requirements.txt'), 'rt') as f:
    install_requires = [l.strip() for l in f.readlines()]

packages = find_packages(include=('fsleyes_props', 'fsleyes_props.*'))

# Extract the vesrion number from fsleyes_props/__init__.py
version = {}
with open(op.join(basedir, "fsleyes_props", "__init__.py"), 'rt') as f:
    for line in f:
        if line.startswith('__version__'):
            exec(line, version)
            break
version = version.get('__version__')

with open(op.join(basedir, 'README.rst'), 'rt', encoding='utf-8') as f:
    readme = f.read().strip()


class doc(Command):
    """Build the API documentation. """

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):

        docdir  = op.join(basedir, 'doc')
        destdir = op.join(docdir, 'html')

        if op.exists(destdir):
            shutil.rmtree(destdir)

        print('Building documentation [{}]'.format(destdir))

        import sphinx.cmd.build as sphinx_build

        try:
            import unittest.mock as mock
        except Exception:
            import mock

        mockobj       = mock.MagicMock()
        mockedModules = open(op.join(docdir, 'mock_modules.txt')).readlines()

        mockedModules = [l.strip()   for l in mockedModules]
        mockedModules = {m : mockobj for m in mockedModules}

        patches = [mock.patch.dict('sys.modules', **mockedModules)]

        [p.start() for p in patches]
        sphinx_build.main([docdir, destdir])
        [p.stop() for p in patches]


setup(

    name='fsleyes-props',
    version=version,
    description='[wx]Python event programming framework',
    long_description=readme,
    long_description_content_type='text/x-rst',
    url='https://git.fmrib.ox.ac.uk/fsl/fsleyes/props',
    author='Paul McCarthy',
    author_email='pauldmccarthy@gmail.com',
    license='Apache License Version 2.0',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules'],

    packages=packages,
    install_requires=install_requires,
    test_suite='tests',

    cmdclass={
        'doc' : doc
    }
)
