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

import sys
import serial
import logging

READVAL = 50
STRIPPING_ERROR = 999

class SerialController:

  serial_logger = logging.getLogger("rs232server.serial")

  def __init__(self, tty, baud_rate, delay):
    try:
      self.ser = serial.Serial(tty, baud_rate, timeout=delay)
      self.ser.flushInput()
      self.ser.flushOutput()
      self.serial_logger.debug("Initialised %s with baud rate %d", tty, baud_rate)
    except:
      self.serial_logger.debug(sys.exc_info())
      self.serial_logger.error("Could not open " + tty)
      exit(1)

  def cmd(self, cmd, read=False):
    try:
      if cmd is not "clear":
        self.ser.write(cmd)
        self.serial_logger.debug (cmd + " called")
        if read:
          code = self.ser.read(READVAL)
          return code
      else:
        self.ser.flushOutput()
        waiting = self.ser.inWaiting()
        if (waiting > 0):
          self.ser.read(waiting)
    except:
      self.serial_logger.debug (cmd + " call failed")

  def flush(self):
    self.ser.flush()
