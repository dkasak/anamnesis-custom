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

import browser
import clipboard
import db
import optparse
import os
import sys

import config
import daemon

help = {
  "start" : "starts anamnesis daemon",
  "stop" : "stops anamnesis daemon",
  "restart" : "restarts anamnesis daemon",
  "browser" : "opens anamnesis browser with clipboard history",
  "list" : "prints the clipboard history last N values",
  "filter" : "use keywords to filter the clips to be listed",
  "add" : "adds a value to the clipboard",
  "remove" : "removes the clipboard element with the given id",
  "brief" : "print only a brief version of long clipboard elements",
  "cleanup" : "optimize database and limit the number of elements",
  "quiet" : "don't print status messages to stdout"
}

parser = optparse.OptionParser(version = config.version)
parser.add_option("--start", action="store_true", dest="start", help=help["start"])
parser.add_option("--stop", action="store_true", dest="stop", help=help["stop"])
parser.add_option("--restart", action="store_true", dest="restart", help=help["restart"])
parser.add_option("-b", "--browser", action="store_true", help=help["browser"])
parser.add_option("--cleanup", action="store_true", help=help["cleanup"])
parser.add_option("-l", "--list", action="store", type="int", dest="n", help=help["list"])
parser.add_option("--filter", action="store", type="string", dest="keywords", help=help["filter"])
parser.add_option("-a", "--add", action="store", type="string", dest="clip_to_add", help=help["add"])
parser.add_option("--remove", action="store", type="int", dest="id_to_remove", help=help["remove"])
parser.add_option("--brief", action="store_true", dest="brief", help=help["brief"])

(options, args) = parser.parse_args()

if not options:
	sys.exit()

if options.clip_to_add:
	db.get_instance().insert(options.clip_to_add)
	clipboard.get_instance().write(options.clip_to_add)

elif options.id_to_remove:
	db.get_instance().remove(options.id_to_remove)

elif options.start:
	daemon.AnamnesisDaemon().start()

elif options.stop:
	daemon.AnamnesisDaemon().stop()

elif options.restart:
	anamnesis_daemon = daemon.AnamnesisDaemon()
	anamnesis_daemon.stop()
	anamnesis_daemon.start()

elif options.browser:
	browser.main()

elif options.cleanup:
	print ("Performing database cleanup, this could take some time. Please wait...")
	db.get_instance().cleanup()
	print ("done.")

elif options.n:
	if options.n:
		n = options.n
	else:
		n = 10
	
	print (' id | clip')
	print ('-------------------')
	for clip in db.get_instance().search(n, options.keywords):
		
		if options.brief:
			clip_text = ' '.join(clip[1][:config.max_rowtext_size].strip().splitlines())
		else:
			clip_text = clip[1]
			
		print (clip[0], '|', clip_text)

else:
	parser.print_help()
