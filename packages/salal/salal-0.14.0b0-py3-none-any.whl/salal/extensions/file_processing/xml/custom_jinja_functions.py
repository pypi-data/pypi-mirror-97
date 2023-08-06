import json
import os.path
import glob
import re
import xml.etree.ElementTree as ET
from salal.core.config import config

#------------------------------------------------------------------------------

def load_config(source):
    with open(os.path.join(config.system['paths']['config_root'], source + '.json')) as config_file_fh:
        variables = json.load(config_file_fh)
        return variables

#------------------------------------------------------------------------------

def page_attributes(page_id):
    # we use 'home' instead of a blank id 
    if page_id == 'home':
        page_path = os.path.join(config.system['paths']['content_root'], 'index.xml')
    else:
        matching_pages = glob.glob(config.system['paths']['content_root'] + '/**/' + page_id + '/index.xml', recursive=True)
        if len(matching_pages) > 1:
            raise ValueError('Non-unique page ID "' + page_id + '"')
        elif len(matching_pages) == 0:
            raise ValueError('Can\'t find page with ID "' + page_id + '"')
        page_path = matching_pages[0]
        
    page_root = ET.parse(page_path).getroot()

    # The rest of this is for two auto-generated attributes: 'link' and
    # 'parent'. Note that 'parent' is in the form of a page ID.
    page_root.attrib['link'] = page_path[7:-9]
    page_depth = page_root.attrib['link'].count('/')
    if page_depth > 3:
        parent_path = re.sub(r'[^/]+/\Z', '', page_root.attrib['link'])
        page_root.attrib['parent'] = re.sub(r'\A/.+/([^/]+)/\Z', r'\1', parent_path)
    elif page_depth == 3:
        page_root.attrib['parent'] = re.sub(r'/([^/]+)/[^/]+/\Z', r'\1', page_root.attrib['link'])
    elif page_depth == 2:
        page_root.attrib['parent'] = 'home'
    elif page_depth == 1:
        page_root.attrib['parent'] = None
    return page_root.attrib
    
#------------------------------------------------------------------------------

def emphasize(text):
    return '<em>' + text + '</em>'

#------------------------------------------------------------------------------

def bold(text):
    return '<b>' + text + '</b>'

#------------------------------------------------------------------------------

def inline_link(url, text, destination="external"):
    if destination == "external":
        anchor = '<a href="' + url + '" target="_blank">' + text + '</a>'
    else:
        anchor = '<a href="' + url + '">' + text + '</a>'
    return anchor

#------------------------------------------------------------------------------

def literal_tag(tag):
    return '<![CDATA[&lt;' + tag + '&gt;]]>'

#------------------------------------------------------------------------------

def register_functions(env):
    env.globals['load_config'] = load_config
    env.globals['page_attributes'] = page_attributes
    env.globals['emphasize'] = emphasize
    env.globals['bold'] = bold
    env.globals['inline_link'] = inline_link
    env.globals['literal_tag'] = literal_tag
    
#------------------------------------------------------------------------------
