#
#  Anamnesis clipboard manager.
#
#  Copyright (C) 2010  Fabio Guerra <fabiowguerra@users.sourceforge.net>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import pygtk
pygtk.require('2.0')
import gtk, gobject
import time

import clipboard
import config
import db

# ----------------------------------------------

clip_database = db.ClipDatabase()

key_escape  = gtk.gdk.keyval_from_name('Escape')
key_up      = gtk.gdk.keyval_from_name('Up')
key_down    = gtk.gdk.keyval_from_name('Down')
key_enter   = gtk.gdk.keyval_from_name('Return')
key_home    = gtk.gdk.keyval_from_name('Home')
key_end     = gtk.gdk.keyval_from_name('End')
key_pgup    = gtk.gdk.keyval_from_name('Page_Up')
key_pgdown  = gtk.gdk.keyval_from_name('Page_Down')

# this class represents a single item in the clipboard history
class Clip:
	def __init__(self, clip):
		self.rowid = clip[0]
		self.text = clip[1]
	
	def get_row_text(self):
		if not self.text:
			return ''
		return ' '.join(self.text[:config.max_rowtext_size].strip().splitlines())

def get_clip(treeview, path):
	model = treeview.get_model()
	iter = model.get_iter(path)
	return model.get_value(iter, 0)

# user chooses the clip, copy to the clipboard and quit
def row_activated(treeview, path, view_column, data=None):
	text = get_clip(treeview, path).text
	clip_database.insert_text(text)
	clipboard.write(text)
	
	# need some time to set the clipboard properly before exitting the application
	window.hide()
	while gtk.events_pending():
		gtk.main_iteration()
	
	time.sleep(0.5)
	
	gtk.main_quit()

# read clipboard history and returns a gtk.ListStore with the history elements
def create_list_model(max_clips, keywords=None):
	list_store = gtk.ListStore(gobject.TYPE_PYOBJECT)
	clips = clip_database.get_clips(max_clips, keywords)
	for clip in clips:
		list_store.append([Clip(clip)])
	return list_store

def cell_data_func(column, cell, model, iter, user_data=None):
	cell.set_property('text', model.get_value(iter, 0).get_row_text())

def exit_callback(widget, event, data=None):
	gtk.main_quit()

# the tooltip shows the clipboard data without removing the line breaks
def query_tooltip(widget, x, y, keyboard_mode, tooltip):
	try:
		path = widget.get_path_at_pos(x, y)[0]
		text = get_clip(widget, path).text
		text = text[:config.max_tooltip_size]
		tooltip.set_text(text)
		widget.set_tooltip_row(tooltip, path)
		# TODO: return True only if the text is not completely visible...
	except:
		return False
	return True

# when a navigation key is pressed change focus to the list, if 'esc' quit,
# otherwise focus the search entry
def key_pressed(widget, event, data=None):
	global treeview
	global search_entry
	
	if event.keyval == key_escape:
		gtk.main_quit()
	elif event.keyval in [key_up, key_down, key_enter, key_pgup, key_pgdown, key_home, key_end]:
		if not treeview.is_focus():
			treeview.grab_focus()
	else:
		if not search_entry.is_focus():
			search_entry.grab_focus()

# updates the clipboard list while editing the search box
def search_changed(editable, data=None):
	keywords = editable.get_text()
	treeview.set_model(create_list_model(config.max_clips, keywords))
	window.resize_children()

#-----------------------------------------

def get_color(color_string):
	return treeview.get_colormap().alloc_color(color_string)

def main():
	global treeview
	global search_entry
	global window
	
	cell_renderer = gtk.CellRendererText()
	cell_renderer.set_property("background", config.list_background)
	cell_renderer.set_property("foreground", config.list_foreground)
	cell_renderer.set_property("width", config.list_width)

	column = gtk.TreeViewColumn()
	column.pack_start(cell_renderer, True)
	column.set_cell_data_func(cell_renderer, cell_data_func)

	model = create_list_model(config.max_clips)

	treeview = gtk.TreeView(model)
	treeview.set_model(model)
	treeview.append_column(column)
	treeview.set_headers_visible(False)
	treeview.set_property('has-tooltip', True)
	treeview.connect('query-tooltip', query_tooltip)
	treeview.connect('row-activated', row_activated)

	treeview_style = treeview.get_style().copy()
	treeview_style.base[gtk.STATE_NORMAL]   = get_color(config.list_background)
	treeview_style.base[gtk.STATE_SELECTED] = get_color(config.list_background_selected)
	treeview_style.fg[gtk.STATE_NORMAL]     = get_color(config.list_foreground)
	treeview_style.fg[gtk.STATE_SELECTED]   = get_color(config.list_foreground_selected)
	treeview.set_style(treeview_style)

	scrolled_window = gtk.ScrolledWindow()
	scrolled_window.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
	scrolled_window.add(treeview)

	search_entry = gtk.Entry()
	search_entry.connect("changed", search_changed)

	vbox = gtk.VBox()
	vbox.pack_start(scrolled_window)
	vbox.pack_start(search_entry, False, False)

	window = gtk.Window(gtk.WINDOW_TOPLEVEL)
	window.add(vbox)
	window.set_default_size(config.window_width, config.window_height)
	window.set_position(gtk.WIN_POS_CENTER)
	window.set_opacity(config.opacity)
	window.set_decorated(False)
	window.connect("delete_event", exit_callback)
	window.connect("focus-out-event", exit_callback)
	window.connect("key-press-event", key_pressed)

	window_style = window.get_style().copy()
	window_style.bg[gtk.STATE_NORMAL] = get_color("#000000")
	window.set_style(window_style)
	window.show_all()

	gtk.main()

if __name__ == '__main__':
	main()
