'''
Created on 16.10.2012

@author: lukas.novak.ext

Error handling
'''
import logging
error_log = logging.getLogger('sepot.error')


class error(Exception):
    '''
    Base class for exceptions in this module.
    '''

class TransitionError(error):
    '''
    Raised when an operation attempts a state transition that's not
    allowed.

    Attributes:
        prev -- state at beginning of transition
        next -- attempted new state
        msg  -- explanation of why the specific transition is not allowed
    '''
    def __init__(self, prev, next, msg):
        self.prev = prev
        self.next = next
        self.msg = msg

class InputError(error):
    '''
    Exception raised for errors in the input.
    '''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

        
def message(self, msg, use_console):
    '''
    Displays error message in modal gtk.MessageDialog and optionally in console
    :param self: use "object" when calling this method
    :param mes: Message string for display
    :param use_console: when True output will be forked to console too
    '''
    import gtk
    #if use_console: print msg
    error_log.error((msg.replace('\n',' ')).replace('  ',' ').replace('ERROR: ',''))    
    dialog = gtk.MessageDialog(None,
                               gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, msg)
    dialog.set_title("GPGUI Error:")
    dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
    dialog.run()
    dialog.destroy()
