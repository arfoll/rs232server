#!/usr/bin/env python2

# Copyright (C) 2018 Brendan Le Foll <brendan@fridu.net>
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
from SerialController import SerialController
from BaseService import BaseService

import azur1_cmds

AZUR1SERVICE_IFACE = 'uk.co.madeo.rs232server.azur1'
AZUR1SERVICE_OBJ_PATH = '/uk/co/madeo/rs232server/azur1'

BAUD_RATE = 9600
STRIPPING_ERROR = 999
READVAL = 50

class Azur1Service(BaseService):

  last = ("none", "-0")

  def __init__(self, tty, bus_name):
    BaseService.__init__(self, bus_name, AZUR1SERVICE_OBJ_PATH, tty, BAUD_RATE, READVAL, azur1_cmds)

  def checkReturnValueInt(self, val):
    try:
      return int(val)
    except:
      return -100

  def findKey(self, val):
    try:
      return [k for k, v in azur1_cmds.errors.iteritems() if v == val][0]
    except:
      return 0

  def stripErrorCode(self, code):
    try:
      code = code.replace('#', '')
      code = code.replace(',', '')
      code = code.replace('\n', '')
      return int(code)
    except:
      self.logger.warning("Stripping error for %s", code)
      return STRIPPING_ERROR

  def friendlyReply(self, code, cmd):
    self.logger.debug("Reply code pre-stripping %s", code)
    if self.findKey(code):
      return self.stripErrorCode(code)
    else:
      return code.replace(azur1_cmds.replies[cmd], '')

  def fire_cmd(self, cmd, direct=False):
    self.logger.debug("sent command : %s", cmd)
    if direct:
      code = self.queue.add(azur1_cmds.commands[cmd].decode('ascii'), direct)
      self.last = (cmd, self.friendlyReply(code, cmd))
      self.logger.debug("Reply is (%s, %s)", self.last[0], self.last[1])
      return self.last[1]
    else:
      self.queue.add(azur1_cmds.commands[cmd].decode('ascii'), direct)

  # typical call would be ('poweron', 1, False)
  @dbus.service.method(AZUR1SERVICE_IFACE, in_signature='sib', out_signature='s')
  def send_cmd(self, cmd, repeat, direct):
    if cmd == "help":
      self.logger.debug("Getting help!")
      return self.help()
    for i in range(0, repeat):
      # volume level check code
      if (self.last[0] == "volup"):
        if (int(self.last[1]) > int(-30)):
          self.logger.error("Volume is too high!")
          return "WARNING: VOLUME is really high..."
        else:
          self.logger.debug("Volume is %s, keep playing...", self.last[1])
      # repeat if required
      if i == (repeat-1) and direct:
        val = self.fire_cmd(cmd, direct)
        #logger.debug("val returned is %s", val)
        return val
      self.fire_cmd(cmd, direct)
    return ""

  @dbus.service.method(AZUR1SERVICE_IFACE)
  def clear(self):
    self.queue.add("clear", True)

