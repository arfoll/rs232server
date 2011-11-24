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

import time
import Queue
from threading import Thread
from threading import Timer
from ampserver_serial import AmpServer

DELAY=0.1
MAXCMDS=0

class AmpServerQueue:

  def __init__(self, tty):
    self.amp = AmpServer(tty)
    self.queue = Queue.Queue()
    self.t = Thread(target=self.monitor)
    self.t.daemon = True
    self.t.start()

  def monitor(self):
    while True:
      if not self.queue.empty():
        item = self.queue.get(True)
        self.amp.cmd(item)
        self.queue.task_done()
        time.sleep(DELAY)

  def add(self, cmd, direct=False):
    if direct:
      #direct execution allows for return
      return self.amp.cmd(cmd, True)
    else:
      self.queue.put(cmd, True)
      # delay here seems to allow the monitor thread to come to life on my single core CPU
      time.sleep(DELAY)
