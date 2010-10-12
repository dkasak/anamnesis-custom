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

import clipboard_gtk
import subprocess

class Clipboard(clipboard_gtk.Clipboard):

	def __init__(self):
		clipboard_gtk.Clipboard.__init__(self)

	def write_to_selection(self, type, text):
		try:
			if text and self.can_write_to_selection(type):
				process = subprocess.Popen(['xclip', '-selection', type], stdin=subprocess.PIPE)
				process.communicate(input=text)
		except:
			print "Error calling xclip to set the clipboard"

