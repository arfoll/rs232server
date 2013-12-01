/*
 *      Copyright (C) 2011 - 2013 Brendan Le Foll <brendan@fridu.net>
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

static void
print_help ()
{
  fprintf(stdout, "Usage:\n miniclient <service> <command> [repeat]\n");
  fprintf(stdout, "Use miniclient list to get a list of currently loaded services\n");
  fprintf(stdout, "Use miniclient <service> help to get a list of commands supported by services\n");
}

static int
parse_instropect_xml(char *data)
{
  unsigned int services = 0;

  // parse using libxml2 our returned dbus string
  xmlDoc *doc = xmlParseMemory(data, strlen(data));
  if (doc == NULL) {
    fprintf(stderr, "Failed to parse dbus instrospect data\n");
    return GENERAL_XML_ERROR;
  }

  xmlNode *root_node = xmlDocGetRootElement(doc);
  // only interested in the direct children of the root node
  xmlNode *cur_node = root_node->children;

  for (; cur_node; cur_node = cur_node->next) {
    if (cur_node->type == XML_ELEMENT_NODE) {
      xmlAttr *attr = cur_node->properties;
      // we only care about the first attribute
      if (attr && strcmp(attr->name, "name") == 0) {
        printf("%s\n", attr->children->content);
        services++;
      }
    }
  }

  if (services == 0)
    printf("rs232services has no services loaded\n");

  xmlFreeDoc(doc);
  xmlCleanupParser();
  return SUCCESS;
}

int
instrospect_bus ()
{
  DBusConnection *connection;
  DBusError error;
  DBusMessage *message;
  DBusMessage *reply;
  int ret = SUCCESS;

  dbus_error_init (&error);

  connection = dbus_bus_get (DBUS_BUS_SYSTEM, &error);
  if (connection == NULL) {
    fprintf(stderr, "Failed to open connection to bus: %s\n", error.message);
    dbus_error_free (&error);
    return GENERAL_DBUS_ERROR;
  }

  /* Construct the message */
  message = dbus_message_new_method_call (RS232SERVER_BUS_NAME, RS232SERVER_OBJ_PATH, INTROSPECT_IFACE, INTROSPECT_METHOD);
  /* send message & flush */
  reply = dbus_connection_send_with_reply_and_block (connection, message, DBUS_REPLY_TIMEOUT, &error);

  if (reply != NULL) {
    DBusMessageIter args;
    int type;
    if (dbus_message_iter_init(reply, &args)) {
      do {
        type = dbus_message_iter_get_arg_type (&args);
	if (type == DBUS_TYPE_STRING) {
	  char *replyContent = NULL;
	  dbus_message_iter_get_basic(&args, &replyContent);
          ret = parse_instropect_xml(replyContent);
	} else {
          printf("Received unexpected dbus reply type: (%d)\n", type);
        }
      } while (dbus_message_iter_has_next(&args));
    }
  } else {
    fprintf(stderr, "We got a dbus timeout, no reply received :(\n");
  }

  if (reply)
    dbus_message_unref (reply);
  dbus_connection_flush(connection);
  /* clean up */
  dbus_message_unref (message);
  dbus_connection_unref (connection);
  dbus_error_free (&error);

  return ret;
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
  message = dbus_message_new_method_call (RS232SERVER_BUS_NAME, obj, iface, RS232SERVER_METHOD);
  /* append arguments */
  dbus_message_append_args (message, DBUS_TYPE_STRING, &method, DBUS_TYPE_INT32, &repeat, DBUS_TYPE_BOOLEAN, &direct, DBUS_TYPE_INVALID);
  /* send message & flush */
  reply = dbus_connection_send_with_reply_and_block (connection, message, DBUS_REPLY_TIMEOUT, &error);
  
//  fprintf(stderr, "Dbus returned: %s\n", error);

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
	} else {
          printf("Received unexpected dbus reply type: (%d)\n", type);
        }
      } while (dbus_message_iter_has_next(&args));
    }
  } else if (reply == NULL && direct) {
    fprintf(stderr, "We got a dbus timeout, no reply received :(\n");
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
  //fprintf(stdout, "Using service %s on Obj %s and iface %s\n", service, objpath, iface);
  return send_message_via_dbus (method, repeat, &objpath, &iface);
}

// expecting something like ./miniclient azur voldown 5
int
main (const int argc, const char **argv)
{
  unsigned int repeat;
  const char *method;
  const char *service;

  service = argv[1];
  method = argv[2];

  /* if we don't get any arguments exit */
  if (argc == 2 && (strcmp(service, "list") == 0)) {
    return instrospect_bus();
  } else if (argc < 3) {
    fprintf (stderr, "%s invalid arguments!\n", argv[0]);
    print_help();
    return (ARG_PARSE_ERROR);
  }

  if (argc == 3) {
    repeat = REPEAT_NONE;
  } else {
    char *endptr;
    unsigned int n;
    errno = 0;
    n = strtol(argv[3], &endptr, 10);
    if (*endptr == '\0' && n > 0) {
      repeat = n;
    } else {
      repeat = REPEAT_NONE;
      fprintf (stderr, "error in string conversion, repeat set to %d.\n", REPEAT_NONE);
    }
  }

  //fprintf (stderr, "service = %s, method = %s, repeat = %d\n", service, method, repeat);
  return send_service(service, method, repeat);
}
