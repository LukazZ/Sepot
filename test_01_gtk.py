import sys
print("Python version {0}.{1}.{2} program is started.".format(sys.version_info.major,sys.version_info.minor,sys.version_info.micro)  )

from gi.repository import Gtk

win = Gtk.Window()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
