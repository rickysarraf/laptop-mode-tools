#! /bin/bash

lang=$LANG
locale=`echo ${lang%%.*}`

pylupdate5 gui/lmt.py -ts -noobsolete -verbose gui/$locale.ts
mv gui/$locale.ts usr/share/laptop-mode-tools/locale/

