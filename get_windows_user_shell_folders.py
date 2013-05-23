 
def get_windows_user_shell_folders():
    # Routine to grab all the Windows Shell Folder locations from the registry.  If successful, returns dictionary
    # of shell folder locations indexed on Windows keyword for each; otherwise, returns an empty dictionary.
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


