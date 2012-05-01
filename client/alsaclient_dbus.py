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

RS232SERVER_BUS_NAME = 'uk.co.madeo.rs232server'
ALSASERVICE_IFACE = 'uk.co.madeo.rs232server.alsa'
ALSASERVICE_OBJ_PATH = '/uk/co/madeo/rs232server/alsa'

class AlsaClient:
  def __init__(self):
    try:
      bus = dbus.SystemBus()
      rs232 = bus.get_object(RS232SERVER_BUS_NAME, ALSASERVICE_OBJ_PATH)
      self.iface = dbus.Interface(rs232, dbus_interface=ALSASERVICE_IFACE)
    except:
      print sys.exc_info()
      print "could not connect to " + RS232SERVER_BUS_NAME
      exit(1)

  def set_headphone_modeon(self):
    self.iface.headphonemodeon()

  def set_headphone_modeoff(self):
    self.iface.headphonemodeoff()

