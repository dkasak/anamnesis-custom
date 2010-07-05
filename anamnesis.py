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
  "quiet" : "don't print status messages to stdout"
}

parser = optparse.OptionParser()
parser.add_option("--start", action="store_true", dest="start", help=help["start"])
parser.add_option("--stop", action="store_true", dest="stop", help=help["stop"])
parser.add_option("--restart", action="store_true", dest="restart", help=help["restart"])
parser.add_option("-b", "--browser", action="store_true", help=help["browser"])
parser.add_option("-l", "--list", action="store", type="int", dest="n", help=help["list"])
parser.add_option("--filter", action="store", type="string", dest="keywords", help=help["filter"])
parser.add_option("-a", "--add", action="store", type="string", dest="clip", help=help["add"])

(options, args) = parser.parse_args()

if not options:
	sys.exit()

elif options.start:
	daemon.AnamnesisDaemon().start()

elif options.stop:
	daemon.AnamnesisDaemon().stop()

elif options.restart:
	daemon.AnamnesisDaemon().stop()
	daemon.AnamnesisDaemon().start()

elif options.browser:
	browser.main()

elif options.n:
	if options.n:
		n = options.n
	else:
		n = 10
	
	print ' id | clip'
	print '-------------------'
	for clip in db.ClipDatabase().get_clips(n, options.keywords):
		print clip[0], '|', clip[1]

else:
	parser.print_help()
