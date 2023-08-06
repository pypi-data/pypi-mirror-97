# import libs
import re 
import os
import sys

# main class
class understander:
    """
    main class that understands the provided code

    understander() parses and analyzes the code from the user and provides the
    details needed to successfully containerize the user's API.
    """

    # define init method
    def __init__(self, script):

        # define slots
        self.wd = os.getcwd()

        # name of the file
        self.script = script

        # read in script
        self.script_content = open(self.script).read()

        # prepared script slot
        self.script_prepared = None

        # running from the same dir
        self.script_in_dir = self.script in os.listdir()

        # check python version
        major_v = str(sys.version_info[0])
        minor_v = str(sys.version_info[1])
        micro_v = str(sys.version_info[2])

        # write to slot
        self.py_version = str(major_v + '.' + minor_v + '.' + micro_v)

        # slot for analysis
        self.analysis = None

    # define method to analyze the code
    def analyze(self):

        # prepare the script
        self.script_prepared = self.__prepare_code()

        # extract all the classes in use
        classes_used = self.__get_classes()

        # extract all the functions in use
        functions_used = self.__get_functions()

        # extract all the packages in use
        packages_used = self.__get_packages()

        # extract all the resources to include
        resources_used = self.__get_resources()

        # create analysis report
        self.analysis = {'classes' : classes_used, 
                         'functions' : functions_used,
                         'packages' : packages_used,
                         'resources' : resources_used}

    # define helper function to prepare the script
    def __prepare_code(self):

        # try to remove docstrings
        try:

            # remove docstring from script
            self.script_prepared = re.sub(r'"""[\s\S]*?"""', '', self.script_content)

        # handle exception
        except:

            # raise issue
            raise Exception('There was an issue with the docstrings in the script ' + self.script + ' , they could not be removed')

        # try to split the script into lines
        try:

            # split the script into lines
            self.script_prepared = self.script_prepared.splitlines()
        
        # handle exception
        except:

            # raise issue
            raise Exception('There was an issue with the script ' + self.script + ', it could not be split into lines')

        # try to remove empty lines
        try:

            # remove empty lines
            self.script_prepared = [line for line in self.script_prepared if line != '']
        
        # handle exception
        except:

            # raise issue
            raise Exception('There was an issue with the empty lines in script ' + self.script + ', they could not be removed')

        # try to remove all comments
        try:

            # remove all comments from script
            self.script_prepared = [line for line in self.script_prepared if line[0] != '#']

        # handle exception
        except:

            # raise issue
            raise Exception('There was an issue with comments in script ' + self.script + ', they could not be removed')
    
        # return
        return self

    # function to extract all classes in use
    def __get_classes(self):

        # try to extract the classes
        try:

            # extract classes
            classes_used = [line for line in self.script_prepared if re.search(r'\bclass\b', line)]

        # handle exception
        except:

            # raise issue
            raise Exception('There was an issue detecting classes in script ' + self.script)

        # return classes used
        return classes_used

    # function to extract all functions in use
    def __get_functions(self):

        # try to extract the functions
        try:

            # extract functions
            functions_used = [line for line in self.script_prepared if re.search(r'\bdef\b', line)]

        # handle exception
        except:

            # raise issue
            raise Exception('There was an issue detecting functions in script ' + self.script)

        # return classes used
        return functions_used

    # function to extract all packages in use
    def __get_packages(self):

        # try to find potential packages
        try:

            # find all potentially mentioned packages
            packages_mentioned = [line for line in self.script_prepared if re.search(r'\bimport\b', line)]

        # handle exception
        except:

            # raise issue
            raise Exception('There was an issue finding imported packages in script ' + self.script)

        # package container
        packages_in_use = []

        # iterate over all packages
        for line in packages_mentioned:

            # if it has only two words
            if len(line.strip().split(' ')) == 2:

                # extract the word after import
                packages_in_use.append(re.findall(r'import (\S+)', line)[0].split('.')[0])

            # if it has more than two words and import and from in it
            elif re.search(r'\bimport\b', line) and re.search(r'\bfrom\b', line):

                # extract the word aftere from and split if .
                packages_in_use.append(re.findall(r'from (\S+)', line)[0].split('.')[0])

            # if it has more than two words and import and as in it
            elif re.search(r'\bimport\b', line) and re.search(r'\bas\b', line):

                # extract the word aftere from and split if .
                packages_in_use.append(re.findall(r'import (\S+)', line)[0].split('.')[0])

        # try to find user written packages
        try:

            # find user written packages
            packages_user_written = [package for package in packages_in_use if package in os.listdir()]

        # handle exception
        except:

            # raise issue
            raise Exception('There was an issue finding user written packages in script ' + self.script)

        # separate user written packages from all others
        packages_in_use = list(set(packages_in_use) - set(packages_user_written)) 

        # return 
        return {'libraries' : packages_in_use, 'user-written' : packages_user_written}

    # function to extract resources
    def __get_resources(self):

        # try to get all files in other dirs
        try:

            # get all file in other dirs
            files_in_dirs_in_use = [line for line in self.script_prepared if re.search(r'(\/.*?\.[\w:]+)', line)]

        # handle exception
        except:

            # raise issue
            raise Exception('There was an issue finding files in use in script ' + self.script)

        # try to get all files in same dir
        try:

            # get all files in same dir
            potential_files_in_same_path = [line for line in self.script_prepared if re.search(r'"([A-Za-z0-9_\./\\-]*)"', line)]
            files_in_same_path = [line for line in potential_files_in_same_path if re.search(r'[0-9A-Z]\.', line)]

        # handle exception
        except:

            # raise issue
            raise Exception('There was an issue finding files in use in script ' + self.script)

        # build files in use container
        files_in_use = []

        # iterate over files in dirs
        for files in files_in_dirs_in_use:

            # extract paths between quotes
            files_in_use.append(re.findall(r'"([A-Za-z0-9_\./\\-]*)"', files)[0])

        # iterate over files in same path
        for files in files_in_same_path:

            # extract file between quotes
            files_in_use.append(re.findall(r'"([A-Za-z0-9_\./\\-]*)"', files)[0])

        # figure out which paths to include
        resources_to_include = []

        # iterate over files_in_use
        for filename in files_in_use:

            # extract the paths
            resources_to_include.append(filename.split('/')[0])

        # return
        return resources_to_include