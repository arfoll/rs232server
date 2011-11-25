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

LOG_FILENAME = '/tmp/ampserver.log'
LOG_FORMAT = "%(asctime)s %(message)s"
READVAL = 50
DELAY = 0.1
STRIPPING_ERROR = 999
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format=LOG_FORMAT)

class AmpServer:
  logging.debug ("Starting AmpService...")

  def __init__(self, tty):
    try:
      self.ser = serial.Serial(tty, 9600, timeout=DELAY)
      self.ser.flushInput()
      self.ser.flushOutput()
      logging.debug("Initialising serial port")
    except:
      message = "Could not open port" + tty
      print message
      logging.debug(message)
      exit(1)

  def findKey(self, val):
    try:
      return [k for k, v in cmds.errors.iteritems() if v == val][0]
    except:  
      return 0

  def stripErrorCode(self, code):
    try:
      code = code.replace('#', '')
      code = code.replace(',', '')
      code = code.replace('\n', '')
      return int(code)
    except:
      logging.debug("stripping error for " + code)
      return STRIPPING_ERROR

  def cmd (self, cmd, read=False):
    try:
      if cmd is not "clear":
        chosencmd = cmds.commands[cmd]
        self.ser.write(cmds.commands[cmd])
        logging.debug (cmd + " called")
        if read:
          code = self.ser.read(READVAL)
          if self.findKey(code):
            return self.stripErrorCode(code) 
          else:
            return code.replace(cmds.replies[cmd], '')
          return code
      else:
        self.ser.flushOutput()
        waiting = self.ser.inWaiting()
        print waiting
        if (waiting > 0):
          self.ser.read(waiting)
    except:
      logging.debug (cmd + " call failed")

