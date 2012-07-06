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
#include <termios.h>
#include <unistd.h>
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
print_help ()
{
  fprintf(stdout, "miniclient for rs232server\n");
  fprintf(stdout, "Commands supported are : volup, voldown, osd\n");
}

int
send_message_via_dbus (const char *method, const int repeat, char *obj, char *iface)
{
  DBusConnection *connection;
  DBusError error;
  DBusMessage *message;
//  const dbus_int32_t repeat = 1;
  const dbus_bool_t reply = 0;

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
  dbus_message_append_args (message, DBUS_TYPE_STRING, &method, DBUS_TYPE_INT32, &repeat, DBUS_TYPE_BOOLEAN, &reply, DBUS_TYPE_INVALID);
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
send_azur_service (const char *method, const int repeat)
{
  return send_message_via_dbus (method, repeat, AZURSERVICE_OBJ_PATH, AZURSERVICE_IFACE);
}

int
send_alsa_service (const char *method, const int repeat)
{
  return send_message_via_dbus (method, repeat, ALSASERVICE_OBJ_PATH, ALSASERVICE_IFACE);  
}

int
osd_direct ()
{
  int c;
  static struct termios oldt, newt;

  /* tcgetattr gets the parameters of the current terminal
     STDIN_FILENO will tell tcgetattr that it should write the settings
     of stdin to oldt*/
  tcgetattr(STDIN_FILENO, &oldt);

  /* Now the settings will be copied */
  newt = oldt;

  /* ICANON normally takes care that one line at a time will be processed
     that means it will return if it sees a "\n" or an EOF or an EOL */
  newt.c_lflag &= ~(ICANON);          

  /* Those new settings will be set to STDIN
     TCSANOW tells tcsetattr to change attributes immediately */
  tcsetattr(STDIN_FILENO, TCSANOW, &newt);

  /* 'e' ends input. Notice that EOF is also turned off in the non-canonical mode */
  while((c=getchar())!= 'e')
    switch (c) {
      case 72:
        send_azur_service("osdup", 1);
        break;
      case 80:
        send_azur_service("osddown", 1);
        break;
      case 77:
        send_azur_service("osdleft", 1);
        break;
      case 75:
        send_azur_service("osdright", 1);
        break;
      case 13:
        send_azur_service("osdenter", 1);
        break;
      default:
        break;
    }

  /* Restore the old settings */
  tcsetattr(STDIN_FILENO, TCSANOW, &oldt);

  return SUCCESS;
}

int
main (const int argc, const char **argv)
{
  int repeat;

  /* if we don't get any arguments exit */
  if (argc < 2) {
    fprintf (stderr, "%s needs a single argument!\n", argv[0]);
    print_help();
    return (ARG_PARSE_ERROR);
  }

  if (argc == 2) {
    repeat = 1;
  } else {
    repeat = atoi(argv[2]);
  }

  char *str = argv[1];

  if (strcmp(str, "osd") == 0)
      return osd_direct();
  else {
      return send_azur_service(str, repeat);
  }
/*  else {
      print_help();
      return (CMD_EXIST_ERROR);
  } */
}
