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
import gobject
gobject.threads_init()
from dbus import glib
glib.init_threads()
import dbus
import time

AMPSERVER_BUS_NAME = 'uk.co.madeo.ampserver'
AMPSERVER_BUS_PATH = '/uk/co/madeo/ampserver'
DELAY=0.1

class AmpServerCLI:
  def __init__(self):
    try:
      self.bus = dbus.SystemBus()
      self.amp = self.bus.get_object(AMPSERVER_BUS_NAME, AMPSERVER_BUS_PATH)
      self.iface = dbus.Interface(self.amp, AMPSERVER_BUS_NAME)
    except:
      print "could not connect to " + AMPSERVER_BUS_NAME
      help()
      #No point carrying on. exit
      exit(1)

  def vol_amp_up(self, db):
    for i in range(0, db):
      time.sleep(DELAY)
      self.iface.volumeup()

  def vol_amp_down(self, db):
    for i in range(0, db):
      time.sleep(DELAY)
      self.iface.volumedown()

  def vol_amp_mute (self):
    self.iface.mute()

  def vol_amp_unmute (self):
    self.iface.unmute()

  def amp_off (self):
    self.iface.poweroff()

  def amp_on (self):
    self.iface.poweron()

  def amp_set_video1 (self):
    self.iface.setinputvideo1()

  def amp_set_cdaux (self):
    self.iface.setinputcdaux()

def help ():
  print "usage: ampservercli <command>"
  print "volume controls = up/down/mute/unmute (up/down can be followed by an amount in db)"
  print "power controls = on/off"
  print "input controls = video1/cdaux"

if __name__ == "__main__":
  if len(sys.argv) > 1:
    amp = AmpServerCLI()
    if sys.argv[1] == "up":
      if len(sys.argv) > 2 and sys.argv[2].isdigit():
        amp.vol_amp_up (int(sys.argv[2]))
      else:
        amp.vol_amp_up (1)
    elif sys.argv[1] == "down":
      if len(sys.argv) > 2 and sys.argv[2].isdigit():
        amp.vol_amp_down (int(sys.argv[2]))
      else:
        amp.vol_amp_down (1)
    elif sys.argv[1] == "off":
      amp.amp_off ()
    elif sys.argv[1] == "on":
      amp.amp_on ()
    elif sys.argv[1] == "unmute":
      amp.vol_amp_unmute ()
    elif sys.argv[1] == "mute":
      amp.vol_amp_mute ()
    elif sys.argv[1] == "xbmc" or sys.argv[1] == "video1":
      amp.amp_set_video1 ()
    elif sys.argv[1] == "cd" or sys.argv[1] == "cdaux":
      amp.amp_set_cdaux ()
    else:
      help()
  else:
    help()
