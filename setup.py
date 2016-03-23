#!/usr/bin/env python
# coding: utf-8

from distutils.core import setup

setup(
    name='pyEdit',
    version='1.0',
    description='Lightweight IDE',
    author='Marek \'cmoud94\' Kouřil',
    author_email='cmoud94@gmail.com',
    url='https://github.com/cmoud94/pyEdit',
    license='GPLv3 license',
    package_dir={'pyEdit': 'src'},
    packages=['pyEdit', ],
    data_files=[('share/icons/hicolor/scalable/apps', ['pyEdit.png']),
                ('share/applications', ['desktop/pyEdit.desktop'])],
    scripts=['pyEdit']
)
