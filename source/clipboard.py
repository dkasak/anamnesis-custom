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

import config

class AbstractClipboard:
	""" This interface is intended to handle all clipboard operations in anamnesis. """

	def __init__(self):
		self.listeners = { "clipboard": [], "primary": [] }
		self.last = { "clipboard": "", "primary": "" }

	def on_data_changed(self, type, text):
		""" This method should be called whenever the data on the clipboard changes. """

		# if the clipboard was erased, restore the last value
		if not text and self.last[type]:
			self.write_to_selection(type, self.last[type])
		else:
			self.last[type] = text

		# notify listeners
		if self.can_read_from_selection(type):
			for listener in self.listeners[type]:
				listener(text)

	def add_listener(self, type, listener):
		""" Adds a listener that will be notified whenever the data on the clipboard changes. """
		self.listeners[type].append(listener)

	def remove_listener(self, type, listener):
		""" Remove a listener that was added in 'add_listener' method. """
		self.listeners[type].remove(listener)

	def write(self, data):
		""" Write data to the clipboard. """
		self.write_to_selection("primary", data)
		self.write_to_selection("clipboard", data)

	def can_read_from_selection(self, type):
		""" Returns true if reading from the given clipboard selection type is enabled """
		return (type == "clipboard" and config.read_from_clipboard) or \
			   (type == "primary" and config.read_from_primary)

	def can_write_to_selection(self, type):
		""" Returns true if writing from the given clipboard selection type is enabled """
		return (type == "clipboard" and config.write_to_clipboard) or \
			   (type == "primary" and config.write_to_primary)

	def write_to_selection(self, type, data):
		""" Writes the given data to the specified clipboard selection type. """
		raise NotImplementedError


clipboard = None

def get_instance():
	global clipboard
	if not clipboard:
		clipboard = __import__("clipboard_" + config.clipboard_implementation).Clipboard()
	return clipboard

