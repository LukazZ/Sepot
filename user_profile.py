# -*- coding: utf-8 -*- 
'''
Created on 11.10.2014

@author: lukaz@centrum.cz

User profile class containing user GPG keys list and use GPG home

Using:
        python-gnupg - A Python wrapper for GnuPG https://github.com/isislovecruft/python-gnupg 

'''

import getpass
import gnupg
import logging
import os
import platform
import sys
import gui_error


user_profile_log = logging.getLogger('sepot.user_profile')

class UserProfile():
    '''
    Holds user related information including GPG keys   
    
    - Automatically determines gpg_home
    - Retrieves current user's public and private keys 
    '''
    gpg = None                          # python-gnupg class instance
    gpg_home = ""                       # gnupg user directory ( in windows eg.:c:\Users\lukas.novak\AppData\Roaming\gnupg)
    user_name = ""                      # OS user name
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
            gui_error.ErrorMessage("Specified GPG user home directory: {0} doesn't exist.".format(gpg_homedir), logit=True)
            sys.exit(1)
       
    def get_gpg_home(self):
        '''
        Path for GnuPG user's home directory 
        '''
        gpg_home = ''
        try:
            if  (platform.uname()[0] == 'Linux'):
                gpg_home = os.getenv("HOME") + "/.gnupg"
            if  (platform.uname()[0] == 'Windows'):
                #TODO
                pass
            if gpg_home == '':
                raise IOError       
        except IOError:
            gui_error.ErrorMessage("User home directory detection failed. OS detection failed.\nPlease use method set_gpg_home", logit=True)
            sys.exit(1)
        try:
            if (os.path.isdir(gpg_home)):
                return gpg_home
            raise IOError
        except IOError:
            gui_error.ErrorMessage("GPG user home directory: {0} doesn't exist. Is the GPG installed on your system?".format(gpg_home), logit=True)
            sys.exit(1)

    def gpg_init(self):
        '''
        Initializate GPG object
        '''
        self.gpg = gnupg.GPG(gnupghome=self.gpg_home)
        #self.gpg.encoding = 'utf-8'
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
            gui_error.ErrorMessage("No public nor private key(s) found in {0} for user: {1} \nPlease import or create your keys using gpg program.".format(self.gpg_home, self.user_name), logit=True)
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
    




def main():
    u = UserProfile()
    msg = "GPG user home directory: %s " % u.gpg_home 
    user_profile_log.info(msg)


    keys = []
    for k in u.private_keys:
        keys.append("Private key: %s" % k["uids"])
    for k in u.public_keys:
        keys.append("Public key: %s" % k["uids"])
    keys.sort()
    for key in keys:
        print(key)


if __name__ == '__main__':
    main()

    
