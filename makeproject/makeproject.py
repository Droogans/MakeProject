#! usr/bin/env python
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

README   = 'readme_template.txt'
LISCENSE = 'standard_liscense.txt'
SETUP    = 'setup_template.txt'
SCRIPT   = 'script_template.txt'
DATA     = 'data_template.db'

import sys, os, errno, argparse, datetime, subprocess

class NewProject(object):
    """interface for building a directory with a new project in it"""
    
    def __init__(self, projectname, directory,
                 use_git=False, use_db=False, use_test=False):
        self.project = projectname
        self.name    = projectname.replace(' ', '')
        self.lowname = self.name.lower()
        self.base    = os.path.abspath(directory)
        
        #defaults
        readme   = open(README  , 'r').read()
        liscense = open(LISCENSE, 'r').read()
        setup    = open(SETUP   , 'r').read()
        self.files = {
            'README.md' :
            readme.format(self.project,
                          '=' * len(self.project),
                          datetime.date.today().strftime("%Y%m%d")
                          ),
            'LISCENSE.txt' : liscense,
            'setup.py' : setup.format(self.project, self.lowname),
            }
        
        self.git, self.db, self.test = use_git, use_db, use_test  

    def newproject(self):
        """creates a file structure for a new project at `directory`"""
        
        self.path = os.path.join(self.base, self.name)
        subpath   = os.path.join(self.path, self.lowname)
        check_build_path(subpath)
        
        for filename, content in self.files.items():
            self.buildfile(filename, content, self.path)

        script = open(SCRIPT, 'r').read().format(self.lowname)
        self.buildfile('{0}.py'.format(self.lowname), script, subpath) 
        self.buildfile('__init__.py', '', subpath)
        
        #optionals
        if self.git:
            self.buildfile('.gitignore', '*.pyc', self.path)
        if self.db:
            datapath = os.path.join(self.path, 'data')
            os.makedirs(datapath)
            copydb = os.path.join(datapath, '{0}.db'.format(self.lowname))
            copy = subprocess.call(['cp', DATA, "%s" % copydb])
        if self.test:
            testpath = os.path.join(self.path, 'tests')
            os.makedirs(testpath)
            self.buildfile('__init__.py', '', testpath)
            
    def buildfile(self, name, content, directory = ""):
        """opens and creates a new file at `directory` with `contents`"""

        if directory:
            directory = os.path.join(directory, name)
            w = open(directory, 'w')
        else:
            loc = os.path.join(self.path, name)
            w = open(loc, 'w')
            
        w.write(content)
        w.close()

        
def check_build_path(loc):
    directory = os.path.normpath(loc)
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        try:
            os.rmdir(directory)
        except OSError as ex:
            if ex.errno == errno.ENOTEMPTY:
                raise OSError("Directory specified must be new or empty")
        check_build_path(loc)
        

if __name__ == '__main__':
    desc = "Creates a simple setup folder for a new project."
    epil = "email issues to: droogans@gmail.com"
    parser = argparse.ArgumentParser(description=desc, epilog=epil)
    parser.add_argument('projectname', type=str,
                        help='project name')
    parser.add_argument('-d', dest='directory',
                        required=False, type=str,
                        help='directory to deploy project, relative accepted')
    parser.add_argument('-g', dest='use_git', action='store_true',
                        default=False, help='create a .gitignore file, *.pyc')
    parser.add_argument('-b', dest='use_db', action='store_true',
                        default=False, help='create a data directory with .db')
    parser.add_argument('-t', dest='use_test', action='store_true',
                        default=False, help='create a directory for unit tests')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 0.1',
                        help='print the module and version, then quit')
    args = vars(parser.parse_args())
    project = NewProject(**args)
    project.newproject()

