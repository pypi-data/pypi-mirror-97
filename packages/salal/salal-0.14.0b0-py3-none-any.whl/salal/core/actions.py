import os
import importlib
from salal.core.log import log
from salal.core.config import config
from salal.core.handlers import handlers
from salal.core.utilities import utilities

class Actions:

    #---------------------------------------------------------------------------

    @classmethod
    def initialize (cls):
        if 'action_commands' not in config.system:
            log.message('ERROR', 'No actions are configured')
        log.message('DEBUG', 'Loading command handlers')
        cls.handlers = handlers.load_handlers(config.system['paths']['command_handlers_dir'])

    #---------------------------------------------------------------------------

    @classmethod
    def execute_internal_command (cls, command):
        if command in cls.handlers:
            cls.handlers[command].execute(command)
        else:
            log.message('ERROR', 'Command ' + command + ' is not configured.')
        
    #---------------------------------------------------------------------------

    @classmethod
    def execute (cls, action):
        # Make sure this action is defined
        if action not in config.system['action_commands']:
            log.message('ERROR', 'The action ' + action + ' is not configured')
        else:
            log.message('INFO', 'Beginning ' + action + ' for ' + config.profile + ' profile')
            
        # Iterates through the list of commands associated with 'tag',
        # does substitution for system variables, and passes them to
        # the OS for execution
        for command_spec in config.system['action_commands'][action]:
            if command_spec['type'] == 'internal':
                cls.execute_internal_command(command_spec['command'])
            elif command_spec['type'] == 'external':
                command_string = utilities.substitute_variables(command_spec['command'], config.system)
                log.message('INFO', command_string)
                os.system(command_string)
            else:
                log.message('ERROR', 'Unrecognized command type ' + command_spec['type'])
 
    #---------------------------------------------------------------------------
    
actions = Actions
