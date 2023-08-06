# This handler copies the file from the source to the target directory,
# substituting any references to project variables with their current values.
#
# For advanced users: Technically, the files get the full Jinja
# treatment, so you can put anything in the file that you can put in a
# Jinja template. But the only variables that will be available are
# project variables.
import os.path
import jinja2
from salal.core.log import log
from salal.core.config import config

class SimpleExpansion:
    
    #---------------------------------------------------------------------------

    @classmethod
    def get_tags (cls):
        return ['js', 'css', 'py', 'htaccess']
    
    #---------------------------------------------------------------------------

    @classmethod
    def process (cls, tag, source_dir, target_dir, file_stem):
        log.message('TRACE', 'Doing simple expansion')
        env = jinja2.Environment(loader = jinja2.FileSystemLoader(source_dir))
        template = env.get_template(file_stem + '.' + tag)
        output = template.render(config.project)
        with open(os.path.join(target_dir, file_stem + '.' + tag), mode = 'w', encoding = 'utf-8', newline = '\n') as output_fh:
            output_fh.write(output)

    #---------------------------------------------------------------------------

handler = SimpleExpansion
