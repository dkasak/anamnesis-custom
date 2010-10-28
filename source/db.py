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

class IClipboardDatabase:

	def insert(self, data):
		""" Inserts a data to the top of the database, search and remove any duplicates. """
		raise NotImplementedError

	def move_up(self, id, data):
		""" Calls remove(id) and insert data to the top of the database.
            Given data must correspond to the given id. """
		raise NotImplementedError

	def remove(self, id):
		""" Remove the clipboard item with the given id"""
		raise NotImplementedError

	def search(self, n, keywords=None):
		""" Returns the n last inserted clipboard items, filter the search with the given list of keywords"""
		raise NotImplementedError

	def cleanup(self):
		""" Perform a cleanup on the database, and make sure the database size is less than 'config.max_history_storage_count'"""
		raise NotImplementedError

db = None

def get_instance():
	global db
	if not db:
		db = __import__("db_" + config.database_implementation).ClipboardDatabase()
	return db

