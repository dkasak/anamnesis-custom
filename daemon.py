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
import atexit, os, signal, sys
import config, db
import logging, logging.handlers

class Daemon:
	def __init__(self):
		self.logger = logging.getLogger('AnamnesisDaemonLogger')
		self.logger.setLevel(logging.DEBUG)
		
		handler = logging.handlers.RotatingFileHandler(config.log_file, maxBytes=40000, backupCount=2)
		
		self.logger.addHandler(handler)
		
	def __atexit_callback(self):
		os.remove(config.pid_file)
	
	def __get_running_process_pid(self):
		
		pid_file = None
		try:
			pid_file = open(config.pid_file, 'r')
			pid = int(pid_file.read().strip())
			os.kill(pid, 0) # make sure exists a process with this pid
		except:
			pid = None
		
		if pid_file:
			pid_file.close()
		
		return pid
	
	def __fork_and_exit_parent(self):
		if os.fork():
			os._exit(0)
	
	def run(self):
		pass
	
	def start(self):
		if self.__get_running_process_pid():
			self.logger.debug("an anamnesis daemon is still running")
			return False
		
		try: 
			self.__fork_and_exit_parent()
			os.chdir("/")
			os.setsid()
			os.umask(0)
			self.__fork_and_exit_parent()
		
		except Exception as exception:
			self.logger.debug("failed to create daemon: %s" % exception)
			return False
		
		atexit.register(self.__atexit_callback)
		
		pid_file = None
		try:
			pid_file = open(config.pid_file,'w+')
			pid_file.write("%d" % os.getpid())
		finally:
			if pid_file:
				pid_file.close()
		
		self.logger.debug("anamnesis daemon started")
		
		# redirect stdin, stdout & stderr to '/dev/null'
		dev_null = os.open("/dev/null", os.O_RDWR)
		os.dup2(dev_null, sys.stdin.fileno())
		os.dup2(dev_null, sys.stdout.fileno())
		os.dup2(dev_null, sys.stderr.fileno())
		
		self.run()
		
		return True
	
	def stop(self):
		pid = self.__get_running_process_pid()
		if pid:
			try:
				os.kill(pid, signal.SIGTERM)
				self.logger.debug("anamnesis daemon stopped")
			except:
				self.logger.debug("cannot kill process from pid: %d" % pid)
		else:
			self.logger.debug("cannot find daemon to be stopped")
		
		try:
			os.remove(config.pid_file)
		except:
			pass

class AnamnesisDaemon(Daemon):
	
	def __init__(self):
		Daemon.__init__(self)
		self.clip_database = db.ClipDatabase()
		self.last_text = ''

	def __clip_callback(self, clipboard, text, data):
		if self.last_text != text:
			self.last_text = text
			self.clip_database.insert_text(text)

	def __owner_change(self, clipboard, event, data=None):
		clipboard.request_text(self.__clip_callback)

	def run(self):
		self.logger.debug("anamnesis daemon started")
		clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)
		clipboard.request_text(self.__clip_callback)
		clipboard.connect("owner-change", self.__owner_change)
		gtk.main()
