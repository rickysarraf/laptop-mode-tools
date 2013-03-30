
default:
	@echo "Please specify a make target: install, clean, version."
	
clean:
	rm -f `find . -name \*~`

# Get the version from usr/sbin/laptop_mode.
VERSION :=$(shell cat usr/sbin/laptop_mode | grep "LMTVERSION=" | sed 's/LMTVERSION=//g')

version:
	@echo $(VERSION)

install:
	./install.sh
