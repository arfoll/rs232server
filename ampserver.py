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

AZUR_BUS_NAME = 'uk.co.madeo.ampserver'
AZUR_BUS_PATH = '/uk/co/madeo/ampserver'
LOG_FILENAME = '/tmp/ampserver.log'

class AzurServer:
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

class AmpService(dbus.service.Object):
    def __init__(self):
        bus_name = dbus.service.BusName(AZUR_BUS_NAME, bus=dbus.SystemBus())
        dbus.service.Object.__init__(self, bus_name, AZUR_BUS_PATH)
        self.amp = AzurServer()

    @dbus.service.method(AZUR_BUS_NAME)
    def mute(self):
        self.amp.vol_amp_mute()

    @dbus.service.method(AZUR_BUS_NAME)
    def unmute(self):
        self.amp.vol_amp_unmute()

    @dbus.service.method(AZUR_BUS_NAME)
    def poweron(self):
        self.amp.amp_on()

    @dbus.service.method(AZUR_BUS_NAME)
    def poweroff(self):
        self.amp.amp_off()

    @dbus.service.method(AZUR_BUS_NAME)
    def volumedown(self):
        self.amp.vol_amp_down()

    @dbus.service.method(AZUR_BUS_NAME)
    def volumeup(self):
        self.amp.vol_amp_up()

DBusGMainLoop(set_as_default=True)
ampService = AmpService()

logging.debug ("Starting AmpService...")
loop = gobject.MainLoop()
loop.run()
