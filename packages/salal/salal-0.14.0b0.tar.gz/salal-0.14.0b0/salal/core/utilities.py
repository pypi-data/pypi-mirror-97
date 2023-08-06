import collections.abc
import copy
import glob
import re
import os
from salal.core.log import log

class Utilities:

    #---------------------------------------------------------------------------
    @classmethod
    def deep_update (cls, target_dict, source_dict):
        # Updates <target_dict> with the values from <source_dict>,
        # overwriting existing values. If for a given key <key>,
        # <target_dict[key]> and <source_dict[key]> both exist and are
        # both some kind of Mapping, do a recursive update rather than
        # overwriting.
        for key, source_value in source_dict.items():
            target_value = target_dict.get(key)
            # note that this test will return false if the key isn't present
            # in the target dict, because target_value will be None 
            if isinstance(source_value, collections.abc.Mapping) and isinstance(target_value, collections.abc.Mapping):
                cls.deep_update(target_value, source_value)
            else:
                target_dict[key] = copy.deepcopy(source_value)
    
    #---------------------------------------------------------------------------

    @classmethod
    def find_subdirectories (cls, directory):
        # Returns a list of all subdirectories in the directory indicated by
        # <directory>. Unlike <find_files>, this method is non-recursive.
        result_list = []
        for entry in os.scandir(directory):
            if entry.is_dir():
                result_list.append(entry.name)
        return result_list

    #---------------------------------------------------------------------------

    @classmethod
    def find_files (cls, directory):
        # Recursively finds all files in the directory indicated by
        # <directory>. Returns a list of paths to these files relative
        # to <directory>.

        # For proper creation of a relative path, we need a consistent
        # convention regarding whether the directory has or does not
        # have a trailing separator. Here we've gone with 'has', and
        # add it if missing.
        if directory[-1] != os.sep:
            directory += os.sep
        result_list = []
        # we need to look for files beginning with . specifically, as they
        # don't match * by default
        absolute_paths = glob.glob(directory + '**' + os.sep + '*', recursive = True) + glob.glob(directory + '**' + os.sep + '.*', recursive = True)
        for absolute_path in absolute_paths:
            if os.path.isfile(absolute_path):
                relative_path = re.match('^' + directory + '(.*)$', absolute_path).group(1)
                result_list.append(relative_path)
        return result_list

    #---------------------------------------------------------------------------

    @classmethod
    def find_files_by_extension (cls, directory, extension):
        # Recursively finds all files in the directory indicated by
        # <directory> that have the extension <extension>. Returns a list
        # of paths to these files relative to <directory>.

        # For proper creation of a relative path, we need a consistent
        # convention regarding whether the directory has or does not
        # have a trailing separator. Here we've gone with 'has', and
        # add it if missing.
        if directory[-1] != os.sep:
            directory += os.sep
        result_list = []
        for absolute_path in glob.glob(directory + '**' + os.sep + '*.' + extension, recursive = True):
            relative_path = re.match('^' + directory + '(.*)$', absolute_path).group(1)
            result_list.append(relative_path)
        return result_list

    #---------------------------------------------------------------------------

    @classmethod
    def substitute_variables (cls, string, variables):
        # Jinja-style variable substitution. Any instances within
        # <string> where {{<identifier>}} occurs are replaced by
        # <variables[identifier]> if it exists, or an empty string
        # otherwise. Returns the resulting string. Any whitespace
        # around the identifier is ignored, so {{ <identifier> }} can
        # be used instead if it improves readability. If the variable
        # you need is in a dict inside of <variables>, you can access
        # it with dot notation, i.e., {{ foo.bar }} is equivalent to
        # variables['foo']['bar'].

        # split the string into literal text and variable references
        substrings = re.split('{{\s*(\S+)\s*}}', string)
        result = ''
        for index, substring in enumerate(substrings):
            # because of how re.split works, matching groups will be found
            # at odd-numbered indices in <substrings>
            if index % 2 == 1:
                # dots indicate a reference to a nested variable
                identifiers = substring.split('.')
                cur_dict = variables
                # if the identifier in a variable reference isn't in
                # <variables>, it gets replaced with the empty string
                match = ''
                for index, identifier in enumerate(identifiers):
                    if identifier not in cur_dict:
                        break
                    elif index < len(identifiers) - 1:
                        cur_dict = cur_dict[identifier]
                    else:
                        match = cur_dict[identifier]
                result += match 
            else:
                result += substring
        return result
            
    #---------------------------------------------------------------------------

utilities = Utilities
