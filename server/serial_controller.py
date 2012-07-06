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

import sys
import time
import Queue
import logging
import serial
from threading import Thread
from threading import Timer

DELAY = 0.05
MAXCMDS = 0
STRIPPING_ERROR = 999

class SerialController:

  serial_logger = logging.getLogger("rs232server.serial")

  def __init__(self, ser, readval):
    self.setup_serial(ser)
    self.readval = readval

    # set up queue and start queue monitoring thread
    self.queue = Queue.Queue()
    self.t = Thread(target=self.monitor)
    self.t.daemon = True
    self.t.start()

  def setup_serial(self, ser):
    self.ser = ser
    self.ser.flushInput()
    self.ser.flushOutput()
    self.serial_logger.debug("Initialised %s with baud rate %d", ser.name, ser.baudrate)

  def cmd(self, cmd, read=False):
    try:
      if cmd is not "clear":
        self.ser.write(cmd)
        self.serial_logger.debug (cmd.rstrip() + " called")
        if read:
          code = self.ser.read(readval)
          return code
      else:
        self.serial_logger.debug ("clearing read buffer")
        self.ser.flushOutput()
        waiting = self.ser.inWaiting()
        if (waiting > 0):
          self.ser.read(waiting)
    except:
      self.serial_logger.error (cmd.rstrip() + " call failed")

  def monitor(self):
    while True:
      if not self.queue.empty():
        item = self.queue.get(True)
        self.cmd(item)
        self.queue.task_done()
        self.ser.flush()

  def add(self, cmd, direct=False):
    if direct:
      #direct execution allows for return
      return self.cmd(cmd, True)
    else:
      self.queue.put(cmd, True)
      # delay here seems to allow the monitor thread to come to life on my single core CPU
      time.sleep(DELAY)
