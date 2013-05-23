#!/usr/bin/env python

#===============================================================================
# Started on 14.11.2012
# 
# @author: lukas.novak.ext
#
# 
#
#
##
##  GPG - encrypting file. Sender uses recipient's public key to encrypt data
##      - decrypting file. Recipient must use his private key to decrypt data
##
#===============================================================================

import error
#import files
import gc
import gtk
#from idlelib.textView import TextViewer
import os
import pango
import pygtk
pygtk.require('2.0')
import sys
import urllib
from user_profile import user_profile
from avail import addtext

#garbage collector
gc.enable()

class gpgui(object):
    '''
    Main application class
    '''
 
    # GTK objects 
    glade_GtkBuilder_XML = "GUI.glade"
    builder = gtk.Builder()
    try:
        builder.add_from_file(glade_GtkBuilder_XML)
    except:
        error.message(object, msg=("ERROR: \"%s\": No such file or directory " % glade_GtkBuilder_XML), use_console=True)
        sys.exit(1)

    windowMain = builder.get_object("windowMain")
    windowHelp = builder.get_object("windowHelp")
    fileChooser = builder.get_object("fileChooser")
    log = builder.get_object("log")
    textview1 = builder.get_object("textview1")
    vbox2 = builder.get_object("vbox2")
    accellabel1 = builder.get_object("accellabel1")
    
        
    # Events local accomodation
    event_ACTION_COPY = gtk.gdk.ACTION_COPY     # @UndefinedVariable
    event_NOTHING = gtk.gdk.NOTHING             # @UndefinedVariable

    # User object holds user details and his private and public keys
    user = user_profile()

    def get_file_path_from_dnd_dropped_uri(self,uri):
        '''
        Extracts file path from dropped URIs
        Utilizing function from "Drag Open File" snippet by Rich Jones <rich@anomos.info> under GPL     
        '''
        path = ""
        if uri.startswith('file:\\\\\\'): # windows
            path = uri[8:] # 8 is len('file:///')
        elif uri.startswith('file://'): # nautilus, rox
            path = uri[7:] # 7 is len('file://')
        elif uri.startswith('file:'): # xffm
            path = uri[5:] # 5 is len('file:')
    
        path = urllib.url2pathname(path) # escape special chars
        path = path.strip('\r\n\x00') # remove \r\n and NULL
        return path


    # Events signal handlers for GUI
    def on_drag_data_received(self,widget, context, x, y, selection, target_type, timestamp):
        '''
        Utilizing function from "Drag Open File" snippet by Rich Jones <rich@anomos.info> under GPL     
        '''
        uri = selection.data.strip('\r\n\x00')
        uri_splitted = uri.split() # we may have more than one file dropped
        for uri in uri_splitted:
            path = self.get_file_path_from_dnd_dropped_uri(uri)
            if os.path.isfile(path): # is it file?
                # your_open_file_function(path)
                # You might also want to look at the File Chooser snippet
                addtext(self.textview1,path,False)
                # If you actually want to read the data in the file, use
                # data = file(path).read()
    
    def on_windowMain_destroy(self, data=None):
        """ on_windowMain_destroy """
        print "Event: on_windowMain_destroy"
        gtk.main_quit()
        
    def on_menuFileExit_activate(self, widget):
        """ on_menuFileExit_activate """
        print "Event: on_menuFileExit_activate"
        self.on_windowMain_destroy()

    def on_buttonProcess_clicked(self, widget):
        """ on_buttonProcess_clicked """
        print "Event: on_buttonProcess_clicked"

    def on_combobox1_change(self, widget):
        """ on_combobox1_change - PGP Key selection changes """
        print "Event: on_combobox1_change - PGP Key selection changes to %s" % self.combobox1.get_active_text()[7:]

    def on_menuHelpAbout_activate(self, widget):
        """ on_menuHelpAbout_activate """
        print "Event: on_menuHelpAbout_activate"
        self.windowHelp.show()

    def on_buttonAboutClose_clicked(self, widget):
        """ on_buttonAboutClose_clicked """
        print "Event: on_buttonAboutClose_clicked"
        self.windowHelp.hide()
        
    def on_menuFileSelect_activate(self,widget):
        """on_menuFileSelect_activate"""
        print "Event: on_menuFileSelect_activate"
        self.fileChooser.show()
        
    def on_fileChooser_delete_event(self, widget, event, data=None):
        """on_fileChooser_delete_event"""
        print "Event: on_fileChooser_delete_event"
        self.fileChooser.hide()
        return True
    
    def on_buttonFileChooserClose_clicked(self, widget):
        """ on_buttonFileChooserClose_activate """
        print "Event: on_buttonFileChooserClose_activate"
        self.on_fileChooser_delete_event(self, widget, self.event_NOTHING)
        return True
                   
    def on_buttonFileChooserOK_clicked(self, widget):
        newfiles = self.fileChooser.get_filenames()
        print newfiles
        for file in newfiles:
            addtext(self.textview1,file,False)
            
#         filestat modified for self file existence check and can be implemented    
            
        return True
                    
    def on_windowHelp_delete_event(self, widget, event, data=None):
        """
        on_windowHelp_delete_event
        If you return FALSE in the "delete_event" signal handler,
        GTK will emit the "destroy" signal. Returning TRUE means
        you don't want the window to be destroyed.
        This is useful for popping up 'are you sure you want to quit?'
        type dialogs.
        """
        print "Event: on_windowHelp_delete_event"
        self.windowHelp.hide()
        return True

        
    #===========================================================================
    # GUI initialization
    #===========================================================================
    def __init__(self):
         
        # connect signals
        self.builder.connect_signals(self)

        # set initial variables and object properties
        self.filename = None
        self.about_dialog = None
        font = pango.FontDescription("Courier 8")
        self.log.modify_font(font)
        
        # getting user profile data eg. pgp keys
        addtext(self.log,"user.gpg_home: %s"%self.user.gpg_home, False)
        
        # adding dynamically created objects to builder
        combolist1 = []

        for k in self.user.private_keys:
            combolist1.append("Decript with private key: %s"%k["uids"][0])
            addtext(self.log,"(Priv) %s"%k["uids"][0], False)
        
        for k in self.user.public_keys:
            combolist1.append("Encrypt with public key: %s"%k["uids"][0])
            addtext(self.log,"(Publ) %s"%k["uids"][0], False)
        
        combolist1.sort()
        self.combobox1 = gtk.combo_box_new_text()
        self.combobox1.connect("changed", self.on_combobox1_change)
        
        for row in combolist1:
            self.combobox1.append_text(row)
        
        self.combobox1.set_active(0) #selected item
        self.accellabel1.set_accel_widget(self.combobox1)
        self.combobox1.show()

        # Put combobox1 into hbox2  
        self.vbox2.pack_start(self.combobox1, expand=True, fill=True, padding=4)
        

        
        
        gtk.window_set_default_icon_name(gtk.STOCK_DIALOG_AUTHENTICATION)
        TARGET_TYPE_URI_LIST = 80
        dnd_list = [ ( 'text/uri-list', 0, TARGET_TYPE_URI_LIST ) ]
        self.textview1.connect('drag_data_received', self.on_drag_data_received)
        self.textview1.drag_dest_set( gtk.DEST_DEFAULT_MOTION |
                          gtk.DEST_DEFAULT_HIGHLIGHT | gtk.DEST_DEFAULT_DROP,
                          dnd_list, self.event_ACTION_COPY)
       
    def main(self):
        self.windowMain.show()
        gtk.main()



#===============================================================================
# Main Run
#===============================================================================

if __name__ == "__main__":
    gui = gpgui()
    gui.main()     
