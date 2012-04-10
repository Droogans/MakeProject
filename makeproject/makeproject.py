
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
    
    def __init__(self, projectname, directory, use_git=False):
        self.project = projectname
        self.name    = projectname.replace(' ', '')
        self.base    = os.path.abspath(directory)
        
        #defaults
        self.git = use_git
        readme            = open('readme_template.txt',   'r').read()
        standard_liscense = open('standard_liscense.txt', 'r').read()
        setup             = open('setup_template.txt',    'r').read()

        self.files = {
            'README.md' :
            readme.format(self.project,
                          '=' * len(self.project),
                          datetime.date.today().strftime("%Y%m%d")
                          ),
            'LISCENSE.txt' : standard_liscense,
            'setup.py' : setup.format(self.project, self.name.lower())
            }        

    def newproject(self):
        """creates a file structure for a new project at `directory`"""
        
        self.path = os.path.join(self.base, self.name)
        
        sub = self.name.lower()
        subpath = os.sep.join([self.path, sub])

        check_build_path(subpath)
        
        for filename, content in self.files.items():
            self.buildfile(filename, content, directory=self.path)
            
        self.buildfile('__init__.py', content='', directory=subpath)
        
        if self.git:
            self.buildfile('.gitignore', content='*.pyc', directory=self.path)
            

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
                        required=False, type=str, default=__file__,
                        help='directory to deploy project, default to cwd')
    parser.add_argument('-g', dest='use_git', action='store_true',
                        default=False, help='create a .gitignore file, *.pyc')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 0.1',
                        help='print the module and version, then quit')
    args = vars(parser.parse_args())
    project = NewProject(**args)
    project.newproject()

