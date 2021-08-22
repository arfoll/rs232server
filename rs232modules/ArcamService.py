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

import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from .SerialController import SerialController
from .BaseService import BaseService

from . import arcam_cmds

ARCAMSERVICE_IFACE = 'uk.co.madeo.rs232server.arcam'
ARCAMSERVICE_OBJ_PATH = '/uk/co/madeo/rs232server/arcam'

DELAY = 1
BAUD_RATE = 38400
BYTESIZE = 8
READVAL = 10

class ArcamService(BaseService):

  def __init__(self, tty, bus_name):
    BaseService.__init__(self, bus_name, ARCAMSERVICE_OBJ_PATH, tty, BAUD_RATE, READVAL, arcam_cmds)

  @dbus.service.method(ARCAMSERVICE_IFACE, in_signature='sib', out_signature='s')
  def send_cmd(self, cmd, repeat, check):
    self.logger.debug("sent command : %s", cmd)
    if cmd == "help":
      self.logger.debug("Getting help!")
      return self.help()
    if (check):
      val = self.ser.cmd(arcam_cmds.commands[cmd], check)
      return val
    for i in range(0, repeat):
      self.ser.cmd(arcam_cmds.commands[cmd], check)
    return ""
