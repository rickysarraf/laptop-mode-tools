#!/bin/sh
# Todo : after adding a new UI file to dialig, also add
#        its corresponding Ui_ script generator here
#

echo "Compiling Ui files"
pyuic4 LaptopModeTools.ui > Ui_LaptopModeTools.py

echo "Compiling Resources files"
pyrcc4 -o resources_rc.py resources.qrc
echo "Done"
