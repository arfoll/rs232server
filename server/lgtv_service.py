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

import sys
import dbus
import dbus.service
import logging
import serial
from dbus.mainloop.glib import DBusGMainLoop
from serial_controller import SerialController

import lgtv_cmds

LGTVSERVICE_IFACE = 'uk.co.madeo.rs232server.lgtv'
LGTVSERVICE_OBJ_PATH = '/uk/co/madeo/rs232server/lgtv'

DELAY = 1
BAUD_RATE = 9600
BYTESIZE = 8

class LgtvService(dbus.service.Object):

  lgtv_logger = logging.getLogger("rs232server.lgtv")

  def __init__(self, tty, bus_name):
    dbus.service.Object.__init__(self, bus_name, LGTVSERVICE_OBJ_PATH)
    
    try:
      ser = serial.Serial(tty, BAUD_RATE, BYTESIZE, serial.PARITY_NONE,
                          serial.STOPBITS_ONE, xonxoff=0, rtscts=0, timeout=DELAY)
    except:
      self.lgtv_logger.error("Could not open " + tty)
      exit(1)

    self.queue = SerialController(ser)
    self.lgtv_logger.debug("Started LGTV Service on %s", LGTVSERVICE_OBJ_PATH)

  def send_cmd(self, cmd, direct=False):
    self.lgtv_logger.debug("sent command : %s", cmd)
    self.queue.add(lgtv_cmds.commands[cmd], direct)

  @dbus.service.method(LGTVSERVICE_IFACE)
  def poweroff(self):
    self.send_cmd('poweroff')

  @dbus.service.method(LGTVSERVICE_IFACE)
  def poweron(self):
    self.send_cmd('poweron')
