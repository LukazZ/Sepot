'''
Created on 25.5.2013

@author: lukas.novak.ext
'''
help('gnupg')

import gnupg
from user_profile import user_profile

u = user_profile()
print u.gpg_home

gpg = gnupg.GPG(gnupghome=u.gpg_home)


