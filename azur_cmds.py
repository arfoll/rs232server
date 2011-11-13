# Copyright (C) 2011 Brendan Le Foll <brendan@fridu.net>
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

# Values taken from the 340R/540R V3 specification from http://www.cambridgeaudio.com
# Values have been tested by me to work on a Cambridge Audio Azur 340R, but they should
# work equaly for a 540R V3 and possible a 640R/650R
commands = {
  "volup":    "#1,02\r",
  "voldown":  "#1,03\r",
  "mute":     "#1,11,01\r",
  "unmute":   "#1,11,00\r",
  "poweron":  "#1,01,0\r",
  "poweroff": "#1,01,1\r",
  "video1":   "#7,01,2\r",
  "cdaux":    "#7,01,7\r"
}

#TODO: use input array instead of commands array as above in effort
#to make class more generic
input = {
  "video1":   "#7,01,2\r",
  "cdaux":    "#7,01,7\r"
}

