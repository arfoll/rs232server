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
#include <string.h>
#include <dbus/dbus.h>

#define SUCCESS 0
#define GENERAL_ERROR 1
#define GENERAL_DBUS_ERROR 2
#define ARG_PARSE_ERROR 3
#define CMD_EXIST_ERROR 4

#define RS232SERVER_BUS_NAME "uk.co.madeo.rs232server"
#define AZURSERVICE_IFACE "uk.co.madeo.rs232server.azur"
#define AZURSERVICE_OBJ_PATH "/uk/co/madeo/rs232server/azur"
#define ALSASERVICE_IFACE "uk.co.madeo.rs232server.alsa"
#define ALSASERVICE_OBJ_PATH "/uk/co/madeo/rs232server/alsa"

#define MAX_STR_SIZE 30

void
print_help()
{
  fprintf(stdout, "miniclient for rs232server\n");
  fprintf(stdout, "Commands supported are : up, down, headphonemodeon, headphonemodeoff\n");
}

int
send_message_via_dbus(char *method, char *obj, char *iface)
{
  DBusConnection *connection;
  DBusError error;
  DBusMessage *message;
  const dbus_int32_t db = 2;

  dbus_error_init (&error);

  connection = dbus_bus_get (DBUS_BUS_SYSTEM, &error);
  if (connection == NULL) {
      fprintf(stderr, "Failed to open connection to bus: %s\n", error.message);
      dbus_error_free (&error);
      return GENERAL_DBUS_ERROR;
  }

  /* Construct the message */
  message = dbus_message_new_method_call (RS232SERVER_BUS_NAME, obj, iface, method);
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

  return SUCCESS; 
}

int
send_azur_service(char *method)
{
  return send_message_via_dbus (method, AZURSERVICE_OBJ_PATH, AZURSERVICE_IFACE);
}

int
send_alsa_service(char *method)
{
  return send_message_via_dbus (method, ALSASERVICE_OBJ_PATH, ALSASERVICE_IFACE);  
}

int
main (int argc, char **argv)
{
  /* if we don't get any arguments exit */
  if (argc != 2) {
    fprintf (stderr, "%s needs a single argument!\n", argv[0]);
    print_help();
    return (ARG_PARSE_ERROR);
  }

  char method[MAX_STR_SIZE];
  char *str = argv[1];

  if (strcmp(str, "up") == 0) {
      strcpy(method, "volumeup");
      return send_azur_service (method);
  }
  else if (strcmp(str, "down") == 0) {
      strcpy(method, "volumedown");
      return send_azur_service (method);
  }
  else if (strcmp(str, "headphonemodeon") == 0)
      return send_alsa_service (str);
  else if (strcmp(str, "headphonemodeoff") == 0)
      return send_alsa_service (str);
  else {
      print_help();
      return (CMD_EXIST_ERROR);
  }
}
