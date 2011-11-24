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

import gobject
gobject.threads_init()
from dbus import glib
glib.init_threads()
import dbus

AMPSERVER_BUS_NAME = 'uk.co.madeo.ampserver'
AMPSERVER_BUS_PATH = '/uk/co/madeo/ampserver'

class AmpClient:
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

  def vol_up(self, db):
    self.iface.volumeup(db)

  def vol_down(self, db):
    self.iface.volumedown(db)

  def vol_mute(self):
    self.iface.mute()

  def vol_unmute(self):
    self.iface.unmute()

  def power_off(self):
    self.iface.poweroff()

  def power_on(self):
    self.iface.poweron()

  def input_video1(self):
    self.iface.setinputvideo1()

  def input_cdaux(self):
    self.iface.setinputcdaux()

  def get_sversion(self):
    self.iface.clear()
    print self.iface.getsversion()

  def get_pversion(self):
    self.iface.clear()
    print self.iface.getpversion()

  def get_volume(self):
    self.iface.clear()
    print self.iface.getvolume()

