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
import ConfigParser

version = "Anamnesis version 0.0.1"

home_dir = os.getenv("HOME") + "/.anamnesis"

# configuration parser

cfg_file = home_dir + "/anamnesis.cfg"
cfg = ConfigParser.RawConfigParser()
cfg.read(cfg_file)

section = ""

def get(key, default_value):
	if cfg.has_option(section, key):
		return cfg.get(section, key)
	else:
		return default_value

def getint(key, default_value):
	return int(get(key, default_value))

def getfloat(key, default_value):
	return float(get(key, default_value))

# paths

section = "paths"
database_file = get("database", home_dir + "/database")
pid_file = get("pid", home_dir + "/anamnesis.pid")
log_file = get("log", home_dir + "/anamnesis.log")

# log

section = "log"
log_formatter = get("formatter", "%(asctime)s - %(message)s")

# limits for better performance

section = "limits"
max_clips = getint("max_clips", 1000) # the browser will show only that number of clips, older clips will be accessible with text search
max_tooltip_size = getint("max_tooltip_size", 6000) # maximum size of a tooltip in characters
max_rowtext_size = getint("max_rowtext_size", 80) # maximum size of clipboard preview in the clipboard browser

# user interface

section = "ui"
list_background = get("background", "#000000")
list_foreground = get("foreground", "#ffffff")
list_background_selected = get("background_selected", "#200000")
list_foreground_selected = get("foreground_selected", "#ffffff")
list_width = getint("list_width", 300)

opacity = getfloat("opacity", 0.9)
window_width = getint("window_width", 450)
window_height = getint("window_height", 400)
