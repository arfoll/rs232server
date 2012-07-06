lib_LTLIBRARIES = libtermkey.la
libtermkey_la_SOURCES = termkey.c \
			termkey.h \
			termkey-internal.h \
			driver-csi.c \
			driver-ti.c

libtermkey_la_CFLAGS = $(NCURSES_CFLAGS) -std=c99
libtermkey_la_LIBADD = $(NCURSES_LIBS)
