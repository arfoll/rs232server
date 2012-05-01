#!/usr/bin/env python2

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
import argparse
from azurclient_dbus import AzurClient
from alsaclient_dbus import AlsaClient

DESCRIPTION = "Send commands to rs232server. Commands are :" \
              "up, down, mute, unmute, on, off, video1, cdaux, sversion, pversion, volume"

class FuncTranslate:
  def __init__(self, args):
    self.azur = AzurClient()
    self.alsa = AlsaClient()
    self.makeFuncDict()
    self.call(args.cmd, args.db)

  def makeFuncDict(self):
    self.funcdict = {
      'up':       self.azur.vol_up,
      'down':     self.azur.vol_down,
      'volume':   self.azur.get_volume,
      'mute':     self.azur.mute,
      'unmute':   self.azur.unmute,
      'on':       self.azur.power_on,
      'off':      self.azur.power_off,
      'video1':   self.azur.input_video1,
      'video2':   self.azur.input_video2,
      'video3':   self.azur.input_video3,
      'cdaux':    self.azur.input_cdaux,
      'headphonemodeon': self.alsa.set_headphone_modeon,
      'headphonemodeoff': self.alsa.set_headphone_modeoff,
      'sversion': self.azur.get_sversion,
      'pversion': self.azur.get_pversion
    }

  def call(self, cmd, db):
    try:
      if db is not -1:
        self.funcdict[cmd](db)
      else:
        self.funcdict[cmd]()
    except KeyError:
      print "Command %s has no mapped function name" % cmd
    except Exception, err:
      print "Error : %s" %str(err)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description=DESCRIPTION)
  parser.add_argument('cmd', metavar='command',
                      help='The command to be passed to ampserver')
  parser.add_argument('--db', '-d', action='store', dest='db', type=int, default=-1,
                      help='db change (for up/down commands only)')
  args = parser.parse_args()

  trans = FuncTranslate(args)
