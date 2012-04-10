MakeProject
===========

Creates a simple setup folder for a new project.

    Follows the guide posted at:
    http://guide.python-distribute.org/quickstart.html#lay-out-your-project

    The structure built will match the following:

    | ProjectName/
    |---> LICENSE.txt
        | README.txt
        | setup.py
        | .gitignore    <-- (optional)
        | projectname/
        | ---> __init__.py

For the sake of best practices, __init__.py is left empty.

Requirements
============
Python v2.7

Suggested usage
===============

    >$ python -m makeproject MakeProject -gd /home/user/py/

Changelog
=========
20120409 v0.1 - Created project 

Notes
=====
I have included some outlines to get you started, and pointers to 
some useful utilities for filling out some of the suggested fields in
README.txt (which isn't README.md, I leave changing that up to you).

Among changing the README file's extension type, I also leave it up to
you to change setup.py and adjust the version from '0.1dev' to '0.1', as
well as adjusting the liscense to something less permissive than NC-SA.

This project was, in fact, created by makeproject.py.

Help
====
email issues to droogans@gmail.com

