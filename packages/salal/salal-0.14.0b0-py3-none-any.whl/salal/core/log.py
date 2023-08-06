import sys

class Log:

    #---------------------------------------------------------------------------

    levels = {
        # this isn't a real message level, it's just for purposes of being
        # able to turn logging off entirely
        'OFF': {
            'severity': 10
        },
        'ERROR': {
            'severity': 5,
            'prefix': '! ',
            'fatal': True
        },
        'WARN': {
            'severity': 4,
            'prefix': '! ',
        },
        'INFO': {
            'severity': 3,
            'prefix': '',
        },
        'DEBUG': {
            'severity': 2,
            'prefix': '  %% ',
        },
        'TRACE': {
            'severity': 1,
            'prefix': '    ++ ',
        }
    }

    # This is a fall-back default; it should only be relevant if an invalid
    # logging level is specified on the command line.
    default_logging_level = 'INFO'

    #---------------------------------------------------------------------------

    @classmethod
    def set_logging_level(cls, level):
        if level in cls.levels:
            cls.logging_level = level
        else:
            cls.message('WARN', 'Attempt to set logging level to unknown level ' + level + ', using default value ' + cls.default_logging_level + ' instead')
            cls.logging_level = cls.default_logging_level
    
    #---------------------------------------------------------------------------

    @classmethod
    def print_to_console (cls, level, text):
        print(cls.levels[level]['prefix'] + text, file = sys.stderr)
    
    #---------------------------------------------------------------------------
    
    @classmethod
    def message (cls, level, text):
        if level not in cls.levels:
            cls.print_to_console('WARN', 'Invalid log message level ' + level)
        else:
            if cls.levels[level]['severity'] >= cls.levels[cls.logging_level]['severity']:
                cls.print_to_console(level, text)
            # note that if a level is set as fatal, we terminate the program
            # regardless of the logging level
            if 'fatal' in cls.levels[level] and cls.levels[level]['fatal']:
                sys.exit(1)

    #---------------------------------------------------------------------------

log = Log
