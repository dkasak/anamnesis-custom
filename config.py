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

version = "Anamnesis version 0.0.1"

config_dir = os.getenv("HOME") + "/.anamnesis"

database_file = config_dir + "/database"
pid_file = config_dir + "/anamnesis.pid"
log_file = config_dir + "/anamnesis.log"

list_background = "#000000"
list_foreground = "#ffffff"
list_background_selected = "#200000"
list_foreground_selected = "#ffffff"
list_width = 300

max_clips = 1000
max_tooltip_size = 6000 # maximum possible size of a tooltip in characters

opacity = 0.9

window_width = 450
window_height = 400
