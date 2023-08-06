#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup pymdown-extensions theme extras."""

from setuptools import setup, find_packages
import os


def get_version():
    """Get version and version_info without importing the entire module."""

    import importlib.util

    path = os.path.join(os.path.dirname(__file__), 'mkdocs_pymdownx_material_extras', '__meta__.py')
    spec = importlib.util.spec_from_file_location("__meta__", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    vi = module.__version_info__
    return vi._get_canonical(), vi._get_dev_status()


def get_requirements(req):
    """Load list of dependencies."""

    install_requires = []
    with open(req) as f:
        for line in f:
            if not line.startswith("#"):
                install_requires.append(line.strip())
    return install_requires


def get_description():
    """Get long description."""

    with open("README.md", 'r') as f:
        desc = f.read()
    return desc


VER, DEVSTATUS = get_version()


setup(
    name='mkdocs_pymdownx_material_extras',
    version=VER,
    keywords='mkdocs plugin material',
    description='Plugin to extend MkDocs Material theme.',
    long_description=get_description(),
    long_description_content_type='text/markdown',
    author='Isaac Muse',
    author_email='Isaac.Muse@gmail.com',
    python_requires='>=3.6',
    include_package_data=True,
    entry_points={
        'mkdocs.plugins': [
            'mkdocs_pymdownx_material_extras = mkdocs_pymdownx_material_extras:PymdownxMaterialExtras',
        ]
    },
    url='https://github.com/facelessuser/mkdocs_pymdownx_material_extras',
    packages=find_packages(exclude=['tools', 'test*']),
    install_requires=get_requirements("requirements/project.txt"),
    license='MIT License',
    classifiers=[
        'Development Status :: %s' % DEVSTATUS,
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML',
    ]
)
