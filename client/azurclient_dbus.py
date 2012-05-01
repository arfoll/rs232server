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
import error_codes

RS232SERVER_BUS_NAME = 'uk.co.madeo.rs232server'
AZURSERVICE_IFACE = 'uk.co.madeo.rs232server.azur'
AZURSERVICE_OBJ_PATH = '/uk/co/madeo/rs232server/azur'

class AzurClient:
  def __init__(self):
    try:
      bus = dbus.SystemBus()
      rs232 = bus.get_object(RS232SERVER_BUS_NAME, AZURSERVICE_OBJ_PATH)
      self.iface = dbus.Interface(rs232, dbus_interface=AZURSERVICE_IFACE)
    except:
      print sys.exc_info()
      print "could not connect to " + RS232SERVER_BUS_NAME
      exit(1)

  def printValOrError(self, val):
    try:
      return error_codes.codes[int(val)]
    except:
      return val

  def vol_up(self, db=1):
    self.iface.volumeup(db)

  def vol_down(self, db=1):
    self.iface.volumedown(db)

  def mute(self):
    self.iface.mute()

  def unmute(self):
    self.iface.unmute()

  def power_off(self):
    self.iface.poweroff()

  def power_on(self):
    self.iface.poweron()

  def input_video1(self):
    self.iface.setinputvideo1()

  def input_video2(self):
    self.iface.setinputvideo2()

  def input_video3(self):
    self.iface.setinputvideo3()

  def input_cdaux(self):
    self.iface.setinputcdaux()

  def get_sversion(self):
    self.iface.clear()
    val = self.iface.getsversion()
    print self.printValOrError(val) 

  def get_pversion(self):
    self.iface.clear()
    val = self.iface.getpversion()
    print self.printValOrError(val)

  def get_volume(self):
    self.iface.clear()
    val = self.iface.getvolume()
    print self.printValOrError(val)

