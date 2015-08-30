#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext


ext_modules = []
pyx_list = ['koma', 'grid', 'board', 'kifu', 'ki2converter']
for pyx in pyx_list:
    ex = Extension('pyogi.{0}'.format(pyx),
                   ['pyogi/{0}.pyx'.format(pyx)],
                   include_dirs = ['.'])
    ext_modules.append(ex)

setup(
    name='pyogi',
    version='0.1',
    packages=['pyogi'],
    author='tosh1ki',
    description='Shogi analysis in Python',
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},
    package_data={'pyogi': ['materials/*']}
)
