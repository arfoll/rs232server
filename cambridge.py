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
import time

class CambridgeCLI:
  # Open serial port for read/write later
  ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

  def __init__(self):
    #Debuggering the serial
    print self.ser
    #Just to be sure...
    self.ser.flushInput()

  def vol_amp_up(self):
    self.ser.write ("#1,02\r")
    time.sleep (0.1)
    self.ser.write ("#1,02\r")
    time.sleep (0.1)
    self.ser.write ("#1,02\r")
    time.sleep (0.1)
    self.ser.write ("#1,02\r")
    time.sleep (0.1)
    self.ser.write ("#1,02\r")

  def vol_amp_down(self):
    self.ser.write ("#1,03\r")
    time.sleep (0.1)
    self.ser.write ("#1,03\r")
    time.sleep (0.1)
    self.ser.write ("#1,03\r")
    time.sleep (0.1)
    self.ser.write ("#1,03\r")
    time.sleep (0.1)
    self.ser.write ("#1,03\r")

  def vol_amp_mute (self):
    self.ser.write ("#1,11,01\r")

  def vol_amp_unmute (self):
    self.ser.write ("#1,11,00\r")

  def amp_off (self):
    self.ser.write ("#1,01,0\r")

  def amp_on (self):
    self.ser.write ("#1,01,1\r")

  def amp_set_video1 (self):
    self.ser.write ("#7,01,2\r")

  def amp_set_cdaux (self):
    self.ser.write ("#7,01,7\r")

def help ():
  print "this is the help"

if __name__ == "__main__":
  if len(sys.argv) is not 1:
    amp = CambridgeCLI ()
    if sys.argv[1] == "up":
      amp.vol_amp_up ()
    elif sys.argv[1] == "down":
      amp.vol_amp_down ()
    elif sys.argv[1] == "off":
      amp.amp_off ()
    elif sys.argv[1] == "on":
      amp.amp_on ()
    elif sys.argv[1] == "unmute":
      amp.vol_amp_unmute ()
    elif sys.argv[1] == "mute":
      amp.vol_amp_mute ()
    elif sys.argv[1] == "xbmc":
      amp.amp_set_video1 ()
    elif sys.argv[1] == "cd":
      amp.amp_set_cdaux ()
    else:
      help()
  else:
    help()
