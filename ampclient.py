#!/usr/bin/python2

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
from ampclient_dbus import AmpClient

PROGRAM_VERSION=1.0

DESCRIPTION = "Send commands to ampserver. Commands are :" \
              "up, down, mute, unmute, on, off, video1, cdaux, sversion, pversion, volume"

class FuncTranslate:
  def __init__(self, args):
    self.amp = AmpClient()
    self.makeFuncDict()
    self.call(args.cmd, args.db)

  def makeFuncDict(self):
    self.funcdict = {
      'up':       self.amp.vol_up,
      'down':     self.amp.vol_down,
      'volume':   self.amp.get_volume,
      'mute':     self.amp.mute,
      'unmute':   self.amp.unmute,
      'on':       self.amp.power_on,
      'off':      self.amp.power_off,
      'video1':   self.amp.input_video1,
      'cdaux':    self.amp.input_cdaux,
      'sverion':  self.amp.get_sversion,
      'pversion': self.amp.get_pversion
    }

  def call(self, cmd, db):
    if db is not None:
      self.funcdict[cmd](db)
    else:
      self.funcdict[cmd]()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(version=PROGRAM_VERSION, description=DESCRIPTION)
  parser.add_argument('cmd', metavar='command',
                      help='The command to be passed to ampserver')
  parser.add_argument('--db', '-d', action='store', dest='db', type=int,
                      help='db change (for up/down commands only)')
  args = parser.parse_args()

  if (args.db is None) or (args.cmd == 'up') or (args.cmd == 'down'):
    trans = FuncTranslate(args)
  else:
    print "do not specify a DB other than for up/down commands"
