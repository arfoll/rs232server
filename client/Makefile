CC=gcc
CFLAGS=-g -Wall -I.
DEPS = 
PKG_CONFIG=`pkg-config --cflags --libs dbus-1`
OBJ = ampclient.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS) $(PKG_CONFIG)

ampclient: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(PKG_CONFIG)
clean:
	rm -f ampclient.o miniclient
