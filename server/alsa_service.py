#!/usr/bin/python2

# Copyright (C) 2012 Brendan Le Foll <brendan@fridu.net>
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

import dbus
import dbus.service
import logging
import azur_service
from dbus.mainloop.glib import DBusGMainLoop

try:
    # Attempt to import the pyalsaaudio module.
    import alsaaudio as alsa

except:
    print "error : alsaaudio : moduled failed to import\n"
    print "Debian: Install python-pyalsaaudio"
    print "Arch:   Install python2-pyalsa"

RS232SERVER_BUS_NAME = 'uk.co.madeo.rs232server'
ALSASERVER_IFACE = 'uk.co.madeo.rs232server.alsa'
ALSASERVER_BUS_PATH = '/uk/co/madeo/rs232server/alsa'

class AlsaService(dbus.service.Object):

  alsa_logger= logging.getLogger("rs232server.alsa")
  headphoneMode = False

  def __init__(self, volume, selection, spdif, ampService):
    # default volume
    self.ampService = ampService
    self.volume = volume
    self.selection = selection
    self.spdif = spdif
    bus_name = dbus.service.BusName(RS232SERVER_BUS_NAME, bus=dbus.SystemBus())
    dbus.service.Object.__init__(self, bus_name, ALSASERVER_BUS_PATH)
    self.alsa_logger.debug("Started Alsa Service on " + ALSASERVER_BUS_PATH)

  def headphone_mode(self, val):
    self.alsa_logger.debug("headphone mode : %r", val)
    if val:
      alsa.Mixer(self.selection).setmute(0)
      alsa.Mixer(self.selection).setvolume(int(self.volume))
      alsa.Mixer(self.spdif).setmute(1)
      self.ampService.poweroff()
      self.headphoneMode = True
    else:
      alsa.Mixer(self.selection).setvolume(int(0))
      alsa.Mixer(self.spdif).setmute(0)
      # check xbmc is running
      # check if xbmc is playing something
      self.ampService.poweron()
      self.headphoneMode = False

  @dbus.service.method(ALSASERVER_IFACE)
  def mute(self):
    raise NotImplemented

  @dbus.service.method(ALSASERVER_IFACE)
  def unmute(self):
    raise NotImplemented

  @dbus.service.method(ALSASERVER_IFACE, out_signature='b')
  def check(self):
    return True

  @dbus.service.method(ALSASERVER_IFACE)
  def headphonemodeon(self):
    self.headphone_mode(True)

  @dbus.service.method(ALSASERVER_IFACE)
  def headphonemodeoff(self):
    self.headphone_mode(False)

  @dbus.service.method(ALSASERVER_IFACE, out_signature='b')
  def getheadphonemodestatus(self):
    return self.headphoneMode
