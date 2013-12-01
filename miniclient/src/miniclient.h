/*
 *      Copyright (C) 2011, 2012 Brendan Le Foll <brendan@fridu.net>
 *      http://www.madeo.co.uk
 *
 *  This Program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2, or (at your option)
 *  any later version.
 *
 *  This Program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with ampserver; see the file COPYING.  If not, write to
 *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
 *  http://www.gnu.org/copyleft/gpl.html
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <errno.h>

#include <dbus/dbus.h>

#include <libxml/parser.h>
#include <libxml/tree.h>

#define SUCCESS 0
#define GENERAL_ERROR 1
#define GENERAL_DBUS_ERROR 2
#define GENERAL_XML_ERROR 3
#define ARG_PARSE_ERROR 4
#define CMD_EXIST_ERROR 5

#define RS232SERVER_BUS_NAME "uk.co.madeo.rs232server"
#define RS232SERVER_OBJ_PATH "/uk/co/madeo/rs232server"
#define RS232SERVER_METHOD "send_cmd"
#define INTROSPECT_IFACE "org.freedesktop.DBus.Introspectable"
#define INTROSPECT_METHOD "Introspect"

#define MAX_STR_SIZE 30
#define DBUS_REPLY_TIMEOUT 50000
#define REPEAT_NONE 1

