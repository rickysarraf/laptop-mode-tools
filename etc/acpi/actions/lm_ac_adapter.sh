#! /bin/sh

test -f /usr/sbin/laptop_mode || exit 0

# ac on/offline event handler

/usr/sbin/laptop_mode auto
