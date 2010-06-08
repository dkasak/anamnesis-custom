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

last_text = ''

def clip_callback(clipboard, text, data):
	global last_text
	if text != last_text:
		last_text = text
		db.insert_text(text)

def update_clipboard():
	clipboard.request_text(clip_callback)
	return True

clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)
clipboard.request_text(clip_callback)

gobject.timeout_add(1000, update_clipboard)

gtk.main()
