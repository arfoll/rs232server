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
import gobject
import argparse
import logging
from dbus.mainloop.glib import DBusGMainLoop
from azur_service import AzurService

LOG_FILENAME = '/tmp/rs232server.log'
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
RS232SERVER_BUS_NAME = 'uk.co.madeo.rs232server'
DEFAULT_AZURTTY="/dev/ttyUSB0"
DESCRIPTION = "Listen over dbus for commands to be sent over RS232"

def set_logging(verbose):
  logger = logging.getLogger("rs232server")
  logger.setLevel(logging.DEBUG)
  formatter = logging.Formatter(LOG_FORMAT)
  fh = logging.FileHandler(LOG_FILENAME)
  fh.setLevel(logging.DEBUG)
  fh.setFormatter(formatter)
  logger.addHandler(fh)
  ch = logging.StreamHandler()
  if verbose:
    ch.setLevel(logging.DEBUG)
  else:
    ch.setLevel(logging.ERROR)
  ch.setFormatter(formatter)
  logger.addHandler(ch)

def main():
  parser = argparse.ArgumentParser(description=DESCRIPTION)
  parser.add_argument('--azurtty', '-at', action='store', dest='azurtty', default=DEFAULT_AZURTTY,
                      help='define which serial tty to use for azur service. Default is ' + DEFAULT_AZURTTY)
  parser.add_argument('--verbose', '-v', action='store_true', dest='verbose', default=False,
                      help='enables more verbose output')
  parser.add_argument('--development', '-dev', action='store_true', dest='dev', default=False,
                      help='development mode disables some commands that could be dangerous. Read documentation before using')

  args = parser.parse_args()

  set_logging(args.verbose)

  DBusGMainLoop(set_as_default=True)
  AzurService(args.azurtty)

  loop = gobject.MainLoop()
  loop.run()

if __name__ == "__main__":
    sys.exit(main())
