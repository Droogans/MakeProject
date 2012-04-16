MakeProject
===========

"""
Creates a simple setup folder for a new project.

    Follows the guide posted at:
    http://guide.python-distribute.org/quickstart.html#lay-out-your-project

    The structure built will match the following:

    | ProjectName/
    |---> LICENSE.txt
        | README.md
        | setup.py
        | .gitignore              <-- (optional, ignores *.pyc)
        | data/                   <-- (optional, sqlite3)
            | ---> projectname.db
        | projectname/
            | ---> __init__.py
            | ---> projectname.py
        | tests/                  <-- (optional, highly recommended)
            | ---> __init__.py

For the sake of best practices, all __init__.py files are left empty.
"""

Requirements
------------
Python v2.7

Suggested usage
---------------

    >$ python -m makeproject ProjectName -gbtd /home/user/py/

Changelog
---------
    20120409 v0.1 - Created project
    20120416 v0.1 - sqlite3 database, tests directory options

Notes
-----
I have included some outlines to get you started, and pointers to 
some useful utilities for filling out some of the suggested fields in
`README.md`. I leave it up to you to change `setup.py`, and adjust its 
version from '0.1dev' to '0.1', as well as adjusting the liscense to 
somethingless permissive than NC-SA, if that is required.

This project was, in fact, created by makeproject.py.

Help
----
email issues to droogans@gmail.com

