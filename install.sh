#! /bin/sh

#
# Laptop Mode Tools installer script
# ----------------------------------
#
# You can configure this installer script by setting the following environment
# variables:
#
# DESTDIR = destination root directory. Leave empty for /.
# INIT_D = destination init.d directory. Set to "none" to disable the
# installation of init scripts.
# MAN_D = directory in which the manual pages are to be installed. This should
# be the base directory, e.g. /usr/local/man.
# INSTALL = command line for install program. By default, this is set to
# "install -o root -g root".
#
# These settings enable / disable support for power management hardware and
# daemons:
#
# ACPI=force / disabled / auto
# PMU=force / disabled / auto
# APM=force / disabled / auto
#
# For each of these settings, "force" means: install the files even if the
# system doesn't support the daemon. "disabled" means: never install the files,
# and "auto" means: autodetect if this power management method is supported.
#

[ -z "$MAN_D" ] && MAN_D="/usr/man"
[ -z "$LIB_D" ] && LIB_D="/lib"
[ -z "$ULIB_D" ] && ULIB_D="/usr/lib"
[ -z "$UDEV_D" ] && UDEV_D="$LIB_D/udev"
[ -z "$SYSTEMD" ] && SYSTEMD="yes"
[ -z "$SYSTEMD_UNIT_D" ] && SYSTEMD_UNIT_D="$LIB_D/systemd/system"
[ -z "$TMPFILES_D" ] && TMPFILES_D="$ULIB_D/tmpfiles.d"

if [ -z "$ACPI" ] ; then
	ACPI=auto
	[ -n "$DESTDIR" ] && ACPI=force
fi
if [ -z "$APM" ] ; then
	APM=auto
	[ -n "$DESTDIR" ] && APM=force
fi
if [ -z "$PMU" ] ; then
	PMU=auto
	[ -n "$DESTDIR" ] && PMU=force
fi

if [ -z "$INIT_D" ] ; then
	# Try non-link directories first, then try links. This helps if one of
	# the locations is linked to another, which is the case on some distros.
	if [ -d "$DESTDIR/etc/rc.d/init.d" -a ! -L "$DESTDIR/etc/rc.d/init.d" ] ; then
		INIT_D="$DESTDIR/etc/rc.d/init.d"
	elif [ -d "$DESTDIR/etc/rc.d" -a ! -L "$DESTDIR/etc/rc.d" -a ! -d "$DESTDIR/etc/rc.d/init.d" ] ; then
		INIT_D="$DESTDIR/etc/rc.d"
	elif [ -d "$DESTDIR/etc/init.d" -a ! -L "$DESTDIR/etc/init.d" ] ; then
		INIT_D="$DESTDIR/etc/init.d"
	elif [ -d "$DESTDIR/etc/rc.d/init.d" ] ; then
		INIT_D="$DESTDIR/etc/rc.d/init.d"
	elif [ -d "$DESTDIR/etc/rc.d" ] ; then
		INIT_D="$DESTDIR/etc/rc.d"
	elif [ -d "$DESTDIR/etc/init.d" ] ; then
		INIT_D="$DESTDIR/etc/init.d"
	elif [ -n "$DESTDIR" ] ; then
		# We're going the package manager route -- make a guess, they
		# will adapt it if needed.
		INIT_D="$DESTDIR/etc/init.d"
	else
		echo "Cannot determine location of init scripts. Please modify install.sh."
		exit 31
	fi
fi

if [ "$INIT_D" != "none" ] ; then
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
		INITSCRIPT="$INIT_D/laptop-mode"
	fi
fi

if [ "`whoami`" != "root" -a -z "$DESTDIR" ] ; then
	echo "You need to be root to install laptop mode tools."
	exit 10
fi

if [ ! -f /proc/sys/vm/laptop_mode ] ; then
	echo "Warning: the kernel you are running does not support laptop mode."
fi

if [ "$INIT_D" != "none" -a -z "$DESTDIR" ] ; then
	echo 'Stopping existing laptop mode service (if any).'
	$RCPROG $INITSCRIPT stop
fi

if [ -z "$INSTALL" ]; then
	INSTALL="install -o root -g root"
fi

