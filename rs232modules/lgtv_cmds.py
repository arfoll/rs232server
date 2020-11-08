# Copyright (C) 2011-2020 Brendan Le Foll <brendan@fridu.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

commands = {
#volume
  'volumelevel'   : "kf 00 ff",
  'mute'          : "ke 00 00",
  'unmute'        : "ke 00 01",
#power
  'poweroff'      : "ka 00 00",
  'poweron'       : "ka 00 01",
  'powerstatus'   : "ka 00 ff",
# energy saving
  'eneroff'       : "jq 00 00",
  'enermin'       : "jq 00 01",
  'enermed'       : "jq 00 02",
  'enermax'       : "jq 00 03",
  'enerscreenoff' : "jq 00 05",
# backlight
  'backlightoff'  : "mg 00 00",
  'backlightfull' : "mg 00 64",
# input
  'hdmi'          : "xb 00 90",
  'component'     : "xb 00 40"
}

responses = {
  # power ACK
  "off"           : "a 00 OK00x",
  "on"            : "a 01 OK01x"
}
