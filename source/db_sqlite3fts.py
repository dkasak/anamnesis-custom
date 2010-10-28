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
import db
import os
import sqlite3

class ClipboardDatabase(db.IClipboardDatabase):
	
	def __init__(self):
		# try to create the data directory if it does not exists yet
		try:
			os.mkdir(config.data_dir)
		except OSError:
			pass
		
		# try to create database if it does not exists yet
		try:
			open(config.database_file, 'a').close()
		except Exception as exception:
			print ("error on database initialization: %s" % str(exception))
			return
		
		# try to connect to the database
		try:
			self.connection = sqlite3.connect(config.database_file)
			self.cursor = self.connection.cursor()
			self.cursor.execute("CREATE VIRTUAL TABLE clips USING fts3(text)")
			self.connection.commit()
		except:
			pass

	def __insert(self, text, id=None):
		# avoid inserting a clip that is already on the clipboard
		if not text or text == self.get_last_clip():
			return

		# do not store duplicates
		if id:
			self.remove(id) # faster
		else:
			self.remove_clip_from_text(text) # slower, need a table full-scan

		self.cursor.execute("INSERT INTO clips VALUES (?)", (unicode(str(text)),))
		self.connection.commit()

	def insert(self, text):
		self.__insert(text)

	def move_up(self, id, text):
		self.__insert(text, id)

	def remove_clip_from_text(self, text):
		if text:
			self.cursor.execute('DELETE FROM clips WHERE text = ?', (unicode(str(text)),))
			self.connection.commit()

	def remove(self, id):
		if id:
			self.cursor.execute('DELETE FROM clips WHERE rowid = ?', (int(id),))
			self.connection.commit()

	def verify_history_size(self):
		try:
			delete_count = self.get_number_of_clips() - config.max_history_storage_count
			
			if delete_count <= 0:
				return
			
			self.cursor.execute('SELECT rowid FROM clips ORDER BY rowid LIMIT ?', (delete_count,))
			
			for row in self.cursor:
				self.cursor.execute('DELETE FROM clips WHERE rowid = ?', (int(row[0]),))
			
			self.connection.commit()
		
		except Exception as exception:
			print ("error verifying the maximum history element count: %s", str(exception))
	
	def cleanup(self):
		self.verify_history_size()
		self.cursor.execute('VACUUM')
		self.connection.commit()

	def get_last_clip(self):
		try:
			return self.search(1)[0]
		except:
			return None

	def search(self, n, keywords=None):
		if keywords:
			match = unicode("* ".join(keywords.split(' ')) + "*")
			self.cursor.execute('SELECT rowid, text FROM clips WHERE text MATCH (?) ORDER BY rowid DESC LIMIT ?', (match,n))
		else:
			self.cursor.execute('SELECT rowid, text FROM clips ORDER BY rowid DESC LIMIT ?', (n,))

		return [row for row in self.cursor]

	def get_number_of_clips(self):
		self.cursor.execute('SELECT count(*) FROM clips')
		return self.cursor.fetchone()[0]