$INSTALL -d -m 755 "$DESTDIR/etc/laptop-mode"
$INSTALL -d -m 755 "$DESTDIR/etc/laptop-mode/batt-start"
$INSTALL -d -m 755 "$DESTDIR/etc/laptop-mode/batt-stop"
$INSTALL -d -m 755 "$DESTDIR/etc/laptop-mode/lm-ac-start"
$INSTALL -d -m 755 "$DESTDIR/etc/laptop-mode/lm-ac-stop"
$INSTALL -d -m 755 "$DESTDIR/etc/laptop-mode/nolm-ac-start"
$INSTALL -d -m 755 "$DESTDIR/etc/laptop-mode/nolm-ac-stop"
$INSTALL -d -m 755 "$DESTDIR/usr/share/laptop-mode-tools/modules"
$INSTALL -d -m 755 "$DESTDIR/usr/share/laptop-mode-tools/module-helpers"
$INSTALL -d -m 755 "$DESTDIR/etc/laptop-mode/conf.d"
$INSTALL -d -m 755 "$DESTDIR/etc/laptop-mode/modules"
$INSTALL -d -m 755 "$DESTDIR/usr/share/polkit-1/actions"
$INSTALL -d -m 755 "$DESTDIR/usr/share/applications"
$INSTALL -d -m 755 "$DESTDIR/usr/share/pixmaps"
$INSTALL -d -m 755 "$DESTDIR/usr/sbin"
$INSTALL -d -m 755 "$DESTDIR/$UDEV_D/rules.d"
$INSTALL -d -m 755 "$DESTDIR/$MAN_D/man8"

ALREADY_EXISTED=0

if [ -f "$DESTDIR/etc/laptop-mode/laptop-mode.conf" ] ; then
	echo "Not reinstalling configuration file: $DESTDIR/etc/laptop-mode/laptop-mode.conf exists."
	ALREADY_EXISTED=1
elif ( ! $INSTALL -m 644 etc/laptop-mode/laptop-mode.conf "$DESTDIR/etc/laptop-mode" ) ; then
	echo "$0: Failed to install configuration file in $DESTDIR/etc/laptop-mode/laptop-mode.conf. Installation failed."
	exit 12
fi

