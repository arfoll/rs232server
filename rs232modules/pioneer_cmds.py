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
#power
  'poweroff'      : "POWR0   \r",
  'poweron'       : "POWR1   \r",
  'powerstatus'   : "POWR?   \r",
#volume
  'mute'          : "MUTE1   \r",
  'unmute'        : "MUTE2   \r"
}

responses = {
  # power ACK
  "ok"           : "OK",
  "err"          : "ERR"
}
