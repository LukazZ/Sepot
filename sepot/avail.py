'''
Created on 21.5.2013

@author: lukas.novak.ext

small avail functions
'''

def lineadd(TV,text,clear_first):
    '''
    Adds new line of text into TextViewer object     
    :param TV: TextView widget
    :param text: String to be added
    :param clear_first: Erase current content before adding text
    '''
    atbuffer = TV.get_buffer()
    atiter = atbuffer.get_iter_at_mark(atbuffer.get_insert())
    if clear_first:
        atbuffer.set_text(text)
    else:
        atbuffer.insert(atiter,"%s\n"%text)   # use "\n" for newlines        

def linesget(TV):
    '''
    Get all lines from textview into list_old
    :param TV: gtk.textview
    '''
    buff = TV.get_buffer()
    text_old = buff.get_text(buff.get_start_iter(), buff.get_end_iter(), include_hidden_chars=True)
    return text_old.split()

def linesset(TV, list_new):
    '''
    Sets new sorted text for TV
    :param TV: gtk.textview
    :list_new is list of lines (strings) to be displayed in TV
    '''
    # Display list_new in textview
    text_new = ""
    for i in sorted(list_new):
        text_new = text_new + i + "\n"
    lineadd(TV,text_new,True)
    
    

def get_windows_user_shell_folders():
    '''
    Function determines Windows Shell Folder locations from the registry.  If successful, returns dictionary
    of shell folder locations indexed on Windows keyword for each; otherwise, returns an empty dictionary.
    '''
    import _winreg
    return_dict = {}
 
    # First open the registry hive
    try:
        Hive = _winreg.ConnectRegistry(None, _winreg.HKEY_CURRENT_USER)
    except WindowsError:
        print "Can't connect to registry hive HKEY_CURRENT_USER."
        return return_dict
 
    # Then open the registry key where Windows stores the Shell Folder locations
    try:
        Key = _winreg.OpenKey(Hive, "Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
    except WindowsError:
        print "Can't open registry key Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders."
        _winreg.CloseKey(Hive)
        return return_dict
 
    # Nothing failed above, so enumerate through all the Shell Folder values and return in a dictionary
    # This relies on error at end of 
    try:
        #i = 0
        #while 1:
        for i in range(0, _winreg.QueryInfoKey(Key)[1]):
            name, value, val_type = _winreg.EnumValue(Key, i)
            return_dict[name] = value
            i += 1
        _winreg.CloseKey(Key)                           # Only use with for loop
        _winreg.CloseKey(Hive)                          # Only use with for loop
        return return_dict                              # Only use with for loop
    except WindowsError:
        # In case of failure before read completed, don't return partial results
        _winreg.CloseKey(Key)
        _winreg.CloseKey(Hive)
        return {}


def main():
    pass

if __name__ == '__main__':
    main()

    
