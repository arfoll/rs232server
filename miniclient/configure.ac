#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.69])
AC_INIT([rs232 miniclient], [0.1], [brendan@fridu.net])
AM_INIT_AUTOMAKE(rs232_miniclient, 0.1)
AC_CONFIG_HEADERS([config.h])

# Checks for programs.
AC_PROG_LIBTOOL
AC_PROG_CC
AC_PROG_INSTALL
AM_PROG_CC_C_O
PKG_PROG_PKG_CONFIG

# Checks for libraries.
#AC_CHECK_LIB([dbus-1], [main], [ LIBS_LIB_DBUS="-ldbus-1"], [ echo "Libdbus-1 not found - exiting!"; exit 1 ])
PKG_CHECK_MODULES(DBUS, dbus-1)
PKG_CHECK_MODULES(NCURSES, ncursesw)

# Checks for header files.
AC_CHECK_HEADERS([stdint.h stdlib.h string.h termios.h unistd.h])

# Checks for typedefs, structures, and compiler characteristics.
AC_C_INLINE
AC_TYPE_SIZE_T
AC_TYPE_SSIZE_T

# Checks for library functions.
AC_FUNC_MALLOC
AC_FUNC_REALLOC
AC_CHECK_FUNCS([memmove strchr strdup strstr])

AC_CONFIG_FILES([src/Makefile libtermkey/Makefile])
AC_OUTPUT
