#!/usr/bin/env python2

# Copyright (C) 2011,2012,2013 Brendan Le Foll <brendan@fridu.net>
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

import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from serial_controller import SerialController
from base_service import BaseService

import azur_cmds

AZURSERVICE_IFACE = 'uk.co.madeo.rs232server.azur'
AZURSERVICE_OBJ_PATH = '/uk/co/madeo/rs232server/azur'

BAUD_RATE = 9600
STRIPPING_ERROR = 999
READVAL = 50

class AzurService(BaseService):

  def __init__(self, tty, bus_name):
    BaseService.__init__(self, bus_name, AZURSERVICE_OBJ_PATH, tty, BAUD_RATE, READVAL, azur_cmds)

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
      self.logger.debug("stripping error for %s", code)
      return STRIPPING_ERROR

  def friendlyReply(self, code, cmd):
    self.logger.debug("Reply code pre-stripping %s", code)
    if self.findKey(code):
      return self.stripErrorCode(code)
    else:
      return code.replace(azur_cmds.replies[cmd], '')

  def fire_cmd(self, cmd, direct=False):
    self.logger.debug("sent command : %s", cmd)
    if direct:
      code = self.queue.add(azur_cmds.commands[cmd].decode('ascii'), direct)
      return self.friendlyReply(code, cmd)
    else:
      self.queue.add(azur_cmds.commands[cmd].decode('ascii'), direct)

  # typical call would be ('poweron', 1, False)
  @dbus.service.method(AZURSERVICE_IFACE, in_signature='sib', out_signature='s')
  def send_cmd(self, cmd, repeat, check):
    if cmd == "help":
      self.logger.debug("Getting help!")
      return self.help()
    if (check):
      return str(self.fire_cmd(cmd, check))
    for i in range(0, repeat):
      self.fire_cmd(cmd, check)
    return ""

  @dbus.service.method(AZURSERVICE_IFACE)
  def clear(self):
    self.queue.add("clear", True)

