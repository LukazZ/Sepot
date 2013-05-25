'''
Created on 25.5.2013

@author: lukas.novak.ext
'''
help('gnupg')

import sys
import os
import platform
import gnupg
import error
from avail import get_windows_user_shell_folders

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



gnupghome =get_gpg_home
print gnupghome
gpg = gnupg.GPG(gnupghome)


