#!/usr/bin/python2

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

import sys
from ampclient_dbus import AmpClient

def help ():
  print "usage: ampservercli <command>"
  print "volume controls = up/down/mute/unmute (up/down can be followed by an amount in db)"
  print "power controls = on/off"
  print "input controls = video1/cdaux"
  print "info = sversion/pversion"

if __name__ == "__main__":
  if len(sys.argv) > 1:
    amp = AmpClient()

    if sys.argv[1] == "up":
      if len(sys.argv) > 2 and sys.argv[2].isdigit():
        amp.vol_up(int(sys.argv[2]))
      else:
        amp.vol_up(1)
    elif sys.argv[1] == "down":
      if len(sys.argv) > 2 and sys.argv[2].isdigit():
        amp.vol_down(int(sys.argv[2]))
      else:
        amp.vol_down(1)
    elif sys.argv[1] == "off":
      amp.power_off()
    elif sys.argv[1] == "on":
      amp.power_on()
    elif sys.argv[1] == "unmute":
      amp.vol_unmute()
    elif sys.argv[1] == "mute":
      amp.vol_mute()
    elif sys.argv[1] == "xbmc" or sys.argv[1] == "video1":
      amp.input_video1()
    elif sys.argv[1] == "cd" or sys.argv[1] == "cdaux":
      amp.input_cdaux()
    elif sys.argv[1] == "sversion":
      amp.get_sversion()
    elif sys.argv[1] == "pversion":
      amp.get_pversion()
    elif sys.argv[1] == "volume":
      amp.get_volume()
    else:
      help()
  else:
    help()
