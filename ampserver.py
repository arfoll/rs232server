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
import gobject
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import logging

#use azur_cmds
import azur_cmds
cmds = azur_cmds

SERIAL_PORT="/dev/ttyUSB0"
AMPSERVER_BUS_NAME = 'uk.co.madeo.ampserver'
AMPSERVER_BUS_PATH = '/uk/co/madeo/ampserver'
LOG_FILENAME = '/tmp/ampserver.log'
LOG_FORMAT = "%(asctime)s %(message)s"
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format=LOG_FORMAT)

class AmpServer:
  ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)

  def __init__(self):
    self.ser.flushInput()
    logging.debug("Initialising serial port")

  def setinput (self, cmd):
    try:
      choseninput = cmds.inputs[cmd]
      self.ser.write(cmds.inputs[cmd])
      logging.debug (cmd + " input changed")
      return True
    except:
      logging.debug (cmd + " input change failed")
      return False

  def cmd (self, cmd):
    try:
      chosencmd = cmds.commands[cmd]
      self.ser.write(cmds.commands[cmd])
      logging.debug (cmd + " called")
      return True
    except:
      logging.debug (cmd + " call failed")
      return False

class AmpService(dbus.service.Object):
    def __init__(self):
      bus_name = dbus.service.BusName(AMPSERVER_BUS_NAME, bus=dbus.SystemBus())
      dbus.service.Object.__init__(self, bus_name, AMPSERVER_BUS_PATH)
      self.amp = AmpServer()

    @dbus.service.method(AMPSERVER_BUS_NAME, out_signature='b')
    def mute(self):
      return self.amp.cmd('mute')

    @dbus.service.method(AMPSERVER_BUS_NAME, out_signature='b')
    def unmute(self):
      return self.amp.cmd('unmute')

    @dbus.service.method(AMPSERVER_BUS_NAME, out_signature='b')
    def poweron(self):
      return self.amp.cmd('poweron')

    @dbus.service.method(AMPSERVER_BUS_NAME, out_signature='b')
    def poweroff(self):
      return self.amp.cmd('poweroff')

    @dbus.service.method(AMPSERVER_BUS_NAME, out_signature='b')
    def volumedown(self):
      return self.amp.cmd('voldown')

    @dbus.service.method(AMPSERVER_BUS_NAME, out_signature='b')
    def volumeup(self):
      return self.amp.cmd('volup')

    @dbus.service.method(AMPSERVER_BUS_NAME, out_signature='b')
    def setinputvideo1(self):
      return self.amp.setinput('video1')

    @dbus.service.method(AMPSERVER_BUS_NAME, out_signature='b')
    def setinputcdaux(self):
      return self.amp.setinput('cdaux')

    @dbus.service.method(AMPSERVER_BUS_NAME, out_signature='b')
    def check(self):
      return True

DBusGMainLoop(set_as_default=True)
ampserv = AmpService()

logging.debug ("Starting AmpService...")
loop = gobject.MainLoop()
loop.run()
