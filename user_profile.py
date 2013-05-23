#!/usr/bin/env python

'''
Created on 16.10.2012

@author: lukaz
'''

import os
import sys
import platform
import getpass
import gnupg
import error
from get_windows_user_shell_folders import get_windows_user_shell_folders


class user_profile():
    '''
    Stores and manipulates user related information including GPG keys    
    '''
    gpg_home = ""                       # gnupg user directory ( in windows eg.:c:\Users\lukas.novak\AppData\Roaming\gnupg)
    user_name = ""                      # OS user name
    gpg = None                          # GnuPG class instance
    private_keys = None                 # Private keys list                 
    public_keys = None                  # Public keys list
    
    def __init__(self):
        self.user_name = getpass.getuser()
        self.gpg_home = self.get_gpg_home()
        self.gpg_init()

    def set_gpg_home(self, gpg_homedir):
        '''
        Path for GnuPG user's home directory - manual entry method
        :param gpg_homedir: Directory where users GPG keys are stored. 
                            Based on operating system
        '''
        try:        
            if (os.path.isdir(gpg_homedir)):
                self.gpg_home = gpg_homedir
            else:
                raise IOError
        except IOError:
            error.message(self, "ERROR:\n\nSpecified GnuPG user's home directory: %s doesn't exist." % (gpg_homedir), use_console=True)
            sys.exit(1)
       
    def get_gpg_home(self):
        '''
        Path for GnuPG user's home directory - automaticaly retrieved from environment 
        '''
        gpg_home = ''
        try:
            if  (platform.uname()[0] == 'Linux'):
                gpg_home = os.getenv("HOME") + "/.gnupg"
            if  (platform.uname()[0] == 'Windows'):
                gpg_home = get_windows_user_shell_folders()['AppData'] + "\\gnupg"      
            if gpg_home == '':
                raise IOError       
        except IOError:
            error.message(self, "ERROR:\n\nUser home directory determination failed. OS detection failed.\nPlease use method set_gpg_home", use_console=True)
            sys.exit(1)
        try:
            if (os.path.isdir(gpg_home)):
                return gpg_home
            raise IOError
        except IOError:
            error.message(self, "ERROR:\nGnuPG user's home directory:\n%s\n\ndoesn't exist.\nIs GnuPG software installed on your system?" % (gpg_home), use_console=True)
            sys.exit(1)

    def gpg_init(self):
        '''
        Set GnuPG object with user's keys self.gpg_home        
        '''
        self.gpg = gnupg.GPG(gnupghome=self.gpg_home)

        # Flags for key existence check
        keys_publ_missing = False
        keys_priv_missing = False

        if len(self.gpg.list_keys()) > 0:
            self.public_keys = self.gpg.list_keys()
        else:
            keys_publ_missing = True

        if len(self.gpg.list_keys()) > 0:
            self.private_keys = self.gpg.list_keys(True)
        else:
            keys_priv_missing = True

        try:
            if keys_publ_missing and keys_priv_missing:
                raise IOError
        except IOError:
            error.message(self, "ERROR:\n\nNo public or private key(s) found in\n\n%s\n\nfor user: %s\n\nYou can import or create your keys using GnuPG program.     " %(self.gpg_home, self.user_name), use_console=True)
            sys.exit(1)

    def get_public_keys(self):
        '''
        Gets list of only dictionary with public key properties
        '''
        return self.public_keys

    def get_private_keys(self):
        '''
        Gets list of only dictionary with private key properties 
        '''
        return self.private_keys
    



#===============================================================================
# When used NOT as a module (for debug)
#===============================================================================
# if __name__ == '__main__':
#     u = user_profile()
#     combolist1 = []
#     for k in u.private_keys:
#         combolist1.append(k["uids"])
#     for k in u.public_keys:
#         combolist1.append(k["uids"])
#     combolist1.sort()
#     for row in combolist1:
#         print row
    

    