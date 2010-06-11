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

import optparse
import os
import sys

parser = optparse.OptionParser()
parser.add_option("--start-daemon", help="starts anamnesis daemon", action="store_true", dest="start")
parser.add_option("--stop-daemon", help="stops anamnesis daemon", action="store_true", dest="stop")
parser.add_option("--browser", help="opens anamnesis browser with clipboard history", action="store_true")
parser.add_option("-l", "--list", help="prints the clipboard history last N values", action="store", type="int", dest="n")
parser.add_option("-a", "--add", help="adds a value to the clipboard", action="store", type="string", dest="clip")
parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()

if not options:
	sys.exit()

elif options.start:
	os.system("/usr/local/bin/anamnesis-daemon &")

elif options.stop:
	os.system("killall -9 anamnesis-daemon")

elif options.browser:
	os.system("/usr/local/bin/anamnesis-browser &")

