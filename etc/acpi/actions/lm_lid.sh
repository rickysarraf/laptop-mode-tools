#! /bin/sh

test -f /lib/udev/lmt-udev || exit 0

# lid button pressed/released event handler
/lib/udev/lmt-udev
