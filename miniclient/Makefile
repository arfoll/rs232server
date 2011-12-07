CC=gcc
CFLAGS=-g -Wall -I.
DEPS = 
PKG_CONFIG=`pkg-config --cflags --libs dbus-1`
OBJ = miniclient.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS) $(PKG_CONFIG)

miniclient: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(PKG_CONFIG)
clean:
	rm -f miniclient.o miniclient
