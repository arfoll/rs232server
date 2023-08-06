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

# Values taken from the 340R/540R V3 specification from http://www.cambridgeaudio.com
# Values have been tested by me to work on a Cambridge Audio Azur 340R & 640R, but they should
# work equaly for a 540R V3 and 650R/551R
commands = {
#volume
  "volup":    b"#1,02,\r",
  "voldown":  b"#1,03,\r",
  "mute":     b"#1,11,01\r",
  "unmute":   b"#1,11,00\r",
#power
  "poweron":  b"#1,01,1\r",
  "poweroff": b"#1,01,0\r",
#inputs
  "dvd":      b"#2,01,1\r",
  "video1":   b"#2,01,2\r",
  "tuner":    b"#2,01,3\r",
  "video2":   b"#2,01,4\r",
  "video3":   b"#2,01,5\r",
  "tape":     b"#2,01,6\r",
  "cdaux":    b"#2,01,7\r",
  "digital":  b"#2,04,01\r",
  "analog":   b"#2,04,00\r",
#OSD
  "osdon":    b"#1,13,\r",
  "osdoff":   b"#1,14,\r",
  "osdup":    b"#1,15,\r",
  "osddown":  b"#1,16,\r",
  "osdleft":  b"#1,17,\r",
  "osdright": b"#1,18,\r",
  "osdenter": b"#1,19,\r",
#treble/bass
  "trebleup":   b"#1,06,\r",
  "trebledown": b"#1,07,\r",
  "bassup":     b"#1,04,\r",
  "bassdown":   b"#1,05,\r",
#drc
  "drcoff":    b"#1,12,00\r",
  "drc1":      b"#1,12,01\r",
  "drc2":      b"#1,12,02\r",
  "drc3":      b"#1,12,03\r",
  "drc4":      b"#1,12,04\r",
#surround modes
  "stereo":    b"#4,01,00\r",
  "stereosw":  b"#4,01,01\r",
  "pl2":       b"#4,02,\r",
  "dd/dts":    b"#4,03,\r",
  "pl2mode":   b"#4,04,\r",
  "dd/dtsmode":b"#4,05,\r",
#software
  "sversion": b"#5,01,\r",
  "pversion": b"#5,02,\r"
}

# dictionary of headers for replies so they can be removed
replies = {
#software
  "sversion": b"#10,01,",
  "pversion": b"#10,02,",
#volume
  "voldown":  b"#6,03,",
  "volup":    b"#6,02,"
}

errors = {
  "off":      b"#11,01\r",
  "wronggrp": b"#11,02\r",
  "wrongopt": b"#11,03\r"
}
