#!/usr/bin/env python2

# Copyright (C) 2011,2012,2013 Brendan Le Foll <brendan@fridu.net>
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
  'powerstatus'   : "ka 00 ff"
}

responses = {
  "off"           : "a 00 OK00x",
  "on"            : "a 01 OK01x"
}
