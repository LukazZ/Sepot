'''
Created on 16.10.2012

@author: lukas@centrum.cz

Error handling in GUI
'''
from gi.repository import Gtk
from logger import log
        
def ErrorMessage(msg, logit=False):
    '''
    Displays error message in modal gtk.MessageDialog and optionally in console
    :param mes: Message string for display
    :param logit: when True output will be logged by logger
    '''
    if logit:
        log.error(msg)
    
    dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR,
                                        Gtk.ButtonsType.CLOSE, 
                                        "Sepot error")
    dialog.format_secondary_text(msg)
    dialog.run()
    dialog.destroy()   

    exit(1)
