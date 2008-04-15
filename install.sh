#! /bin/sh

# If your distribution puts this in other locations, please adjust the values of
# these variables before installing!
# INIT_D=/etc/init.d
MAN_D=/usr/local/man/man8

if [ "$INIT_D" = "" ] ; then
	# Try non-link directories first, then try links. This helps if one of
	# the locations is linked to another, which is the case on some distros.
	if [ -d /etc/rc.d/init.d -a ! -L /etc/rc.d/init.d ] ; then
		INIT_D=/etc/rc.d/init.d
	elif [ -d /etc/rc.d -a ! -L /etc/rc.d -a ! -d /etc/rc.d/init.d ] ; then
		INIT_D=/etc/rc.d
	elif [ -d /etc/init.d -a ! -L /etc/init.d ] ; then
		INIT_D=/etc/init.d
	elif [ -d /etc/rc.d/init.d ] ; then
		INIT_D=/etc/rc.d/init.d
	elif [ -d /etc/rc.d ] ; then
		INIT_D=/etc/rc.d
	elif [ -d /etc/init.d ] ; then
		INIT_D=/etc/init.d
	else
		echo "Cannot determine location of init scripts. Please modify install.sh."
		exit 31
	fi
fi

if ( which invoke-rc.d > /dev/null ) ; then
	# Debian uses invoke-rc.d
	RCPROG=invoke-rc.d
	INITSCRIPT=laptop-mode
elif ( which service > /dev/null ) ; then
	# RedHat uses service
	RCPROG=service
	INITSCRIPT=laptop-mode
else
	# Any other -- we start it ourselves.
	RCPROG=
	INITSCRIPT=$INIT_D/laptop-mode
fi

if [ "`whoami`" != "root" ] ; then
	echo "You need to be root to install the laptop mode tools."
	exit 10
fi

if [ ! -f /proc/sys/vm/laptop_mode ] ; then
	echo "Warning: the kernel you are running does not support laptop mode."
fi

echo 'Stopping existing laptop mode service (if any).'
$RCPROG $INITSCRIPT stop

INSTALL="install -o root -g root"

mkdir -p /etc/laptop-mode /etc/laptop-mode/batt-start /etc/laptop-mode/batt-stop /etc/laptop-mode/lm-ac-start /etc/laptop-mode/lm-ac-stop /etc/laptop-mode/nolm-ac-start /etc/laptop-mode/nolm-ac-stop /usr/share/laptop-mode-tools/modules /etc/laptop-mode/conf.d /etc/laptop-mode/modules

ALREADY_EXISTED=0

if [ -f /etc/laptop-mode/laptop-mode.conf ] ; then
	echo "Not reinstalling configuration file: /etc/laptop-mode/laptop-mode.conf exists."
	ALREADY_EXISTED=1
elif ( ! $INSTALL -m 644 etc/laptop-mode/laptop-mode.conf /etc/laptop-mode ) ; then
	echo "$0: Failed to install configuration file in /etc/laptop-mode/laptop-mode.conf. Installation failed."
	exit 12
fi

if [ -f /etc/default/laptop-mode -a "$ALREADY_EXISTED" -eq 0 ] ; then
        echo "Found old configuration file in /etc/default/laptop-mode. Moving to the new location."
	if ( ! mv /etc/default/laptop-mode /etc/laptop-mode/laptop-mode.conf ) ; then
		echo "$0: Failed to move old configuration file to new location."
		exit 20
	fi
fi
if [ -f /etc/sysconfig/laptop-mode -a "$ALREADY_EXISTED" -eq 0 ] ; then
        echo "Found old configuration file in /etc/sysconfig/laptop-mode. Moving to the new location."
	if ( ! mv /etc/sysconfig/laptop-mode /etc/laptop-mode/laptop-mode.conf ) ; then
		echo "$0: Failed to move old configuration file to new location."
		exit 21
	fi
fi

