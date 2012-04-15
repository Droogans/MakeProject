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
        | .gitignore    <-- (optional, ignores *.pyc)
        | projectname/
        | ---> __init__.py

For the sake of best practices, __init__.py is left empty.
"""

import sys, os, errno, argparse, datetime

class NewProject(object):
    """interface for building a directory with a new project in it"""
    
    def __init__(self, projectname, directory, use_git=False, use_db=False):
        self.project = projectname
        self.name    = projectname.replace(' ', '')
        self.lowname = self.name.lower()
        self.base    = os.path.abspath(directory)
        
        #defaults
        self.git, self.db = use_git, use_db
        readme   = open('readme_template.txt'  , 'r').read()
        liscense = open('standard_liscense.txt', 'r').read()
        setup    = open('setup_template.txt'   , 'r').read()

        self.files = {
            'README.md' :
            readme.format(self.project,
                          '=' * len(self.project),
                          datetime.date.today().strftime("%Y%m%d")
                          ),
            'LISCENSE.txt' : liscense,
            'setup.py' : setup.format(self.project, self.lowname),
            }        

    def newproject(self):
        """creates a file structure for a new project at `directory`"""
        
        self.path = os.path.join(self.base, self.name)
 
        subpath  = os.sep.join([self.path, self.lowname])
        testpath = os.sep.join([self.path, 'tests'])
        os.makedirs(testpath)
        
        check_build_path(subpath)
        
        for filename, content in self.files.items():
            self.buildfile(filename, content, directory=self.path)

        script = open('firstscript.txt', 'r').read().format(self.lowname)
        self.buildfile('{0}.py'.format(self.lowname), script, subpath) 
        self.buildfile('__init__.py', '', subpath)
        
        if self.git:
            self.buildfile('.gitignore', '*.pyc', directory=self.path)
        if self.db:
            datapath = os.sep.join([self.path, 'data'])
            os.makedirs(datapath)
            self.buildfile('{0}.db'.format(self.name.lower()), '', datapath)

    def buildfile(self, name, content, directory = ""):
        """opens and creates a new file at `directory` with `contents`"""

        if directory:
            directory = os.sep.join([directory, name])
            w = open(directory, 'w')
        else:
            loc = os.sep.join([self.path, name])
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
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 0.1',
                        help='print the module and version, then quit')
    args = vars(parser.parse_args())
    project = NewProject(**args)
    project.newproject()

