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

import azur_cmds

AMPSERVER_BUS_NAME = 'uk.co.madeo.ampserver'
AMPSERVER_BUS_PATH = '/uk/co/madeo/ampserver'
LOG_FILENAME = '/tmp/ampserver.log'

logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

class AmpServer:
  ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

  def __init__(self):
    #Debuggering the serial
    print self.ser
    #Just to be sure...
    self.ser.flushInput()
    logging.debug("Initialising serial port")

#TODO: generic call for volume
  def vol_up(self):
    self.ser.write ("#1,02\r")
    time.sleep (0.1)
    self.ser.write ("#1,02\r")
    time.sleep (0.1)
    self.ser.write ("#1,02\r")
    time.sleep (0.1)
    self.ser.write ("#1,02\r")
    time.sleep (0.1)
    self.ser.write ("#1,02\r")
    logging.debug("volume up")

  def vol_down(self):
    self.ser.write ("#1,03\r")
    time.sleep (0.1)
    self.ser.write ("#1,03\r")
    time.sleep (0.1)
    self.ser.write ("#1,03\r")
    time.sleep (0.1)
    self.ser.write ("#1,03\r")
    time.sleep (0.1)
    self.ser.write ("#1,03\r")
    logging.debug("volume down")

  def cmd (self, cmd):
    self.ser.write(azur_cmds.commands[cmd])
    logging.debug (cmd + " called")

class AmpService(dbus.service.Object):
    def __init__(self):
      bus_name = dbus.service.BusName(AMPSERVER_BUS_NAME, bus=dbus.SystemBus())
      dbus.service.Object.__init__(self, bus_name, AMPSERVER_BUS_PATH)
      self.amp = AmpServer()

    @dbus.service.method(AMPSERVER_BUS_NAME)
    def mute(self):
      self.amp.cmd('mute')

    @dbus.service.method(AMPSERVER_BUS_NAME)
    def unmute(self):
      self.amp.cmd('unmute')

    @dbus.service.method(AMPSERVER_BUS_NAME)
    def poweron(self):
      self.amp.cmd('poweron')

    @dbus.service.method(AMPSERVER_BUS_NAME)
    def poweroff(self):
      self.amp.cmd('poweroff')

    @dbus.service.method(AMPSERVER_BUS_NAME)
    def volumedown(self):
      self.amp.vol_down()

    @dbus.service.method(AMPSERVER_BUS_NAME)
    def volumeup(self):
      self.amp.vol_up()

    @dbus.service.method(AMPSERVER_BUS_NAME)
    def setinputvideo1(self):
      self.amp.cmd('video1')

    @dbus.service.method(AMPSERVER_BUS_NAME)
    def setinputcdaux(self):
      self.amp.cmd('cdaux')

DBusGMainLoop(set_as_default=True)
ampserv = AmpService()

logging.debug ("Starting AmpService...")
loop = gobject.MainLoop()
loop.run()
