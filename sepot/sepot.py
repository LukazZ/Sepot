#!/usr/bin/env python

#===============================================================================
# Started on 14.11.2012
# 
# @author: lukas.novak.ext
#
##
##  GPG - encrypting file. Sender uses recipient's public key to encrypt data
##      - decrypting file. Recipient must use his private key to decrypt data
##
#===============================================================================

import logging
import error
#import files
import gc
import gtk
import pygtk
pygtk.require('2.0')
import sys
import urllib
from user_profile import user_profile
from avail import lineadd 
from avail import linesget
from avail import linesset
gc.enable()

log = logging.getLogger('sepot')
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

filelog = logging.FileHandler('sepot.log')
filelog.setLevel(logging.DEBUG)
filelog.setFormatter(formatter)
log.addHandler(filelog)

cons = logging.StreamHandler()
cons.setLevel(logging.DEBUG)
log.addHandler(cons)

log.info("Program starting")


class gpgui(object):
    ''' 
    Main application class 
    '''
    
    # User object holds user details and his private and public keys
    user = user_profile()

    # DND Event local accomodation
    event_ACTION_COPY = gtk.gdk.ACTION_COPY             # @UndefinedVariable
    event_ACTION_DEFAULT = gtk.gdk.ACTION_DEFAULT       # @UndefinedVariable
    event_NOTHING = gtk.gdk.NOTHING                     # @UndefinedVariable
    
    glade_GtkBuilder_XML = "GUI.glade"
    # GTK objects 
    builder = gtk.Builder()
    try:
        builder.add_from_file(glade_GtkBuilder_XML)
    except:
        error.message(object, msg=("ERROR: \"%s\": No such file or directory " % glade_GtkBuilder_XML), use_console=True)
        sys.exit(1)
    
    # GtkBuilder objects mapping
    windowMain = builder.get_object("windowMain")
    windowSettings = builder.get_object("windowSettings")
    windowHelp = builder.get_object("windowHelp")
    fileChooser = builder.get_object("fileChooser")
    textview1 = builder.get_object("textview1")
    vbox2 = builder.get_object("vbox2")
    accellabel1 = builder.get_object("accellabel1")
    checkboxFileChooserHiddenFiles = builder.get_object("checkboxFileChooserHiddenFiles")
    optionsFrame1 = builder.get_object('optionsFrame1')
    optionsFrame2 = builder.get_object('optionsFrame2')
    optionsFrame3 = builder.get_object('optionsFrame3')
    optionsFrame4 = builder.get_object('optionsFrame4')
    optionsFrame5 = builder.get_object('optionsFrame5')
    optionsFrame6 = builder.get_object('optionsFrame6')
    settingsOutputDirectoryChooser = builder.get_object('settingsOutputDirectoryChooser')
    radioButtonSettings05 = builder.get_object('radioButtonSettings05')
    radioButtonSettings06 = builder.get_object('radioButtonSettings06')


    def on_radioButtonSettings05_toggled(self, widget, data=None):
        if data == "radioButtonSettings05" and widget.get_active:
            log.info("radioButtonSettings05 vybrano")
            self.settingsOutputDirectoryChooser.enabled = False
        else:
            log.info("radioButtonSettings06 vybrano")
            self.settingsOutputDirectoryChooser.enabled = True
            

        
    
    def on_buttonSettingsSave_clicked(self, widget):
        log.info("->>> SAVE SETTINGS NOW!")
        self.windowSettings.hide()

    def on_buttonSettingsClose_clicked(self, widget):
        self.windowSettings.hide()

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

    def on_textview1_drag_data_received(self,widget, context, x, y, selection, target_type, timestamp):
        '''
        On Drop event
        '''
        
        log.debug("selection.get_format:    %s" %selection.get_format)
        log.debug("selection.get_length:    %s" %selection.get_length)
        log.debug("selection.get_pixbuf:    %s" %selection.get_pixbuf)
        log.debug("selection.get_selection:    %s" %selection.get_selection)
        log.debug("selection.get_target:    %s" %selection.get_target)
        log.debug("selection.get_targets:    %s" %selection.get_targets)
        log.debug("selection.get_text:    %s" %selection.get_text)
        log.debug("selection.get_uris:    %s" %selection.get_uris)
        log.debug("selection.target:    %s" %selection.target)
        log.debug("selection.targets_include_image:    %s" %selection.targets_include_image)
        log.debug("selection.targets_include_rich_text:    %s" %selection.targets_include_rich_text)
        log.debug("selection.targets_include_text:    %s" %selection.targets_include_text)
        log.debug("selection.targets_include_uri:    %s" %selection.targets_include_uri)
        log.debug("selection.tree_get_row_drag_data:    %s" %selection.tree_get_row_drag_data)
        log.debug("selection.tree_set_row_drag_data:    %s" %selection.tree_set_row_drag_data)
        log.debug("selection.type:    %s" %selection.type)
        log.debug("selection.data:    %s" %selection.data)
        uri = selection.data.strip('\r\n\x00')
        log.info("uri: %s " % uri)
        
        uri_splitted = uri.split() # More than one file dropped
        log.info("uri splitted: %s " % uri_splitted)
        for uri in uri_splitted:
            path = self.get_file_path_from_dnd_dropped_uri(uri)
            # Add all to textview (to be sorted and made unique later)
            lineadd(self.textview1,"%s" % path,False)
            
        # Get all lines from textview
        list_old = linesget(self.textview1)        
        # Making unique list from list_old in case already file present is about to be add again
        list_new = []
        for i in sorted(list_old):
            if not i in list_new:
                list_new.append(i)

        linesset(self.textview1,list_new)

    
    def on_windowMain_destroy(self, data=None):
        """ on_windowMain_destroy """
        gtk.main_quit()
        log.info("Program terminating")
        exit(0)
        
    def on_menuFileExit_activate(self, widget):
        """ on_menuFileExit_activate """
        self.on_windowMain_destroy()

    def on_buttonProcess_clicked(self, widget):
        """ on_buttonProcess_clicked """
        self.textview1.place_cursor_onscreen()
        #self.textview1.scroll_to_iter(self.textview1.get_buffer().get_end_iter())
        log.debug("Pocet soubory %s" %(len(linesget(self.textview1))) )
    
    def on_combobox1_change(self, widget):
        """ on_combobox1_change - PGP Key selection changes """
        log.info("Action selected - %s" % self.combobox1.get_active_text() )

    def on_menuOptionSettings_activate(self, widget):
        """ Activate settings window"""
        self.windowSettings.show()
        
        

    def on_menuHelpAbout_activate(self, widget):
        """ on_menuHelpAbout_activate """
        self.windowHelp.show()

    def on_buttonAboutClose_clicked(self, widget):
        """ on_buttonAboutClose_clicked """
        self.windowHelp.hide()
        
    def on_menuFileSelect_activate(self,widget):
        """on_menuFileSelect_activate"""
        self.fileChooser.show()
        
        
    def on_fileChooser_delete_event(self, widget, event, data=None):
        """on_fileChooser_delete_event"""
        self.fileChooser.hide()
        return True

    def on_buttonFileChooserClose_clicked(self, widget):
        """ on_buttonFileChooserClose_activate """
        self.on_fileChooser_delete_event(self, widget, self.event_NOTHING)
        return True
                   
    def on_buttonFileChooserOK_clicked(self, widget):
        # Get all lines from textview and merge it with newfiles from filechooser
        list_old = linesget(self.textview1) + self.fileChooser.get_filenames()        
        # Remove initial empty line from textview's buffer 
        if list_old[0] == '':
            list_old = list_old[1:]
        # Add only unique items only into list_new
        list_new = []
        for i in sorted(list_old):
            if not i in list_new:
                list_new.append(i)
        # Refresh textview
        linesset(self.textview1,list_new)
        self.fileChooser.hide()
        return True

    def on_windowSettings_delete_event(self, widget, event, data=None):
        """
        on_windowSettings_delete_event
        If you return FALSE in the "delete_event" signal handler, GTK will emit the "destroy" signal. Returning TRUE means
        you don't want the window to be destroyed. This is useful for popping up 'are you sure you want to quit?' type dialogs
        """
        self.windowSettings.hide()
        return True

    def on_windowHelp_delete_event(self, widget, event, data=None):   
        """
        on_windowHelp_delete_event
        """
        self.windowHelp.hide()
        return True

        
    #===========================================================================
    # GUI initialization
    #===========================================================================
    def __init__(self):
         
        # Connect signals
        self.builder.connect_signals(self)

        # Set initial properties
        self.filename = None
        self.about_dialog = None
        self.radioButtonSettings05.connect("toggled", self.on_radioButtonSettings05_toggled, "radioButtonSettings05")
        self.radioButtonSettings06.connect("toggled", self.on_radioButtonSettings05_toggled, "radioButtonSettings06")
        self.combobox1 = gtk.combo_box_new_text()
        self.combobox1.connect("changed", self.on_combobox1_change)

        
        # Adding dynamically created objects to builder
        combolist1 = []

        for k in self.user.private_keys:
            combolist1.append("Decript with private key: %s"%k["uids"][0])
            log.info("Found private key: %s"%k["uids"][0])
        
        for k in self.user.public_keys:
            combolist1.append("Encrypt with public key: %s"%k["uids"][0])
            log.info("Found public key: %s"%k["uids"][0])
        
        combolist1.sort()
        
        for row in combolist1:
            self.combobox1.append_text(row)
        
        self.combobox1.set_active(0) #selected item
        self.accellabel1.set_accel_widget(self.combobox1)
        self.combobox1.show()

        # Put combobox1 into hbox2  
        self.vbox2.pack_start(self.combobox1, expand=True, fill=True, padding=4)

        TARGET_TYPE_URI_LIST = 80
        dnd_list = [ ( 'text/uri-list', 0, TARGET_TYPE_URI_LIST ) ]
        #self.textview1.connect('drag_data_received', self.on_textview1_drag_data_received)
        self.textview1.drag_dest_set( gtk.DEST_DEFAULT_MOTION |
                          gtk.DEST_DEFAULT_HIGHLIGHT | gtk.DEST_DEFAULT_DROP,
                          dnd_list, self.event_ACTION_DEFAULT)
       
    def main(self):
        self.windowMain.show()
        gtk.main()

if __name__ == "__main__":
    gui = gpgui()
    gui.main()     