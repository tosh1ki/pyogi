#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Cython.Distutils import build_ext
from setuptools import setup, Extension


pyx_list = [
    ('koma', 'pyx'),
    ('grid', 'pyx'),
    ('board', 'pyx'),
    ('kifu', 'pyx'),
    ('ki2converter', 'pyx'),
    ('plot', 'py'),
    ('threadcrawler', 'py'),
    ('warscrawler', 'py')
]

ext_modules = []

for name, ex in pyx_list:
    ex = Extension(
        'pyogi.{0}'.format(name),
        sources=['pyogi/{0}.{1}'.format(name, ex)]
    )

    ext_modules.append(ex)


setup(
    name='pyogi',
    packages=['pyogi'],
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext}
)
