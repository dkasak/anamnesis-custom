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

import clipboard
import pygtk
pygtk.require('2.0')
import gtk
import time

class Clipboard(clipboard.AbstractClipboard):

	def __init__(self):
		clipboard.AbstractClipboard.__init__(self)
		self.selection = {}
		
		# max time to wait after writing to the clipboard
		self.write_timeout = 2
		
		if self.can_read_from_selection("clipboard") or self.can_write_to_selection("clipboard"):
			self.selection["clipboard"] = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)
			self.selection["clipboard"].request_text(self.callback_clipboard)
			self.selection["clipboard"].connect("owner-change", self.__owner_change_clipboard)

		if self.can_read_from_selection("primary") or self.can_write_to_selection("primary"):
			self.selection["primary"] = gtk.clipboard_get(gtk.gdk.SELECTION_PRIMARY)
			self.selection["primary"].request_text(self.callback_primary)
			self.selection["primary"].connect("owner-change", self.__owner_change_primary)

		self.data = {"primary": None, "clipboard": None}

	def callback_clipboard(self, clipboard, text, data):
		self.data["clipboard"] = text
		self.on_data_changed("clipboard", text)

	def callback_primary(self, clipboard, text, data):
		self.data["primary"] = text
		self.on_data_changed("primary", text)

	def __owner_change_clipboard(self, clipboard, event, data=None):
		self.selection["clipboard"].request_text(self.callback_clipboard)
	def __owner_change_primary(self, clipboard, event, data=None):
		self.selection["primary"].request_text(self.callback_primary)

	def write_to_selection(self, type, text):
		if text and self.can_write_to_selection(type):
			self.selection[type].set_text(text)
			self.selection[type].store()
			
			t0 = time.time()
			while self.data[type] != text and time.time() - t0 < self.write_timeout:
				self.__wait_gtk()

	def __wait_gtk(self):
		while gtk.events_pending():
			gtk.main_iteration()
		time.sleep(0.05)

