#!/usr/bin/python2

# Copyright (C) 2011,2012 Brendan Le Foll <brendan@fridu.net>
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
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from azur_service import AzurService
from lgtv_service import LgtvService
from ConfigParser import SafeConfigParser

LOG_FILENAME = '/tmp/rs232server.log'
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
RS232SERVER_BUS_NAME = 'uk.co.madeo.rs232server'
DESCRIPTION = "Listen over dbus for commands to be sent over RS232"

def configureLogging(verbose, logger):
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

def initServices(parser, logger, bus_name):
  # Azur Service
  try:
    azurtty = parser.get('azur', 'tty')
    ampService = AzurService(str(azurtty), bus_name)
  except:
    logger.debug('disabled azur service')

  # LGTV Service
  try:
    lgtvtty = parser.get('lgtv', 'tty')
    tvService = LgtvService(str(lgtvtty), bus_name)
  except:
    logger.debug('disabled lgtv service')

def main():
  # parse CLI arguments
  parser = argparse.ArgumentParser(description=DESCRIPTION)
  parser.add_argument('--verbose', '-v', action='store_true', dest='verbose', default=False,
                      help='enables more verbose output')
  parser.add_argument('--development', '-dev', action='store_true', dest='dev', default=False,
                      help='development mode disables some commands that could be dangerous. Read documentation before using')
  args = parser.parse_args()

  # set up logging
  logger = logging.getLogger("rs232server")
  configureLogging(args.verbose, logger)

  # read configuration file
  parser = SafeConfigParser()
  try:
    parser.read('rs232.conf')
  except:
    logger.error('failed to read rs232.conf')
    exit(1)

  # start dbus mainloop
  DBusGMainLoop(set_as_default=True)
  try:
    bus_name = dbus.service.BusName(RS232SERVER_BUS_NAME, bus=dbus.SystemBus())
  except:
    logger.error('fatal dbus error')
    exit(1)

  # parse configuration file
  try:
    azurtty = parser.get('azur', 'tty')
  except:
    azurtty = None
    logger.debug('disabled azur service')

  try:
    lgtvtty = parser.get('lgtv', 'tty')
  except:
    lgtvtty = None
    logger.debug('disabled lgtv service')

  # enable the correct services
  if azurtty is not None:
    AzurService(str(azurtty), bus_name)
  if lgtvtty is not None:
    LgtvService(str(lgtvtty), bus_name)

  loop = gobject.MainLoop()
  loop.run()

if __name__ == "__main__":
    sys.exit(main())
