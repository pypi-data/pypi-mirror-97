# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name="reposmgr",
    version='0.0.6',
    description='(Very) Simple set of commands to manage a set of repository with one file (git only)',
    author='Jakub Janoszek',
    author_email='jqbj@protonmail.com',
    url='https://bitbucket.org/jqb/reposmgr',
    py_modules=['reposmgr'],
    install_requires=[
    ],
    scripts=[
        'bin/reposmgr-switch-version',
        'bin/reposmgr-update-repo',
        'bin/reposmgr-update-all',
        'bin/reposmgr-ensure-repo',
        'bin/reposmgr-ensure-all',
        'bin/reposmgr-reclone-repo',
        'bin/reposmgr-reclone-all',
        'bin/reposmgr-status',
    ],
    entry_points='''
        [console_scripts]
        reposmgr=reposmgr:main
    ''',
    include_package_data=True,
    zip_safe=False,
)

# Usage of setup.py:
# $> python setup.py build sdist upload   # build, make source dist and upload to PYPI
