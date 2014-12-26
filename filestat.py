'''
Created on Nov 4, 2014

@author: lukaz
'''

#from _ast import TryExcept
from collections import UserDict
#import gnupg
import os
import sys

from logger import log


class FileStat(UserDict):
    '''
    Returns file properties of selected file:
 
    Usage examples:
     
                        fc = filestat('/tmp/testfile')
                        print(fc['user_id'])       
                    
                        fc = filestat('C://temp/testfile.asc')
                        print(fc['extension'])

    '''
    def __init__(self, filepath):
        
        try:
            if os.path.exists(filepath):
                UserDict.__init__(self)
                st = os.stat(filepath)
                self['id'] = id(self)
                self['full_name'] = filepath
                self['size'] = st.st_size
                self['sizeh'] = approximate_size(st.st_size,a_kilobyte_is_1024_bytes=False)
                self['user_id'] = st.st_uid
                self['group_id'] = st.st_gid
                self['is_directory'] = False
                self['is_file'] = False
                self['is_link'] = False
                self['extension'] = ''
                if (os.path.isdir((self['full_name']))):
                    self['is_directory'] = True
                if (os.path.isfile((self['full_name']))):
                    self['is_file'] = True
                if (os.path.isdir((self['full_name']))):
                    self['is_link'] = True
                if self['is_file']:
                    self['extension'] = filepath.split(os.extsep)[len(filepath.split(os.extsep))-1]
            else:
                raise IOError
        except IOError:
            log.error("File {0} doesn't exist.".format(filepath))
            sys.exit(1)

            
    def is_gpg_encrypted(self):
        ''' Returns boolean flag checking if file is GPG encrypted '''
        identification_phase_1 = False
        identification_phase_2 = False
        GPG_identification_string_1 = "-----BEGIN PGP MESSAGE-----"
        GPG_identification_string_2 = "-----END PGP MESSAGE-----"
        
        try:
            fhandle=open(self["full_name"],"r")
            while True:
                lhandle=fhandle.readline()
                if GPG_identification_string_1 in lhandle:
                    identification_phase_1 = True
                if GPG_identification_string_2 in lhandle:
                    identification_phase_2 = True
                if not lhandle:
                    break
            fhandle.close()
        except IOError:
            log.error("Can't read file {0} ".format(self["full_name"]))
        return (identification_phase_1 and identification_phase_2)
        

    def info(self):
        ''' Prints file details dictionary '''
        print(2*"\n")
        for k,v in sorted (self.items()):
            print("{0}: {1}".format(k,v))
        print("\n")




def approximate_size(size, a_kilobyte_is_1024_bytes=True):
    '''Convert a file size to human-readable form.

    Keyword arguments:
    size -- file size in bytes
    a_kilobyte_is_1024_bytes -- if True (default), use multiples of 1024
                                if False, use multiples of 1000

    Returns: string

    # This function is under a
    #
    # Copyright (c) 2009, Mark Pilgrim, All rights reserved.
    # 
    # Redistribution and use in source and binary forms, with or without modification,
    # are permitted provided that the following conditions are met:
    # 
    # * Redistributions of source code must retain the above copyright notice,
    #   this list of conditions and the following disclaimer.
    # * Redistributions in binary form must reproduce the above copyright notice,
    #   this list of conditions and the following disclaimer in the documentation
    #   and/or other materials provided with the distribution.
    # 
    # THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS IS'
    # AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    # IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
    # ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
    # LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
    # CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
    # SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
    # INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
    # CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    # ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    # POSSIBILITY OF SUCH DAMAGE.


    '''
    SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
                1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']}
    
    if size < 0:
        raise ValueError('number must be non-negative')

    multiple = 1024 if a_kilobyte_is_1024_bytes else 1000
    for suffix in SUFFIXES[multiple]:
        size /= multiple
        if size < multiple:
            return '{0:.1f} {1}'.format(size, suffix)

    raise ValueError('number too large')


if __name__ == '__main__':

    
    
    fc=FileStat('./test3/f2')
    fc.info()
    print("Test if it's GPG encrypted file: {0}".format(fc.is_gpg_encrypted()))
    
    fc=FileStat('./test3/f3.asc')
    fc.info()
    print("Test if it's GPG encrypted file: {0}".format(fc.is_gpg_encrypted()))

    
    exit(0)
        
   
    