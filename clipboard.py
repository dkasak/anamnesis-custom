import pygtk
pygtk.require('2.0')
import gtk

def __clip_callback(clipboard, text, data):
	for listener in listeners:
		listener(text)

def __owner_change(clipboard, event, data=None):
	clipboard.request_text(__clip_callback)

listeners = []

clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)
clipboard.request_text(__clip_callback)
clipboard.connect("owner-change", __owner_change)

primary = gtk.clipboard_get(gtk.gdk.SELECTION_PRIMARY)

def add_listener(listener):
	listeners.append(listener)

def set(text):
	clipboard.set_text(text)
	clipboard.store()
	
	primary.set_text(text)
	primary.store()
