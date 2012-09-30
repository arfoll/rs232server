#!/bin/sh
[ -e config.cache ] && rm -f config.cache

libtoolize --automake
aclocal
autoconf
autoheader
automake -a
exit

