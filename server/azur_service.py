#!/usr/bin/python2

# Copyright (C) 2011,2012 Brendan Le Foll <brendan@fridu.net>
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

import dbus
import dbus.service
import logging
from dbus.mainloop.glib import DBusGMainLoop
from serial_controller import SerialController

import azur_cmds

RS232SERVER_BUS_NAME = 'uk.co.madeo.rs232server'
AZURSERVER_IFACE = 'uk.co.madeo.rs232server.azur'
AZURSERVER_BUS_PATH = '/uk/co/madeo/rs232server/azur'

DELAY = 0.1
BAUD_RATE = 9600
STRIPPING_ERROR = 999

class AzurService(dbus.service.Object):

  azur_logger = logging.getLogger("rs232server.azur")

  def __init__(self, tty):
    bus_name = dbus.service.BusName(RS232SERVER_BUS_NAME, bus=dbus.SystemBus())
    dbus.service.Object.__init__(self, bus_name, AZURSERVER_BUS_PATH)
    self.queue = SerialController(tty, BAUD_RATE, DELAY)
    self.azur_logger.debug("Started Azur Service on " + AZURSERVER_BUS_PATH)

  def checkReturnValueInt(self, val):
    try:
      return int(val)
    except:
      return -100

  def findKey(self, val):
    try:
      return [k for k, v in azur_cmds.errors.iteritems() if v == val][0]
    except:
      return 0

  def stripErrorCode(self, code):
    try:
      code = code.replace('#', '')
      code = code.replace(',', '')
      code = code.replace('\n', '')
      return int(code)
    except:
      self.azur_logger.debug("stripping error for %s", code)
      return STRIPPING_ERROR

  def friendlyReply(self, code, cmd):
    if self.findKey(code):
      return self.stripErrorCode(code)
    else:
      return code.replace(azur_cmds.replies[cmd], '')

  def send_cmd(self, cmd, direct=False):
    self.azur_logger.debug("sent command : %s", cmd)
    if direct:
      code = self.queue.add(azur_cmds.commands[cmd], direct)
      return self.friendlyReply(code, cmd)
    else:
      self.queue.add(azur_cmds.commands[cmd], direct)

  @dbus.service.method(AZURSERVER_IFACE)
  def mute(self):
    self.send_cmd('mute')

  @dbus.service.method(AZURSERVER_IFACE)
  def unmute(self):
    self.send_cmd('unmute')

  @dbus.service.method(AZURSERVER_IFACE)
  def poweron(self):
    self.send_cmd('poweron')

  @dbus.service.method(AZURSERVER_IFACE)
  def poweroff(self):
    self.send_cmd('poweroff')

  @dbus.service.method(AZURSERVER_IFACE, in_signature='i')
  def volumedown(self, db):
    for i in range(0, db):
      self.send_cmd('voldown')

  @dbus.service.method(AZURSERVER_IFACE, in_signature='i')
  def volumeup(self, db):
    for i in range(0, db):
      self.send_cmd('volup')

  @dbus.service.method(AZURSERVER_IFACE)
  def setinputvideo1(self):
    self.send_cmd('video1')

  @dbus.service.method(AZURSERVER_IFACE)
  def setinputvideo1(self):
    self.send_cmd('video2')

  @dbus.service.method(AZURSERVER_IFACE)
  def setinputvideo1(self):
    self.send_cmd('video3')

  @dbus.service.method(AZURSERVER_IFACE)
  def setinputcdaux(self):
    self.send_cmd('cdaux')

  @dbus.service.method(AZURSERVER_IFACE, out_signature='i')
  def getvolume(self):
    self.send_cmd('volup', True)
    return self.checkReturnValueInt(self.send_cmd('voldown', True))

  @dbus.service.method(AZURSERVER_IFACE, out_signature='s')
  def getsversion(self):
    return str(self.send_cmd('sversion', True))

  @dbus.service.method(AZURSERVER_IFACE, out_signature='s')
  def getpversion(self):
    return str(self.send_cmd('pversion', True))

  @dbus.service.method(AZURSERVER_IFACE)
  def clear(self):
    self.queue.add("clear", True)

  @dbus.service.method(AZURSERVER_IFACE, out_signature='b')
  def check(self):
    return True
