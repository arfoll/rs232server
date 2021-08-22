# Copyright (C) 2011-2020 Brendan Le Foll <brendan@fridu.net>
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

start = "\x50\x43\x5f" # PC_
end = "\x0d" # <CR>

zone_1 = "\x31"
zone_2 = "\x32"

option_0 = "\x30"
option_1 = "\x31"
option_2 = "\x32"
option_3 = "\x33"
option_4 = "\x34"
option_5 = "\x35"
option_6 = "\x36"
option_7 = "\x37"
option_8 = "\x38"
option_9 = "\x39"

commands = {
#volume
  'voldown':  start + "\x2f" + zone_1 + option_0 + end,
  'volup':    start + "\x2f" + zone_1 + option_1 + end,
  'mute':     start + "\x2e" + zone_1 + option_0 + end,
  'unmute':   start + "\x2e" + zone_1 + option_1 + end,
#power
  'poweron':  start + "\x2a" + zone_1 + option_1 + end,
  'poweroff': start + "\x2a" + zone_1 + option_0 + end,
#inputs
  'dvd':      start + "\x31" + zone_1 + option_0 + end,
  'sat':      start + "\x31" + zone_1 + option_1 + end,
  'av':       start + "\x31" + zone_1 + option_2 + end,
  'pvr':      start + "\x31" + zone_1 + option_3 + end,
  'vcr':      start + "\x31" + zone_1 + option_4 + end,
  'cd':       start + "\x31" + zone_1 + option_5 + end,
  'fm':       start + "\x31" + zone_1 + option_6 + end,
  'am':       start + "\x31" + zone_1 + option_7 + end,
  'dvda':     start + "\x31" + zone_1 + option_8 + end,
#two-channel modes
  "pl2movie":  start + "\x34" + zone_1 + option_0 + end,
  "pl2music":  start + "\x34" + zone_1 + option_1 + end,
  "pl2xmovie": start + "\x34" + zone_1 + option_3 + end,
  "pl2xmusic": start + "\x34" + zone_1 + option_4 + end,
  "neo6cinema":start + "\x34" + zone_1 + option_7 + end,
  "neo6music": start + "\x34" + zone_1 + option_8 + end,
#surround modes
  "stereo":    start + "\x35" + zone_1 + "\x2f" + end,
  "dd/dtsmode":start + "\x35" + zone_1 + option_0 + end,
  "pl2mode":   start + "\x35" + zone_1 + option_2 + end
}

responses = {
}
