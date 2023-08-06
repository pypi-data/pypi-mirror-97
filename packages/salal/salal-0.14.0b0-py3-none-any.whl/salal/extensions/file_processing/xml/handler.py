# This recursively expands the templates specified in the XML source file,
# and writes the result to an HTML file. During the expansion, templates
# have access to both the project variables and the attributes and content
# provided with the corresponding tag.
import os.path
import re
import jinja2
import xml.etree.ElementTree as ET
from salal.core.log import log
from salal.core.config import config
from . import custom_jinja_functions

class XMLHandler:

    #---------------------------------------------------------------------------

    @classmethod
    def get_tags (cls):
        return ['xml']

    #---------------------------------------------------------------------------

    @classmethod
    def configure_modules (cls, node, env):
        module_dirs = [os.path.join(config.system['paths']['design_root'], config.system['paths']['module_dir'])]
        if 'theme_root' in config.system['paths']:
            module_dirs.append(os.path.join(config.system['paths']['theme_root'], config.system['paths']['module_dir']))
        for module in node.attrib['modules'].split():
            # try to locate the module directory
            module_location = None
            for module_dir in module_dirs:
                module_subdir = os.path.join(module_dir, module)
                if os.path.isdir(module_subdir):
                    log.message('TRACE', 'Found module ' + module + ' in ' + module_dir)
                    module_location = module_dir
                    env.loader.searchpath.append(module_subdir)
                    break
            else:
                log.message('ERROR', 'Cannot find module ' + module)

            # if it exists, add module style sheet to the styles list
            for extension, attribute in [('css', 'styles'), ('js', 'scripts')]:
                file_path =  os.path.join(module, module + '.' + extension)
                if os.path.exists(os.path.join(module_location, file_path)):
                    log.message('TRACE', 'Configuring ' + attribute + ' for module ' + module)
                    if attribute not in node.attrib:
                        node.attrib[attribute] = ''
                    else:
                        node.attrib[attribute] += ' '
                    node.attrib[attribute] += os.path.join(os.sep, extension, file_path)

    #---------------------------------------------------------------------------

    @classmethod
    def render_node (cls, node, env, variables):

        # A tage name beginning with _ indicates a preprocessor directive, i.e.,
        # something needs to be done with the node before further processing
        if node.tag.startswith('_'):
            if node.tag == '_include':
                if 'file' in node.attrib:
                    include_tree = ET.parse(node.attrib['file'])
                    include_root = include_tree.getroot()
                    for child in include_root:
                        node.append(child)
                else:
                    raise ValueError('_include directive requires a file attribute')
            else:
                raise ValueError('Unrecognized preprocessor directive ' + node.tag)
        
        # If the node has text content, expand variables in that
        # content, and use the result as the node's text. Otherwise,
        # set the text content to the empty string.
        if node.text and node.text.strip():
            content_template = env.from_string(node.text.strip())
            node.text = content_template.render(variables)
        else:
            node.text = ''
            
        # If the node has children, call this method recursively on
        # each child. Concatenate the results from those calls, and
        # append them to the node's text.
        if len(node) > 0:
            for child in node:
                node.text += cls.render_node(child, env, variables) + '\n'
                if child.tail:
                    content_template = env.from_string(child.tail.strip())
                    node.text += content_template.render(variables)

        # Initialize the variables that will be passed to Jinja for rendering
        # the node. We start with whatever variables were passed in, and
        # add a 'this' variable that points to a dict of variables specific
        # to this node. Those include any attributes on the node, as well as
        # a special variable 'this.content' that contains the node text that
        # was set above.
        render_variables = variables.copy()
        render_variables['this'] = { 'content': node.text }
        if node.attrib:
            render_variables['this'].update(node.attrib)

        # Load the template for this node
        if node.tag.startswith('_'):
            template = env.from_string('{{ this.content }}')
        else:
            template = env.get_template(node.tag + '.html')

        # Render the node and return the result
        return template.render(render_variables)
    
    #---------------------------------------------------------------------------

    @classmethod
    def process (cls, tag, source_dir, target_dir, file_stem):

        log.message('TRACE', 'Doing XML expansion')
        # Get the XML source file to be expanded
        xml_root = ET.parse(os.path.join(source_dir, file_stem + '.' + tag)).getroot()
        # We auto-generate a page ID, which is just the name of the directory
        # holding the index.xml file
        page_depth = file_stem.count('/')
        if page_depth == 0:
            page_id = 'home'
        elif page_depth == 1:
            page_id = re.sub(r'/index\Z', '', file_stem)
        else:
            page_id = re.sub(r'\A.+/([^/]+)/index\Z', r'\1', file_stem)
        xml_root.attrib['id'] = page_id
        # Configure the directories to be searched for templates. We
        # add the theme template dir after the local one, so a local
        # template will be found first if there is one
        template_dirs = [os.path.join(config.system['paths']['design_root'], config.system['paths']['template_dir'])] 
        if 'theme_root' in config.system['paths']:
            template_dirs.append(os.path.join(config.system['paths']['theme_root'], config.system['paths']['template_dir']))
        # Initialize Jinja
        env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dirs), trim_blocks = True, lstrip_blocks = True)
        # If there is a modules attribute on the root, configure modules
        if 'modules' in xml_root.attrib:
            log.message('TRACE', 'Configuring modules for ' + file_stem)
            cls.configure_modules(xml_root, env)
        # Register Salal-specific Jinja functions
        custom_jinja_functions.register_functions(env)
        # Do template expansion on the source file
        xml_root.text = cls.render_node(xml_root, env, config.project)
        # Write the expanded file to the target directory
        with open(os.path.join(target_dir, file_stem + '.html'), mode = 'w', encoding = 'utf-8', newline = '\n') as output_fh:
            output_fh.write(xml_root.text)

    #---------------------------------------------------------------------------

handler = XMLHandler
