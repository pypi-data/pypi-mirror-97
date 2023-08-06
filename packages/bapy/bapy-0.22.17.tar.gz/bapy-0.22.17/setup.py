#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""The setup script."""
from setuptools import find_packages
from setuptools import setup

from bapy import bapy
from bapy import Url
from bapy import User

setup(
    author=User.gecos,
    author_email=Url.email(),
    description=bapy.project.description(),
    entry_points={
        'console_scripts': [
            f'{bapy.repo} = {bapy.repo}:app',
        ],
    },
    include_package_data=True,
    install_requires=bapy.project.requirements['requirements'],
    name=bapy.repo,
    package_data={
        bapy.repo: [f'{bapy.repo}/scripts/*', f'{bapy.repo}/templates/*'],
    },
    packages=find_packages(),
    python_requires='>=3.9,<4',
    scripts=bapy.project.scripts_relative,
    setup_requires=bapy.project.requirements['requirements_setup'],
    tests_require=bapy.project.requirements['requirements_test'],
    url=Url.lumenbiomics(http=True, repo=bapy.repo).url,
    use_scm_version=False,
    version='0.22.17',
    zip_safe=False,
)
