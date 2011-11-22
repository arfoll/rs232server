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

import serial
import logging

#use azur_cmds
import azur_cmds
cmds = azur_cmds

SERIAL_PORT="/dev/ttyUSB0"
LOG_FILENAME = '/tmp/ampserver.log'
LOG_FORMAT = "%(asctime)s %(message)s"
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format=LOG_FORMAT)

class AmpServer:
  logging.debug ("Starting AmpService...")
  ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)

  def __init__(self):
    self.ser.flushInput()
    logging.debug("Initialising serial port")

  def cmd (self, cmd):
    try:
      chosencmd = cmds.commands[cmd]
      self.ser.write(cmds.commands[cmd])
      logging.debug (cmd + " called")
      return True
    except:
      logging.debug (cmd + " call failed")
      return False

