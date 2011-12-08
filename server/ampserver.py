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

import gobject
import argparse
from dbus.mainloop.glib import DBusGMainLoop
from ampserver_dbus import AmpService

DEFAULT_TTY="/dev/ttyUSB0"
DESCRIPTION = "Listen over dbus for commands to be sent over RS232"

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description=DESCRIPTION)
  parser.add_argument('--tty', '-t', action='store', dest='tty',
                      help='define which serial tty to use. Default is /dev/ttyUSB0')

  args = parser.parse_args()

  if args.tty is not None:
    tty = args.tty
  else:
    tty = DEFAULT_TTY

  DBusGMainLoop(set_as_default=True)
  ampserv = AmpService(tty)
  loop = gobject.MainLoop()
  loop.run()
