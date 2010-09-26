import config
import pygtk
pygtk.require('2.0')
import gtk

listeners = { "clipboard": [], "primary": [] }

def can_read_from_selection(type):
	return (type == "clipboard" and config.read_from_clipboard) or \
	       (type == "primary" and config.read_from_primary)

def can_write_to_selection(type):
	return (type == "clipboard" and config.write_to_clipboard) or \
	       (type == "primary" and config.write_to_primary)

def notify_listeners(type, text):
	for listener in listeners[type]:
		listener(text)

def add_listener(type, listener):
	listeners[type].append(listener)

def callback_clipboard(clipboard, text, data):
	notify_listeners("clipboard", text)
def callback_primary(clipboard, text, data):
	notify_listeners("primary", text)

def __owner_change_clipboard(clipboard, event, data=None):
	selection["clipboard"].request_text(callback_clipboard)
def __owner_change_primary(clipboard, event, data=None):
	selection["primary"].request_text(callback_primary)

def write_to_selection(type, text):
	if text and can_write_to_selection(type):
		selection[type].set_text(text)
		selection[type].store()

def write(text):
	write_to_selection("primary", text)
	write_to_selection("clipboard", text)

selection = {}

if can_read_from_selection("clipboard") or can_write_to_selection("clipboard"):
	selection["clipboard"] = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)
	selection["clipboard"].request_text(callback_clipboard)
	selection["clipboard"].connect("owner-change", __owner_change_clipboard)

if can_read_from_selection("primary") or can_write_to_selection("primary"):
	selection["primary"] = gtk.clipboard_get(gtk.gdk.SELECTION_PRIMARY)
	selection["primary"].request_text(callback_primary)
	selection["primary"].connect("owner-change", __owner_change_primary)

