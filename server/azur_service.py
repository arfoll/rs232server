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
import logging
from dbus.mainloop.glib import DBusGMainLoop
from serial_queue import SerialQueue

RS232SERVER_BUS_NAME = 'uk.co.madeo.rs232server'
AZURSERVER_IFACE = 'uk.co.madeo.rs232server.azur'
AZURSERVER_BUS_PATH = '/uk/co/madeo/rs232server/azur'

DELAY = 0.1
BAUD_RATE = 9600

class AzurService(dbus.service.Object):

  azur_logger = logging.getLogger("rs232server.azur")

  def __init__(self, tty):
    bus_name = dbus.service.BusName(RS232SERVER_BUS_NAME, bus=dbus.SystemBus())
    dbus.service.Object.__init__(self, bus_name, AZURSERVER_BUS_PATH)
    self.queue = SerialQueue(tty, BAUD_RATE, DELAY)
    self.azur_logger.debug("Started Azur Service on " + AZURSERVER_BUS_PATH)

  def checkReturnValueInt(self, val):
    try:
      return int(val)
    except:
      return -100

  @dbus.service.method(AZURSERVER_IFACE)
  def mute(self):
    self.queue.add('mute')

  @dbus.service.method(AZURSERVER_IFACE)
  def unmute(self):
    self.queue.add('unmute')

  @dbus.service.method(AZURSERVER_IFACE)
  def poweron(self):
    self.queue.add('poweron')

  @dbus.service.method(AZURSERVER_IFACE)
  def poweroff(self):
    self.queue.add('poweroff')

  @dbus.service.method(AZURSERVER_IFACE, in_signature='i')
  def volumedown(self, db):
    for i in range(0, db):
      self.queue.add('voldown')

  @dbus.service.method(AZURSERVER_IFACE, in_signature='i')
  def volumeup(self, db):
    for i in range(0, db):
      self.queue.add('volup')

  @dbus.service.method(AZURSERVER_IFACE, out_signature='i')
  def getvolume(self):
    self.queue.add('volup', True)
    return self.checkReturnValueInt(self.queue.add('voldown', True))

  @dbus.service.method(AZURSERVER_IFACE)
  def setinputvideo1(self):
    self.queue.add('video1')

  @dbus.service.method(AZURSERVER_IFACE)
  def setinputcdaux(self):
    self.queue.add('cdaux')

  @dbus.service.method(AZURSERVER_IFACE, out_signature='s')
  def getsversion(self):
    return str(self.queue.add('sversion', True))

  @dbus.service.method(AZURSERVER_IFACE, out_signature='s')
  def getpversion(self):
    return str(self.queue.add('pversion', True))

  @dbus.service.method(AZURSERVER_IFACE)
  def clear(self):
    self.queue.add('clear', True)

  @dbus.service.method(AZURSERVER_IFACE, out_signature='b')
  def check(self):
    return True

