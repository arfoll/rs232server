/*
 *      Copyright (C) 2011 Brendan Le Foll <brendan@fridu.net>
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
#include <string.h>
#include <dbus/dbus.h>

int
main (int argc, char **argv)
{
  DBusConnection *connection;
  DBusError error;
  DBusMessage *message;

  const char* RS232SERVER_BUS_NAME = "uk.co.madeo.rs232server";
  const char* AZURSERVICE_IFACE = "uk.co.madeo.rs232server.azur";
  const char* AZURSERVICE_OBJ_PATH = "/uk/co/madeo/rs232server/azur";
  const dbus_int32_t db = 2;

  /* if we don't get any arguments exit */
  if (argc != 2) {
    fprintf (stderr, "%s needs an argument!\n", argv[0]);
    exit (1);
  }

  char method[15];

  if (strcmp(argv[1],"up") == 0) {
      strcpy(method, "volumeup");
  } else {
      strcpy(method, "volumedown");
  }

  dbus_error_init (&error);

  connection = dbus_bus_get (DBUS_BUS_SYSTEM, &error);
  if (connection == NULL) {
      fprintf(stderr, "Failed to open connection to bus: %s\n", error.message);
      dbus_error_free (&error);
      exit (1);
  }

  /* Construct the message */
  message = dbus_message_new_method_call (RS232SERVER_BUS_NAME, AZURSERVICE_OBJ_PATH, AZURSERVICE_IFACE, method); 
  /* append arguments */
  dbus_message_append_args (message, DBUS_TYPE_INT32, &db, DBUS_TYPE_INVALID);
  /* don't ask for a reply */
  dbus_message_set_no_reply(message, TRUE);
  /* send message & flush */
  dbus_connection_send (connection, message, NULL);
  dbus_connection_flush(connection);

  /* clean up */
  dbus_message_unref (message);
  dbus_connection_unref (connection);
  dbus_error_free (&error);

  return 0;
}
