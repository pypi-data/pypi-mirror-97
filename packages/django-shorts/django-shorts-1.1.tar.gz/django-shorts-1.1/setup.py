#!/usr/bin/env python
#-*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name = 'django-shorts',
    version = '1.1',
    description = "You spend way too much time typing 'python manage.py'",
    long_description = readme,
    author = "Mhadi Ahmed",
    author_email = "mhadiahmed63@gmail.com",
    url = "https://github.com/mhadiahmed/django-shorts.git",
    py_modules = ['django_shorts'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.8'
    ],
    entry_points={
        'console_scripts': [
            'django=django_shorts:main',
            'd=django_shorts:main',
        ]
    },
)