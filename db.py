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
import os
import sqlite3

class ClipDatabase:
	
	def __init__(self):
		# try to create configuration directory if it does not exists yet
		try:
			os.mkdir(config.config_dir)
		except OSError:
			pass
		
		# try to create database if it does not exists yet
		try:
			open(config.database_file, 'a').close()
		except Exception as exception:
			print "[anamnesis] error on initialization:", exception
			return
		
		# try to connect to the database
		try:
			self.connection = sqlite3.connect(config.database_file)
			self.cursor = self.connection.cursor()
			self.cursor.execute("CREATE VIRTUAL TABLE clips USING fts3(text)")
			self.connection.commit()
		except:
			pass

	def insert_text(self, text):
		if not text or text == self.get_last_clip():
			return
		
		self.remove_clip_from_text(text)
		self.cursor.execute("INSERT INTO clips VALUES (?)", (str(text),))
		self.connection.commit()

	def remove_clip_from_text(self, text):
		if text:
			self.cursor.execute('DELETE FROM clips WHERE text = ?', (str(text),))
			self.connection.commit()

	def get_last_clip(self):
		try:
			return self.get_clips(1)[0]
		except:
			return None

	def get_clips(self, n, keywords=None):
		if keywords:
			match = "* ".join(keywords.split(' ')) + "*"
			self.cursor.execute('SELECT rowid, text FROM clips WHERE text MATCH (?) ORDER BY rowid DESC LIMIT ?', (match,n))
		else:
			self.cursor.execute('SELECT rowid, text FROM clips ORDER BY rowid DESC LIMIT ?', (n,))

		return [row for row in self.cursor]

