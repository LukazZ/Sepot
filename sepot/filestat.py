'''
Created on 25.5.2013

@author: lukas.novak.ext

File protperties class
'''

import os
import sys
#from datetime import datetime
from UserDict import UserDict
import error
import logging
filestat_log = logging.getLogger('sepot.filestat')

class filestat(UserDict):
    '''
    Returns file properties of selected file:

    ['is_pgpecnrypted_flag']        
    ['is_dir_flag']
    ['is_link_flag']
    ['is_file_flag']
    ['path'] = ['full_name']
    ['extension']
    ['size']
    ['time_accessed']
    ['time_modified']
    ['time_created']
    ['inode_device']
    ['inode_protection_mode']
    ['inode_number']
    ['inode_links_count']
    ['user_id']
    ['group_id']

    Usage examples:
     
        fc = filestat('/tmp/testfile')
        print fc['encryption_type']
        print fc['user_id']        # prints: 'user id' in Linux systems
    
        fc = filestat('C://temp/testfile.asc')
        print fc['extension']    # prints file extension: 'asc'

    '''
    def __init__(self,filepath):
        try:
            if os.path.exists(filepath):
                UserDict.__init__(self)
                st = os.stat(filepath)
                self['id'] = id(self)
                #self['fullpath'] = filepath
                self['full_name'] = filepath
                self['size'] = st.st_size
                #self['time_accessed'] = datetime.fromtimestamp(st.st_atime).strftime('%Y-%m-%d %H:%M:%S')
                #self['time_modified'] = datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                #self['time_created'] = datetime.fromtimestamp(st.st_ctime).strftime('%Y-%m-%d %H:%M:%S')            
                #self['inode_device'] = st.st_dev
                #self['inode_protection_mode'] = st.st_mode
                #self['inode_number'] = st.st_ino
                #self['inode_links_count'] = st.st_nlink
                self['user_id'] = st.st_uid
                self['group_id'] = st.st_gid
                self['is_dir_flag'] = False
                self['is_file_flag'] = False
                self['is_link_flag'] = False
                self['extension'] = ''
                self['is_gpgencrypted_flag'] = False
                self.is_gpgencrypted_flag =False
    
                if (os.path.isdir((self['full_name']))):
                    self['is_dir_flag'] = True
                
                if (os.path.isfile((self['full_name']))):
                    self['is_file_flag'] = True
    
                if (os.path.isdir((self['full_name']))):
                    self['is_link_flag'] = True
    
                if self['is_file_flag']:
                    if (open(self['full_name'], 'r').read()[:27]) == '-----BEGIN PGP MESSAGE-----':
                        self['is_gpgencrypted_flag'] = True
                        self.is_gpgencrypted = True
                    self['extension'] = filepath.split(os.extsep)[len(filepath.split(os.extsep))-1]
            else:
                raise IOError
        except IOError:
            error.message(self, "File Error:\n\n%s\n\ndoesn't exist.\n\nTry to specify this file again before all selected files can be processed."%filepath, use_console=True)
            sys.exit(1)

    def printinfo(self):
        for k,v in sorted (self.items()):
            print '%s: %s' % (k,v)

    def dumpinfo(self):
        print self

