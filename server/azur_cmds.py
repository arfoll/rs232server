# Copyright (C) 2011,2012 Brendan Le Foll <brendan@fridu.net>
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
# work equaly for a 540R V3 and possibly 640R/650R/551R
commands = {
#volume
  "volup":    "#1,02\r",
  "voldown":  "#1,03\r",
  "mute":     "#1,11,01\r",
  "unmute":   "#1,11,00\r",
#power
  "poweron":  "#1,01,1\r",
  "poweroff": "#1,01,0\r",
#inputs
  "dvd":      "#2,01,1\r",
  "video1":   "#2,01,2\r",
  "tuner":    "#2,01,3\r",
  "video2":   "#2,01,4\r",
  "video3":   "#2,01,5\r",
  "tape":     "#2,01,6\r",
  "cdaux":    "#2,01,7\r",
  "digital":  "#2,04,01\r",
  "analog":   "#2,04,00\r",
#OSD
  "osdon":    "#1,13\r",
  "osdoff":   "#1,14\r",
  "osdup":    "#1,15\r",
  "osddown":  "#1,16\r",
  "osdleft":  "#1,17\r",
  "osdright": "#1,18\r",
  "osdenter": "#1,19\r",
#treble/bass
  "trebleup":   "#1,06\r",
  "trebledown": "#1,07\r",
  "bassup":     "#1,04\r",
  "bassdown":   "#1,05\r",
#software
  "sversion": "#5,01,\r",
  "pversion": "#5,02,\r"
}

# dictionary of headers for replies so they can be removed
replies = {
#software
  "sversion": "#10,01,",
  "pversion": "#10,02,",
#volume
  "voldown":  "#6,03,",
  "volup":    "#6,02,"
}

errors = {
  "off":      "#11,01\r",
  "wronggrp": "#11,02\r",
  "wrongopt": "#11,03\r"
}
