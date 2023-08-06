# This handler just copies the file from the source directory to the target
# directory.
import os.path
import shutil
from salal.core.log import log

class Default:
    
    #---------------------------------------------------------------------------

    @classmethod
    def get_tags (cls):
        return ['copy', 'default']
    
    #---------------------------------------------------------------------------

    @classmethod
    def process (cls, tag, source_dir, target_dir, file_stem):
        log.message('TRACE', 'Copying')
        # the 'copy' extension is just an indicator that we don't apply the
        # normal file handling for this kind of file, so we strip it
        # in the target filename
        if tag == 'copy':
            target_file = file_stem
        else:
            target_file = file_stem + '.' + tag
        shutil.copyfile(os.path.join(source_dir, file_stem + '.' + tag), os.path.join(target_dir, target_file))
    
    #---------------------------------------------------------------------------

handler = Default
