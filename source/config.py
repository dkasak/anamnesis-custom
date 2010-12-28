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

import os, os.path

from ConfigParser import RawConfigParser
from xdg.BaseDirectory import *

version = "Anamnesis version 1.0.4"

cfg_filename = "anamnesis.cfg"
cfg_subdir = "anamnesis"

config_dir = os.path.join(xdg_config_home, cfg_subdir)
data_dir = os.path.join(xdg_data_home, cfg_subdir)

# try read configuration files from on $XDG_DATA_DIRS and $XDG_CONFIG_HOME

cfg_files = [os.path.join(config_dir, cfg_filename)]

for dir in xdg_data_dirs:
	cfg_files += [os.path.join(os.path.expanduser(dir), cfg_subdir, cfg_filename)]

cfg_files.reverse()

cfg = RawConfigParser()
cfg.read(cfg_files)

section = ""

# search the configuration for the given key, returns the found value if it exists,
# otherwise return the default_value
def get(key, default_value):
	if cfg.has_option(section, key):
		return cfg.get(section, key)
	return default_value

# search an integer value on the configuration file
def getint(key, default_value):
	return int(get(key, default_value))

# search a floating point number on the configuration file
def getfloat(key, default_value):
	return float(get(key, default_value))

# search a boolean value on the configuration file
def getboolean(key, default_value):
	if cfg.has_option(section, key):
		return cfg.getboolean(section, key)
	return default_value

# paths

section = "paths"
database_file = get("database", os.path.join(data_dir, "database")) # database location
pid_file = get("pid", os.path.join(data_dir, "anamnesis.pid")) # pidfile location
log_file = get("log", os.path.join(data_dir, "anamnesis.log")) # log location

# log

section = "log"
log_activated = getboolean("activated", True) # if true, log messages to a file, otherwise does not write logs
log_formatter = get("formatter", "%(asctime)s - %(message)s") # formatter used to write the log messages

# limits for better performance

section = "limits"
max_clips = getint("max_clips", 100) # the browser will show only that number of clips, older clips will be accessible with text search
max_tooltip_size = getint("max_tooltip_size", 6000) # maximum size of a tooltip in characters
max_rowtext_size = getint("max_rowtext_size", 80) # maximum number of characters shown for each clipboard item on the gui
max_history_storage_count = getint("max_history_storage_count", 10000) # maximum number of clips that could be stored, if necessary the oldest clips will be removed

# user interface

section = "ui"

tweak_ui = getboolean("tweak_ui", True)

list_background = get("list_background", "#000000") # bg color for the list of clipboard items
list_foreground = get("list_foreground", "#ffffff") # fg color for the list of clipboard items
list_background_selected = get("list_background_selected", "#200000") # bg color of the selected item
list_foreground_selected = get("list_foreground_selected", "#ffffff") # fg color of the selected item

opacity = getfloat("opacity", 0.9) # opacity of the window, must be between 0 and 1. Choose 1 for no transparency.
hide_window_decoration = getboolean("hide_window_decoration", True) # enable to hide the window title and borders

window_width = getint("window_width", 500) # window width
window_height = getint("window_height", 500) # window height
window_background = get("window_background", "#000000") # window bg color

# clipboard

section = "clipboard"
clipboard_implementation = get("clipboard_implementation", "gtk")
write_to_clipboard = getboolean("write_to_clipboard", True) # enable to write on the clipboard selection
write_to_primary = getboolean("write_to_primary", True) # enable to write on the primary selection

read_from_clipboard = getboolean("read_from_clipboard", True) # enable to read/store values from the clipboard
read_from_primary = getboolean("read_from_primary", False) # enable to read/store values from the primary selection

# database

section = "database"
database_implementation = get("database_implementation", "sqlite3fts") # use sqlite3 with full-text search enabled
cleanup_on_start = getboolean("cleanup_on_start", True) # performs a cleanup when the daemon is started

