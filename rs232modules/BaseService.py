# Copyright (C) 2011-2020 Brendan Le Foll <brendan@fridu.net>
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
import dbus
import dbus.service
import logging
from . import Shared
import serial
from .SerialController import SerialController

class invalidtty(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class BaseService(dbus.service.Object):

  def __init__(self, bus_name, obj_path, tty, baud_rate, cmds):
    dbus.service.Object.__init__(self, bus_name, obj_path)
    self.logger = logging.getLogger(Shared.APP_NAME + '.' + self.__class__.__name__ )
    self.cmds = cmds
    try:
      ser = serial.Serial(tty, baud_rate, timeout=Shared.DELAY)
    except:
      raise invalidtty("Could not open " + tty + ", check it is valid and that the user has permission to use it.")

    self.ser = SerialController(ser)
    self.logger.info("Started service on %s", obj_path)

  def help(self):
    string = ""
    for p in self.cmds.commands:
      string += '\n' + p
    # strip first character
    return string[1:]

  # TODO: make these @dbus methods that are inherited from
  def send_cmd(self, cmd, repeat, check):
    self.logger.info("cmd %s sent", cmd)
    self.ser.cmd(cmd)
    return

  def clear(self):
    self.ser.clear()
    return
