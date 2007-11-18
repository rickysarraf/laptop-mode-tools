
default:
	@echo "Please specify a make target: install, dist, clean."
	
clean:
	rm -f `find . -name \*~`

# Get the version from usr/sbin/laptop_mode.
VERSION :=$(shell cat usr/sbin/laptop_mode | grep "LMTVERSION=" | sed 's/LMTVERSION=//g')

version:
	@echo $(VERSION)

dist:
	rm -rf ../dist/laptop-mode-tools-$(VERSION)
	mkdir -p ../dist/laptop-mode-tools-$(VERSION)
	cp -a * ../dist/laptop-mode-tools-$(VERSION)
	@# Remove Subversion stuff before distributing! 
	rm -rf `find ../dist/laptop-mode-tools-$(VERSION) -name .svn`
	cd ../dist && tar cvzf laptop-mode-tools_$(VERSION).tar.gz laptop-mode-tools-$(VERSION)
	rm -rf ../dist/laptop-mode-tools-$(VERSION)
	# If you need to do some stuff after a release, but you don't want to make this
	# public, put a laptop-mode-tools-postmakedist somewhere in your path.
	if [ `which laptop-mode-tools-postmakedist` ] ; then laptop-mode-tools-postmakedist $(VERSION) ; fi

install:
	./install.sh
