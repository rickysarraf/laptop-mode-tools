#! /bin/sh

test -f /usr/sbin/laptop_mode || exit 0

# lid button pressed/released event handler

/usr/sbin/laptop_mode auto
