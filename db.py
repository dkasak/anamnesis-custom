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

import os
import sqlite3

database_filename = os.getenv("HOME") + "/.anamnesis/database"

connection = None
cursor = None

def initialize():
	global connection
	global cursor
	global database_filename

	try:
		open(database_filename, 'a').close()
	except Exception as exception:
		print "[anamnesis] error on initialization:", exception
		return
	try:
		connection = sqlite3.connect(database_filename)
		cursor = connection.cursor()
		cursor.execute("CREATE VIRTUAL TABLE clips USING fts3(text)")
		connection.commit()
	except:
		pass

initialize()

def insert_text(text):
	initialize()
	if not text or text == get_last_clip():
		return
	
	remove_clip_from_text(text)
	cursor.execute("INSERT INTO clips VALUES (?)", (str(text),))
	connection.commit()

def remove_clip_from_text(text):
	initialize()
	if text:
		cursor.execute('DELETE FROM clips WHERE text = ?', (str(text),))
		connection.commit()

def get_last_clip():
	initialize()

	try:
		return get_clips(1)[0]
	except:
		return None

def get_clips(n, keywords):
	initialize()

	if keywords:
		match = "* ".join(keywords.split(' ')) + "*"
		cursor.execute('SELECT rowid, text FROM clips WHERE text MATCH (?) ORDER BY rowid DESC LIMIT ?', (match,n))
	else:
		cursor.execute('SELECT rowid, text FROM clips ORDER BY rowid DESC LIMIT ?', (n,))

	return [row for row in cursor]

