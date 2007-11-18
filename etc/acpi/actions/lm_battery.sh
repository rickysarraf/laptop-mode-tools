#! /bin/bash

test -f /usr/sbin/laptop_mode || exit 0

# Automatically disable laptop mode when the battery almost runs out,
# and re-enable it when it 

/usr/sbin/laptop_mode auto
