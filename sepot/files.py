'''
Created on 25.5.2013

@author: lukas.novak.ext

Class for storing selected files properties providing files operations
'''

class files():
    '''
    List of unique selected files represented by instances of filestat class 
    with methods providing needed file operations.
    '''
    def __init__(self, output_directory, dir_archive_format, use_ascii_armor, gpg_key):
        self.flist = []
        self.ARCHIVE_FORMAT = dir_archive_format
        self.OUTPUT_DIR = output_directory
        self.ASCII_ARMOR = use_ascii_armor
            
    def unique(self, flist_item):
        '''
        Check if flist_item is unique in flist
        :param flist_item: filestat object contained in flist
        '''
        return flist_item in self.flist

    def add(self, fstat_object):
        '''
        Add unique filestat object into flist
        :param flist_item: filestat object contained in flist
        '''
        if not self.unique(fstat_object):
            print "files.add => [%s] %s " % (fstat_object['id'],fstat_object['full_name'])
            self.flist.append(fstat_object)
        else:
            print "files.add-> ignoring duplicate file %s" % fstat_object['full_name']
            
    
    def remove(self, flist_item):
        '''
        Removes filestat object appointed by flist_item from flist
        :param flist_item: filestat object contained in flist
        '''
        self.flist.remove(flist_item)
        
        
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
    
    def zipdir(self, flist_item, archive_format):
        '''
        Used when directory was selected for encryption. So it must be archived into one file which can be gpg encrypted afterwards.
        :param flist_item:  filestat object contained in flist
        :param archive_format: tgz or zip
        '''
        pass
    
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
    
    def sort(self):
        self.flist.sort()
    
    def shred(self,flist_item):
        '''
        Safely shred file or directory from disk represented by filestat object from flist
        :param flist_item: filestat object contained in flist
        '''
        wipedout = False
        
        return wipedout

