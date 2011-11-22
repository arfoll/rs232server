#!/usr/bin/python2

# Copyright (C) 2009 Tom Carlson
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
    def __init__(self):
      bus_name = dbus.service.BusName(AMPSERVER_BUS_NAME, bus=dbus.SystemBus())
      dbus.service.Object.__init__(self, bus_name, AMPSERVER_BUS_PATH)
      self.queue = AmpServerQueue()

    @dbus.service.method(AMPSERVER_BUS_NAME, out_signature='b')
    def mute(self):
      return self.queue.add('mute')

    @dbus.service.method(AMPSERVER_BUS_NAME, out_signature='b')
    def unmute(self):
      return self.queue.add('unmute')

    @dbus.service.method(AMPSERVER_BUS_NAME, out_signature='b')
    def poweron(self):
      return self.queue.add('poweron')

    @dbus.service.method(AMPSERVER_BUS_NAME, out_signature='b')
    def poweroff(self):
      return self.queue.add('poweroff')

    @dbus.service.method(AMPSERVER_BUS_NAME, out_signature='b')
    def volumedown(self):
      return self.queue.add('voldown')

    @dbus.service.method(AMPSERVER_BUS_NAME, out_signature='b')
    def volumeup(self):
      return self.queue.add('volup')

    @dbus.service.method(AMPSERVER_BUS_NAME, out_signature='b')
    def setinputvideo1(self):
      return self.queue.add('video1')

    @dbus.service.method(AMPSERVER_BUS_NAME, out_signature='b')
    def setinputcdaux(self):
      return self.queue.add('cdaux')

    @dbus.service.method(AMPSERVER_BUS_NAME, out_signature='b')
    def check(self):
      return True

DBusGMainLoop(set_as_default=True)
ampserv = AmpService()

loop = gobject.MainLoop()
loop.run()
