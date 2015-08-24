#! /bin/sh

test -f /lib/udev/lmt-udev || exit 0

# ac on/offline event handler
/lib/udev/lmt-udev
