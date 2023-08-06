import os
import sys
import importlib
from salal.core.log import log
from salal.core.config import config

class Handlers:

    #---------------------------------------------------------------------------
    @classmethod
    def load_module_source (cls, name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module
    
    #---------------------------------------------------------------------------

    @classmethod
    def load_handlers (cls, directory):
        # Handlers are a way to determine what processing to carry out
        # in a particular instance based on a 'tag' value. To
        # implement a set of handlers, in <directory> have separate
        # subdirectories for each handler. Each subdirectory should
        # contain a <handler.py> file, which should create an object
        # called <handler>.  The handler object should have a method
        # <get_tags> that returns a list of the tags that should be
        # associated with this particular handler. This method will
        # real all the <handler.py> files, and return a dict where the
        # keys are all the tags, and the values are the corresponding
        # handler objects. Generally each handler object should have
        # one or more additional methods that carry out the actual
        # processing, but what those are and how they are called is up
        # to the code that calls the <load_handler> method.

        handlers = dict()
        for extension_dir in config.system['paths']['extension_dirs']:
            if os.path.isdir(os.path.join(extension_dir, directory)):
                with os.scandir(os.path.join(extension_dir, directory)) as entries:
                    for entry in entries:
                        if entry.is_dir() and not entry.name.startswith('__'):
                            handler_relative_path = os.path.join(directory, entry.name, 'handler.py')
                            handler_full_path = os.path.join(extension_dir, handler_relative_path)
                            if not os.path.exists(handler_full_path):
                                log.message('WARN', 'Handler directory ' + entry.name + ' does not contain a handler.py file')
                            else:
                                package_specifier = os.path.normpath(handler_relative_path).replace(os.sep, '.').replace('.py', '')
                                log.message('TRACE', 'Loading handler from ' + package_specifier)
                                sys.path.insert(0, extension_dir)
                                handler_module = importlib.import_module(package_specifier)
                                sys.path.pop(0)
                                for tag in handler_module.handler.get_tags():
                                    log.message('TRACE', tag)
                                    handlers[tag] = handler_module.handler
        return handlers
    
    #---------------------------------------------------------------------------

handlers = Handlers
