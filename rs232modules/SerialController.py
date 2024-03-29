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

import logging
import sys
import serial

from . import Shared

DELAY = 0.05
MAXCMDS = 0
STRIPPING_ERROR = 999

class SerialController:

  def __init__(self, ser, readval):
    self.serial_logger = logging.getLogger(Shared.APP_NAME + '.' + self.__class__.__name__)

    self.ser = ser
    self.ser.flushInput()
    self.ser.flushOutput()
    self.serial_logger.debug("Initialised %s with baud rate %d", ser.name, ser.baudrate)

    self.readval = readval
    self.serial_logger.debug("Serial is %s", str(ser))

  def clear(self):
    self.serial_logger.debug ("Clearing read buffer")
    self.ser.flush()
    self.ser.flushOutput()
    self.ser.flushInput()
    waiting = self.ser.inWaiting()
    if (waiting > 0):
      self.ser.read(waiting)

  def cmd(self, cmd, read=False):
    self.serial_logger.debug ("cmd is: %s", cmd)
    try:
      if cmd != "clear":
        numBytes = self.ser.write(cmd.encode('ascii'))
        self.serial_logger.debug("Wrote %d bytes", numBytes)
        self.serial_logger.debug (cmd.rstrip() + " called")
        if read:
          code = self.ser.read(self.readval)
          return code
      else:
        self.clear()
    except:
      self.serial_logger.error ("%s call failed", cmd.rstrip())
