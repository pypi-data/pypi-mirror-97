Django shorts
================

You spend too much time typing ``python manage.py``.

Usage
-----

Django shorts installs a ``django`` binary that proxies
Django's ``manage.py`` and ``django-admin.py`` scripts.



    $ django <command or shortcut>

    $ cd any/project/subdirectory
    $ django <command or shortcut>

Requirements
------------

Some commands require additional packages

+ Django 


Shortcuts
---------



ALIASES = {
    # Django
    'c'  : 'collectstatic',
    'r'  : 'runserver',
    'sd' : 'syncdb',
    'sp' : 'startproject',
    'sa' : 'startapp',
    't'  : 'test',

    # Shell
    'd'  : 'dbshell',
    's'  : 'shell',

    # Auth
    'csu': 'createsuperuser',
    'cpw': 'changepassword',

    # database
    'm'  : 'migrate',
    'mkm' : 'makemigrations',

    # session
    'cs' : 'clearsessions',


Installation
------------



    $ pip install django-shorts