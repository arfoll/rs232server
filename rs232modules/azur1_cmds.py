#!/usr/bin/env python2

# Copyright (C) 2018 Brendan Le Foll <brendan@fridu.net>
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

# Values taken from the 340R/540R V3 specification from
# http://www.cambridgeaudio.com Values have been tested by me to work on a
# Cambridge Audio Azur 351R from the 551R guide so I assume they would work on
# that too
commands = {
#volume
  "volup":    "#1,02,000\r",
  "voldown":  "#1,03,000\r",
  "mute":     "#1,11,010\r",
  "unmute":   "#1,11,000\r",
#power
  "poweron":  "#1,01,010\r",
  "poweroff": "#1,01,000\r",
#inputs
  "dvd":      "#2,01,010\r",
  "video1":   "#2,01,020\r",
  "video2":   "#2,01,030\r",
  "cdaux":    "#2,01,040\r",
  "tape":     "#2,01,050\r",
  "tuner":    "#2,01,060\r",
  "tvarc":    "#2,01,070\r",
#surround modes
  "stereo":    "#4,01,000\r",
  "stereosw":  "#4,01,010\r",
#software
  "sversion": "#05,01,00\r",
  "pversion": "#05,02,00\r"
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
  "unknown":      "#11,01\r",
  "wronggrp":     "#11,02\r",
  "wrongdata":    "#11,03\r"
}
