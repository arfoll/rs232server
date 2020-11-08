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

CONF_NAME="rs232"
SYS_CONF_PATH="/etc/"
USER_CONF_PATH="~/."
CONF_PREFIX=".conf"

SYS_CONF=SYS_CONF_PATH+CONF_NAME+CONF_PREFIX
USER_CONF=USER_CONF_PATH+CONF_NAME+CONF_PREFIX
DEV_CONF=CONF_NAME+CONF_PREFIX

APP_NAME=CONF_NAME+"server"

DELAY=0.1