for CONF in etc/laptop-mode/conf.d/* ; do
	if [ -f "$DESTDIR/$CONF" ] ; then
		echo "Not reinstalling configuration file $DESTDIR/$CONF."
	elif ( ! $INSTALL -m 644 "$CONF" "$DESTDIR/$CONF" ) ; then
		echo "$0: Failed to install configuration file $DESTDIR/$CONF. Installation failed."
		exit 12
	fi
done


if [ -f "$DESTDIR/etc/laptop-mode/lm-profiler.conf" ] ; then
	echo "Configuration file $DESTDIR/etc/laptop-mode/lm-profiler.conf already exists."
elif ( ! $INSTALL -m 644 etc/laptop-mode/lm-profiler.conf "$DESTDIR/etc/laptop-mode" ) ; then
	echo "$0: Failed to install configuration file in $DESTDIR/etc/laptop-mode/lm-profiler.conf. Installation failed."
	exit 12
fi

if ( ! $INSTALL -m 755 usr/sbin/laptop_mode "$DESTDIR/usr/sbin" ) ; then
	echo "$0: Failed to install $DESTDIR/usr/sbin/laptop_mode. Installation failed."
	exit 11
fi

if ( ! $INSTALL -m 644 usr/share/polkit-1/actions/org.linux.lmt.gui.policy "$DESTDIR/usr/share/polkit-1/actions/" ) ; then
	echo "$0: Failed to install $DESTDIR/usr/share/polkit-1/actions/org.linux.lmt.gui.policy Installation failed."
	exit 11
fi

if ( ! $INSTALL -m 755 usr/sbin/lm-syslog-setup "$DESTDIR/usr/sbin" ) ; then
	echo "$0: Failed to install $DESTDIR/usr/sbin/lm-syslog-setup. installation failed."
	exit 25
fi

if ( ! $INSTALL -m 755 usr/sbin/lm-profiler "$DESTDIR/usr/sbin" ) ; then
	echo "$0: Failed to install $DESTDIR/usr/sbin/lm-profiler. Installation failed."
	exit 11
fi

if [ -f "$DESTDIR/usr/share/laptop-mode-tools/modules/core" ] ; then
	if ( ! rm "$DESTDIR/usr/share/laptop-mode-tools/modules/core" ) ; then
		echo "$0: Failed to install modules into /usr/share/laptop-mode-tools/modules. Installation failed."
		exit 35
	fi
fi		

if ( ! $INSTALL -m 755 usr/share/laptop-mode-tools/modules/* "$DESTDIR/usr/share/laptop-mode-tools/modules" ) ; then
	echo "$0: Failed to install modules into /usr/share/laptop-mode-tools/modules. Installation failed."
	exit 26
fi

if ( ! $INSTALL -m 755 usr/share/laptop-mode-tools/module-helpers/* "$DESTDIR/usr/share/laptop-mode-tools/module-helpers" ) ; then
	echo "$0: Failed to install module helpers into /usr/share/laptop-mode-tools/module-helpers. Installation failed."
	exit 37
fi

if ( ! $INSTALL -m 744 man/* "$DESTDIR/$MAN_D/man8" ) ; then
	echo "$0: Could not copy manual pages to $DESTDIR/$MAN_D/man8. Installation failed."
	exit 23
fi

if ( ! $INSTALL -m 644 gui/laptop-mode-tools.desktop "$DESTDIR/usr/share/applications" ) ; then
	echo "$0: Failed to install $DESTDIR/usr/share/applications/laptop-mode-tools.desktop"
	exit 11
fi

if ( ! $INSTALL -m 755 gui/lmt-config-gui* "$DESTDIR/usr/sbin" ) ; then
	echo "$0: Failed to install $DESTDIR/usr/sbin/lmt-config-gui*"
	exit 11
fi

if ( ! $INSTALL -m 644 gui/laptop-mode-tools.svg "$DESTDIR/usr/share/pixmaps" ) ; then
	echo "$0: Failed to install $DESTDIR/usr/share/pixmaps/laptop-mode-tools.svg";
	exit 11
fi

if ( ! $INSTALL -m 644 gui/LMT.py "$DESTDIR/usr/share/laptop-mode-tools" ) ; then
	echo "$0: Failed to install $DESTDIR/usr/share/laptop-mode-tools/lmt.py";
	exit 11
fi

# Install pm-utils hook only if pm-utils config dir is present, or force the
# install if we have a DESTDIR.
if [ -n "$DESTDIR" -o -d "$DESTDIR/$ULIB_D/pm-utils/sleep.d" ] ; then
	if ( ! $INSTALL -D -m 755 usr/lib/pm-utils/sleep.d/01laptop-mode "$DESTDIR/$ULIB_D/pm-utils/sleep.d/01laptop-mode" ) ; then
		echo "$0: Failed to install 01-laptop-mode into $ULIB_D/pm-utils/sleep.d. Installation failed."
		exit 36
	fi
fi

if [ -f "$DESTDIR/$ULIB_D/pm-utils/sleep.d/99laptop-mode" ]; then
	rm -f $DESTDIR/$ULIB_D/pm-utils/sleep.d/99laptop-mode;
fi

# udev rule
if ( ! $INSTALL -D -m 644 etc/rules/99-laptop-mode.rules "$DESTDIR/$UDEV_D/rules.d/99-laptop-mode.rules" ) ; then
	echo "$0: Failed to install udev rule into $UDEV_D/rules.d/ Installation failed."
	exit 23
fi

# udev helper tool
if ( ! $INSTALL -D -m 755 etc/rules/lmt-udev "$DESTDIR/$UDEV_D/lmt-udev" ) ; then
	echo "$0: Failed to install udev helper tool into $UDEV_D Installation failed."
fi

if [ "${SYSTEMD}" = "yes" ]; then
	$INSTALL -d -m 755 "$DESTDIR/$SYSTEMD_UNIT_D"
	$INSTALL -d -m 755 "$DESTDIR/$TMPFILES_D"

	# systemd service
	if ( ! $INSTALL -D -m 644 etc/systemd/laptop-mode.service "$DESTDIR/$SYSTEMD_UNIT_D/laptop-mode.service" ) ; then
		echo "$0: Failed to install systemd service into $SYSTEMD_UNIT_D Installation failed."
	fi

	# timer file
	if ( ! $INSTALL -D -m 644 etc/systemd/laptop-mode.timer "$DESTDIR/$SYSTEMD_UNIT_D/laptop-mode.timer" ) ; then
		echo "$0: Failed to install systemd timer into $SYSTEMD_UNIT_D Installation failed."
	fi

	# and timer's calling service file
	if ( ! $INSTALL -D -m 644 etc/systemd/lmt-poll.service "$DESTDIR/$SYSTEMD_UNIT_D/lmt-poll.service" ) ; then
		echo "$0: Failed to install systemd poll service into $SYSTEMD_UNIT_D Installation failed."
	fi

	# and systemd's tmpfiles.d
	if ( ! $INSTALL -D -m 644 etc/systemd/laptop-mode.conf.tmpfiles "$DESTDIR/${TMPFILES_D}/laptop-mode.conf" ) ; then
		echo "$0: Failed to install systemd tmpfiles into ${TMPFILES_D} Installation failed."
	fi
fi

ACPI_DONE=0
APM_DONE=0
PMU_DONE=0

if [ "$ACPI" = "force" ] || [ "$ACPI" = "enabled" -a ! -d /proc/pmu -a -d "$DESTDIR/etc/acpi" ] ; then
	$INSTALL -d -m 755 "$DESTDIR/etc/acpi/actions"
	$INSTALL -d -m 755 "$DESTDIR/etc/acpi/events"
	
	# Remove the old action scripts, but not the old event files. Apparently, Gentoo handles
	# its speedfreq using /etc/acpi/events/battery, and we were using that too. Simply removing
	# the scripts and leaving the event files will hopefully cause acpid to notice that the
	# files don't exist and leave it at that.
	rm -f "$DESTDIR/etc/acpi/actions/battery.sh" "$DESTDIR/etc/acpi/actions/ac.sh"
	
	if ( ! $INSTALL -m 755 etc/acpi/actions/* "$DESTDIR/etc/acpi/actions" ) ; then
		echo "$0: Failed to install ACPI action scripts in $DESTDIR/etc/acpi/actions. Installation failed."
		exit 13
	fi
	if ( ! $INSTALL -m 644 etc/acpi/events/* "$DESTDIR/etc/acpi/events" ) ; then
		echo "$0: Failed to install ACPI event file in $DESTDIR/etc/acpi/events. Installation failed."
		exit 14
	fi
	if [ -z "$DESTDIR" ] ; then
		killall -HUP acpid
	fi
	echo "Installed ACPI support."
	ACPI_DONE=1
fi

if [ "$APM" = "force" ] || [ "$APM" = "enabled" -a ! -d /proc/pmu -a -d /etc/apm ] ; then
	$INSTALL -d -m 755 "$DESTDIR/etc/apm/event.d"
	if ( ! $INSTALL -m 755 etc/apm/event.d/* "$DESTDIR/etc/apm/event.d" ) ; then
		echo "$0: Failed to install APM event script in $DESTDIR/etc/apm/event.d. Installation failed."
		exit 15
	fi
	echo "Installed APM support."
	APM_DONE=1
fi

if [ "$PMU" = "force" ] || [ "$PMU" = "enabled" -a -d /proc/pmu -a -d /etc/power ] ; then
	$INSTALL -d -m 755 "$DESTDIR/etc/power/event.d"
	$INSTALL -d -m 755 "$DESTDIR/etc/power/scripts.d"
	if ( ! $INSTALL -m 755 etc/power/scripts.d/laptop-mode "$DESTDIR/etc/power/scripts.d" ) ; then
		echo "$0: Failed to install pbbuttonsd event script in $DESTDIR/etc/power/scripts.d. Installation failed."
		exit 33
	fi
	if ( ! ln -fs ../scripts.d/laptop-mode "$DESTDIR/etc/power/event.d" ) ; then
		echo "$0: Failed to install pbbuttonsd event script in $DESTDIR/etc/power/event.d. Installation failed."
		exit 34
	fi
	if [ -f "$DESTDIR/etc/power/pwrctl" ] ; then
		if ( ! grep pwrctl-local "$DESTDIR/etc/power/pwrctl" ) ; then
			echo "WARNING: "$DESTDIR/etc/power/pwrctl" does not call pwrctl-local. Laptop mode will not start automatically when you use pmud."
		fi
		if [ ! -f "$DESTDIR/etc/power/pwrctl-local" ] ; then
			echo >> "$DESTDIR/etc/power/pwrctl-local"
		fi
		if ( ! grep laptop_mode "$DESTDIR/etc/power/pwrctl-local" ) ; then
			if (! grep -q "#\!"  "$DESTDIR/etc/power/pwrctl-local" ); then
				sed -i -e "1i\\#! /bin/sh" "$DESTDIR/etc/power/pwrctl-local"
			fi
			sed -i -e "2i\\/usr/bin/laptop_mode auto" "$DESTDIR/etc/power/pwrctl-local"
		else
			echo "/etc/power/pwrctl-local already seems to contain a laptop mode call. Not adding an extra one."
		fi
	fi
	if [ -f "$DESTDIR/etc/apm/event.d/laptop-mode" -a -z "$DESTDIR" ] ; then
		# This file interferes with the pbbuttonsd integration,
		# because pbbuttonsd also emulates APM, so we have to
		# remove it.
		
		# We don't do this when DESTDIR != "", because that means we're
		# doing an install for a package manager.
		rm "$DESTDIR/etc/apm/event.d/laptop-mode"
	fi
	echo "Installed PMU (pmud/pbbuttonsd) support."
	PMU_DONE=1
fi

if [ $APM_DONE -eq 0 -a $ACPI_DONE -eq 0 -a $PMU_DONE -eq 0 ] ; then
	echo "ACPI/APM/PMU support was not installed. Laptop mode will not start automatically."
	echo "Install either acpid, apmd, pbbuttonsd or pmud (depending on what your laptop supports) and reinstall."
fi

if [ "$INIT_D" != "none" ] ; then
	if [ -d "$INIT_D" -o -n "$DESTDIR" ] ; then
		$INSTALL -d -m 755 "$INIT_D"
		if ( ! $INSTALL -m 755 etc/init.d/laptop-mode "$INIT_D" ) ; then
			echo "$0: failed to install init script in $INIT_D. Installation failed."
			exit 16
		fi
		if [ -f "$DESTDIR/etc/rcS.d/S99laptop_mode" ] ; then
			# Old symlink.
			rm "$DESTDIR/etc/rcS.d/S99laptop-mode"
		fi
		if [ -z "$DESTDIR" ] ; then
			if ( which update-rc.d > /dev/null ) ; then
				update-rc.d -f laptop-mode remove
				if ( ! update-rc.d laptop-mode defaults 99 ) ; then
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
			# Package manager's route: don't install the init script for
			# any particular runlevels. Since we don't have chkconfig or
			# update-rc.d available, we can't know for sure how this should
			# be done.
			/bin/true		
		fi
	else
		echo "Directory $INIT_D not found: not installing script to initialize"
		echo "laptop mode at boot time."
	fi

	if [ -z "$DESTDIR" ] ;then
		if ( ! $RCPROG $INITSCRIPT start ) ; then
			echo "$0: Could not start laptop mode init script /etc/init.d/laptop-mode."
			exit 24
		fi
	fi

	# Check for acpid and restart if running
	acpi_pid=`pidof acpid`
	if [ ! -z $acpi_pid ]; then
		echo "Reloading acpid daemon"
		killall -SIGHUP acpid;
	fi

	apm_pid=`pidof apmd`
	if [ ! -z $apm_pid ]; then
		echo "Reloading apmd daemon"
		killall -SIGHUP apmd;
	fi

	pbbuttonsd_pid=`pidof pbbuttonsd`
	if [ ! -z $pbbuttonsd_pid ]; then
		echo "Reloading pbbuttonsd daemon"
		killall -SIGHUP pbbuttonsd;
	fi

	pmud_pid=`pidof pmud`
	if [ ! -z $pmud_pid ]; then
		echo "Reloading pmud daemon"
		killall -SIGHUP pmud;
	fi
fi

echo "Installation complete."