for CONF in etc/laptop-mode/conf.d/* ; do
	if [ -f /"$CONF" ] ; then
		echo "Not reinstalling configuration file /$CONF."
	elif ( ! $INSTALL -m 600 "$CONF" /"$CONF" ) ; then
		echo "$0: Failed to install configuration file /$CONF. Installation failed."
		exit 12
	fi
done


if [ -f /etc/laptop-mode/lm-profiler.conf ] ; then
	echo "Configuration file /etc/laptop-mode/lm-profiler.conf already exists."
elif ( ! $INSTALL -m 600 etc/laptop-mode/lm-profiler.conf /etc/laptop-mode ) ; then
	echo "$0: Failed to install configuration file in /etc/laptop-mode/lm-profiler.conf. Installation failed."
	exit 12
fi


if ( ! $INSTALL -m 700 usr/sbin/laptop_mode /usr/sbin ) ; then
	echo "$0: Failed to install /usr/sbin/laptop_mode. Installation failed."
	exit 11
fi

if ( ! $INSTALL -m 700 usr/sbin/lm-syslog-setup /usr/sbin ) ; then
	echo "$0: Failed to install /usr/sbin/lm-syslog-setup. installation failed."
	exit 25
fi

if ( ! $INSTALL -m 700 usr/sbin/lm-profiler /usr/sbin ) ; then
	echo "$0: Failed to install /usr/sbin/lm-profiler. Installation failed."
	exit 11
fi

if ( ! $INSTALL -m 700 usr/share/laptop-mode-tools/modules/* /usr/share/laptop-mode-tools/modules ) ; then
	echo "$0: Failed to install modules into /usr/share/laptop-mode-tools/modules. Installation failed."
	exit 26
fi

if ( ! mkdir -p $MAN_D ) ; then
  echo "$0: Could not create directory $MAN_D. Installation failed."
  exit 22
fi
if ( ! cp man/* $MAN_D ) ; then
  echo "$0: Could not copy manual pages to $MAN_D. Installation failed."
  exit 23
fi

ACPI_DONE=0
if [ ! -d /proc/pmu -a -d /etc/acpi ] ; then
	mkdir -p /etc/acpi/actions
	mkdir -p /etc/acpi/events
	
	# Remove the old action scripts, but not the olddd event files. Apparently, Gentoo handles
	# its speedfreq using /etc/acpi/events/battery, and we were using that too. Simply removing
	# the scripts and leaving the event files will hopefully cause acpid to notice that the
	# files don't exist and leave it at that.
	rm -f /etc/acpi/actions/battery.sh /etc/acpi/actions/ac.sh
	
	if ( ! $INSTALL -m 700 etc/acpi/actions/* /etc/acpi/actions ) ; then
		echo "$0: Failed to install ACPI action scripts in /etc/acpi/actions. Installation failed."
		exit 13
	fi
	if ( ! $INSTALL -m 600 etc/acpi/events/* /etc/acpi/events ) ; then
		echo "$0: Failed to install ACPI event file in /etc/acpi/events. Installation failed."
		exit 14
	fi
	killall -HUP acpid
	echo "Installed ACPI support."
	ACPI_DONE=1
fi

APM_DONE=0
if [ ! -d /proc/pmu -a -d /etc/apm ] ; then
	mkdir -p /etc/apm/event.d
	if ( ! $INSTALL -m 700 etc/apm/event.d/* /etc/apm/event.d ) ; then
		echo "$0: Failed to install APM event script in /etc/apm/event.d. Installation failed."
		exit 15
	fi
	echo "Installed APM support."
	APM_DONE=1
fi

PMU_DONE=0
if [ -d /proc/pmu -a -d /etc/power ] ; then
	mkdir -p /etc/power/event.d /etc/power/scripts.d
	if ( ! $INSTALL -m 700 etc/power/scripts.d/laptop-mode /etc/power/scripts.d ) ; then
		echo "$0: Failed to install pbbuttonsd event script in /etc/power/scripts.d. Installation failed."
		exit 33
	fi
	if ( ! ln -fs ../scripts.d/laptop-mode /etc/power/event.d ) ; then
		echo "$0: Failed to install pbbuttonsd event script in /etc/power/event.d. Installation failed."
		exit 34
	fi
	if [ -f /etc/power/pwrctl ] ; then
		if ( ! grep pwrctl-local /etc/power/pwrctl ) ; then
			echo "WARNING: /etc/power/pwrctl does not call pwrctl-local. Laptop mode will not start automatically when you use pmud."
		fi
		touch /etc/power/pwrctl-local
		if ( ! grep laptop_mode /etc/power/pwrctl-local ) ; then
			(echo "#! /bin/sh" ; echo "/usr/sbin/laptop_mode auto" ; cat /etc/power/pwrctl-local) > /etc/power/pwrctl-local-tmp
			cat /etc/power/pwrctl-local-tmp /etc/power/pwrctl-local
			rm /etc/power/pwrctl-local-tmp
		else
			echo "/etc/power/pwrctl-local already seems to contain a laptop mode call. Not adding an extra one."
		fi
	fi
	if [ -f /etc/apm/event.d/laptop-mode ] ; then
		# This file interferes with the pbbuttonsd integration,
		# because pbbuttonsd also emulates APM, so we have to
		# remove it.
		rm /etc/apm/event.d/laptop-mode
	fi
	echo "Installed PMU (pmud/pbbuttonsd) support."
	PMU_DONE=1
fi

if [ $APM_DONE -eq 0 -a $ACPI_DONE -eq 0 -a $PMU_DONE -eq 0 ] ; then
	echo "ACPI/APM/PMU support was not found. Laptop mode will not start automatically."
	echo "Install either acpid, apmd, pbbuttonsd or pmud (depending on what your laptop supports) and reinstall."
fi

if [ -d $INIT_D ] ; then
  if ( ! $INSTALL -m 700 etc/init.d/laptop-mode $INIT_D ) ; then
    echo "$0: failed to install init script in $INIT_D. Installation failed."
    exit 16
  fi
  if [ -f /etc/rcS.d/S99laptop_mode ] ; then    
    # Old symlink.
    rm $RCS_D/S99laptop-mode
  fi
  if ( which update-rc.d > /dev/null ) ; then
    if ( ! update-rc.d laptop-mode defaults ) ; then
      echo "$0: update-rc.d failed, laptop mode will not be initialized at bootup."
      exit 17
    fi
  elif ( which chkconfig > /dev/null ) ; then
    if ( ! chkconfig laptop-mode on ) ; then
      echo "$0: chkconfig failed, laptop mode will not be initialized at bootup."
      exit 30
    fi
  fi
else
  echo "Directory $INIT_D not found: not installing script to initialize"
  echo "laptop mode at boot time."
fi

if ( ! mkdir -p $MAN_D ) ; then
  echo "$0: Could not create directory $MAN_D. Installation failed."
  exit 22
fi
if ( ! cp man/* $MAN_D ) ; then
  echo "$0: Could not copy manual pages to $MAN_D. Installation failed."
  exit 23
fi

if ( ! $RCPROG $INITSCRIPT start ) ; then
	echo "$0: Could not start laptop mode init script /etc/init.d/laptop-mode."
	exit 24
fi

echo "Installation complete."
