#! /bin/sh

test -f /lib/udev/lmt-udev || exit 0

# Automatically disable laptop mode when the battery almost runs out,
# and re-enable it when it
/lib/udev/lmt-udev
