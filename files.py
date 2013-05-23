#!/usr/bin/env python

'''
Created on 16.10.2012

@author: lukaz

contains classes: filestat and files  
'''

import os
import sys
from datetime import datetime
from UserDict import UserDict
import error

class filestat(UserDict):
    '''
    Returns file properties of selected file:

    ["is_pgpecnrypted_flag"]        
    ["is_dir_flag"]
    ["is_link_flag"]
    ["is_file_flag"]
    ["path"] = ["name"]
    ["extension"]
    ["size"]
    ["time_accessed"]
    ["time_modified"]
    ["time_created"]
    ["inode_device"]
    ["inode_protection_mode"]
    ["inode_number"]
    ["inode_links_count"]
    ["user_id"]
    ["group_id"]

    Usage examples:
     
        fc = filechosen("/tmp/testfile")
        print fc["encryption_type"]
        print fc["user_id"]        # prints: 'user id' in Linux systems
    
        fc = filechosen("C://temp/testfile.asc")
        print fc["extension"]    # prints file extension: 'asc'

    '''
    def __init__(self,filepath):
        try:
            if os.path.exists(filepath):
                UserDict.__init__(self)
                st = os.stat(filepath)
                self["fullpath"] = filepath
                self["name"] = filepath
                self["size"] = st.st_size
                self["time_accessed"] = datetime.fromtimestamp(st.st_atime).strftime('%Y-%m-%d %H:%M:%S')
                self["time_modified"] = datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                self["time_created"] = datetime.fromtimestamp(st.st_ctime).strftime('%Y-%m-%d %H:%M:%S')            
                self["inode_device"] = st.st_dev
                self["inode_protection_mode"] = st.st_mode
                self["inode_number"] = st.st_ino
                self["inode_links_count"] = st.st_nlink
                self["user_id"] = st.st_uid
                self["group_id"] = st.st_gid
                self["is_dir_flag"] = False
                self["is_file_flag"] = False
                self["is_link_flag"] = False
                self["extension"] = ""
                self["is_gpgencrypted_flag"] = False
    
                if (os.path.isdir((self["fullpath"]))):
                    self["is_dir_flag"] = True
                
                if (os.path.isfile((self["fullpath"]))):
                    self["is_file_flag"] = True
    
                if (os.path.isdir((self["fullpath"]))):
                    self["is_link_flag"] = True
    
                if self["is_file_flag"]:
                    if (open(self["fullpath"], 'r').read()[:27]) == "-----BEGIN PGP MESSAGE-----":
                        self["is_gpgencrypted_flag"] = True
                    self["extension"] = filepath.split(os.extsep)[len(filepath.split(os.extsep))-1]
            else:
                raise IOError
        except IOError:
            error.message(self, "File Error:\n\n%s\n\ndoesn't exist.\n\nTry to specify this file again before all selected files can be processed."%filepath, use_console=True)
            sys.exit(1)

    def printinfo(self):
        for k, v in sorted(self.items()):
            print "%s: %s" % (k,v)

    def dumpinfo(self):
        print self





class files():
    '''
    List of unique selected files 
    with methods providing needed file operations.
    '''
    def __init__(self, output_directory, dir_archive_format, use_ascii_armor):
        self.flist = []
        self.ARCHIVE_FORMAT = dir_archive_format
        self.OUTPUT_DIR = output_directory
        self.ASCII_ARMOR = use_ascii_armor
        
    def unique(self, flist_item):
        '''
        Check if flist_item is unique in flist
        :param flist_item: filestat object contained in flist
        '''
        uniq = False
        
        return uniq

    def add(self, fstat_object):
        '''
        Add next filestat object into flist
        :param flist_item: filestat object contained in flist
        '''
        added = False
        
        return added
    
    def remove(self, flist_item):
        '''
        Removes filestat object appointed by flist_item from flist
        :param flist_item: filestat object contained in flist
        '''
        removed = False
        
        return removed
        
    def lock(self, flist_item):
        '''
        Locks a file appointed by filestat object from flist
        :param flist_item: filestat object contained in flist
        '''
        locked = False
        
        return locked
    
    def unlock(self, flist_item):
        '''
        Unlocks a file appointed by filestat object from flist
        :param flist_item: filestat object contained in flist
        '''
        unlocked = False
        
        return unlocked
    
    def dirzip(self, flist_item, archive_format):
        '''
        Used when directory was selected for encryption. So it must be archived into one file which can be gpg encrypted afterwards.
        :param flist_item:  filestat object contained in flist
        :param archive_format: tgz or zip
        '''
        dir_zipped = False
        
        return dir_zipped
    
    def encrypt(self, flist_item):
        '''
        GPG encryption into self.output_path
        :param flist_item: filestat object contained in flist
        '''
        encrypted = False
        
        return encrypted

    def decrypt(self, flist_item):
        '''
        GPG encryption into self.output_path
        :param flist_item: filestat object contained in flist
        '''
        decrypted = False
        
        return decrypted
    
    
    def shred(self,flist_item):
        '''
        Safely shred file or directory from disk represented by filestat object from flist
        :param flist_item: filestat object contained in flist
        '''
        wipedout = False
        
        return wipedout

#===============================================================================
# When used NOT as a module (for console use / debug / testing)
#===============================================================================
if __name__ == '__main__':
    #===========================================================================
    # Testing files:
    #
    # sys.argv[1]="C:\Temp\radio"  is dir
    # sys.argv[2]="C:\Temp\bookmarks.html" is file
    # sys.argv[3]="C:\lukaz\_DOCS\_SEC\sifrovane_verze_03.03\pas\Lukas-Pas-02.jpg.gpg"  is encrypted file
    #
    #===========================================================================
    
    if (len(sys.argv) < 2):
        print "\nUsage: filestat.py <filename1> <filename2> ... <filenameN> \n"
        sys.exit(1)
        
    counter = 1
    while counter < len(sys.argv):
        fstatdict = filestat(sys.argv[counter])
        fstatdict.printinfo()
        counter = counter + 1
        print "-------------------------------------"
    
sys.exit(0)