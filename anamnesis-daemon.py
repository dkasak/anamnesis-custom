#!/usr/bin/env python
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
import db

clip_database = db.ClipDatabase()

last_text = ''

def clip_callback(clipboard, text, data):
	global last_text
	if text != last_text:
		last_text = text
		clip_database.insert_text(text)

def owner_change(clipboard, event, data=None):
	clipboard.request_text(clip_callback)

clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)
clipboard.request_text(clip_callback)
clipboard.connect("owner-change", owner_change)

gtk.main()
