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

import lgtv_cmds

LGTVSERVICE_IFACE = 'uk.co.madeo.rs232server.lgtv'
LGTVSERVICE_OBJ_PATH = '/uk/co/madeo/rs232server/lgtv'

DELAY = 1
BAUD_RATE = 9600
BYTESIZE = 8
READVAL = 10

class LgtvService(BaseService):

  def __init__(self, tty, bus_name):
    BaseService.__init__(self, bus_name, LGTVSERVICE_OBJ_PATH, tty, BAUD_RATE, READVAL, lgtv_cmds)

  @dbus.service.method(LGTVSERVICE_IFACE, in_signature='sib', out_signature='s')
  def send_cmd(self, cmd, repeat, check):
    self.logger.debug("sent command : %s", cmd)
    if cmd == "help":
      self.logger.debug("Getting help!")
      return self.help()
    if (check):
      return self.queue.add(lgtv_cmds.commands[cmd] + b'\r', check)
    for i in range(0, repeat):
      self.queue.add(lgtv_cmds.commands[cmd] + b'\r', check)
    return ""
