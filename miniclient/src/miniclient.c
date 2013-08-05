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

#include "miniclient.h"

void
print_help ()
{
  fprintf(stdout, "Usage:\n miniclient <service> <command> [repeat]\n");
  fprintf(stdout, "Services supported:\n azur\n lgtv\n pioneer\n");
  fprintf(stdout, "Use miniclient <service> help to get a list of commands supported by services\n");
}

int
send_message_via_dbus (const char *method, const int repeat, char *obj, char *iface)
{
  DBusConnection *connection;
  DBusError error;
  DBusMessage *message;
  DBusMessage *reply;
  dbus_bool_t direct = 0;

  if (repeat == 1) {
    direct = 1;
  }

  dbus_error_init (&error);

  connection = dbus_bus_get (DBUS_BUS_SYSTEM, &error);
  if (connection == NULL) {
    fprintf(stderr, "Failed to open connection to bus: %s\n", error.message);
    dbus_error_free (&error);
    return GENERAL_DBUS_ERROR;
  }

  /* Construct the message */
  message = dbus_message_new_method_call (RS232SERVER_BUS_NAME, obj, iface, "send_cmd");
  /* append arguments */
  dbus_message_append_args (message, DBUS_TYPE_STRING, &method, DBUS_TYPE_INT32, &repeat, DBUS_TYPE_BOOLEAN, &direct, DBUS_TYPE_INVALID);
#if 0
  /* don't ask for a reply */
  dbus_message_set_no_reply(message, TRUE);
#endif
  /* send message & flush */
  reply = dbus_connection_send_with_reply_and_block (connection, message, DBUS_REPLY_TIMEOUT, &error);
  
  if (reply != NULL && direct) {
    DBusMessageIter args;
    int type;
    if (dbus_message_iter_init(reply, &args)) {
      do {
        type = dbus_message_iter_get_arg_type (&args);
	if (type == DBUS_TYPE_STRING) {
	  char *replyContent = NULL;
	  dbus_message_iter_get_basic(&args, &replyContent);
          printf("%s\n", replyContent);
	}
      } while (dbus_message_iter_has_next(&args));
    }
  }

  if (reply)
    dbus_message_unref (reply);
  dbus_connection_flush(connection);
  /* clean up */
  dbus_message_unref (message);
  dbus_connection_unref (connection);
  dbus_error_free (&error);

  /* make sure the line is clear when sending repeat messages and not collecting responses over serial */
  if (!direct)
    send_message_via_dbus ("clear", 1, obj, iface);

  return SUCCESS; 
}

int
send_service (const char *service, const char *method, const int repeat)
{
  char objpath[255];
  char iface[255];
  strcpy(iface, RS232SERVER_BUS_NAME);
  strcat(iface, ".");
  strcat(iface, service);
  strcpy(objpath, RS232SERVER_OBJ_PATH);
  strcat(objpath, "/");
  strcat(objpath, service);
  fprintf(stdout, "Using service %s on Obj %s and iface %s\n", service, objpath, iface);
  return send_message_via_dbus (method, repeat, &objpath, &iface);
}

// expecting something like ./miniclient azur voldown 5
int
main (const int argc, const char **argv)
{
  unsigned int repeat;
  const char *method;
  const char *service;

  /* if we don't get any arguments exit */
  if (argc < 3) {
    fprintf (stderr, "%s invalid arguments!\n", argv[0]);
    print_help();
    return (ARG_PARSE_ERROR);
  }

  service = argv[1];
  method = argv[2];
  if (argc == 3) {
    repeat = 1;
  } else {
    char *endptr;
    unsigned int n;
    errno = 0;
    n = strtol(argv[3], &endptr, 10);
    if (*endptr == '\0' && n > 0) {
      repeat = n;
    } else {
      repeat = 1;
      fprintf (stderr, "error in string conversion, repeat set to 1.\n");
    }
  }

  //fprintf (stderr, "service = %s, method = %s, repeat = %d\n", service, method, repeat);
  return send_service(service, method, repeat);
}
