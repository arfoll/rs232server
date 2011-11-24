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
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from ampserver_queue import AmpServerQueue

AMPSERVER_BUS_NAME = 'uk.co.madeo.ampserver'
AMPSERVER_BUS_PATH = '/uk/co/madeo/ampserver'

class AmpService(dbus.service.Object):
    def __init__(self, tty):
      bus_name = dbus.service.BusName(AMPSERVER_BUS_NAME, bus=dbus.SystemBus())
      dbus.service.Object.__init__(self, bus_name, AMPSERVER_BUS_PATH)
      self.queue = AmpServerQueue(tty)

    @dbus.service.method(AMPSERVER_BUS_NAME)
    def mute(self):
      self.queue.add('mute')

    @dbus.service.method(AMPSERVER_BUS_NAME)
    def unmute(self):
      self.queue.add('unmute')

    @dbus.service.method(AMPSERVER_BUS_NAME)
    def poweron(self):
      self.queue.add('poweron')

    @dbus.service.method(AMPSERVER_BUS_NAME)
    def poweroff(self):
      self.queue.add('poweroff')

    @dbus.service.method(AMPSERVER_BUS_NAME, in_signature='i')
    def volumedown(self, db):
      for i in range(0, db):
        self.queue.add('voldown')

    @dbus.service.method(AMPSERVER_BUS_NAME, in_signature='i')
    def volumeup(self, db):
      for i in range(0, db):
        self.queue.add('volup')

    @dbus.service.method(AMPSERVER_BUS_NAME, out_signature='i')
    def getvolume(self):
      self.queue.add('volup', True)
      return int(self.queue.add('voldown', True))

    @dbus.service.method(AMPSERVER_BUS_NAME)
    def setinputvideo1(self):
      self.queue.add('video1')

    @dbus.service.method(AMPSERVER_BUS_NAME)
    def setinputcdaux(self):
      self.queue.add('cdaux')

    @dbus.service.method(AMPSERVER_BUS_NAME, out_signature='s')
    def getsversion(self):
      return self.queue.add('sversion', True)

    @dbus.service.method(AMPSERVER_BUS_NAME, out_signature='s')
    def getpversion(self):
      return self.queue.add('pversion', True)

    @dbus.service.method(AMPSERVER_BUS_NAME)
    def clear(self):
      self.queue.add('clear', True)

    @dbus.service.method(AMPSERVER_BUS_NAME, out_signature='b')
    def check(self):
      return True

