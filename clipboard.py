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

	def __init__(self):
		self.listeners = { "clipboard": [], "primary": [] }

	def notify_listeners(self, type, text):
		for listener in self.listeners[type]:
			listener(text)

	def add_listener(self, type, listener):
		self.listeners[type].append(listener)

	def write(self, text):
		self.write_to_selection("primary", text)
		self.write_to_selection("clipboard", text)

	def can_read_from_selection(self, type):
		return (type == "clipboard" and config.read_from_clipboard) or \
			   (type == "primary" and config.read_from_primary)

	def can_write_to_selection(self, type):
		return (type == "clipboard" and config.write_to_clipboard) or \
			   (type == "primary" and config.write_to_primary)

	def write_to_selection(self, type, text):
		pass


clipboard = None

def get_instance():
	global clipboard
	if not clipboard:
		clipboard = __import__("clipboard_" + config.clipboard_implementation).Clipboard()
	return clipboard

