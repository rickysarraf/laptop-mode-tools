# Authority: dag
# Upstream: Ritesh Raj Sarraf <rrs@researchut.com>

Summary: Tools for power savings based on battery/AC status
Name: laptop-mode-tools
Version: 1.69
Release: 1
License: GPL
Group: System Environment/Base
URL: http://github.com/rickysarraf/laptop-mode-tools
Vendor: Laptop Mode Tools Developers
Distribution: RPM Based distributions
Packager: Ritesh Raj Sarraf <rrs@researchut.com>

Source: http://www.samwel.tk/laptop_mode/tools/downloads/laptop-mode-tools_%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

%description
Laptop mode is a Linux kernel feature that allows your laptop to save
considerable power, by allowing the hard drive to spin down for longer
periods of time. This package contains the userland scripts that are
needed to enable laptop mode. It includes support for automatically
enabling laptop mode when the computer is working on batteries. In
addition, it provides a set of modules which allow you to apply
various other power savings.

%prep
%setup -n %{name}_%{version}

%build

%{__rm} -rf %{buildroot}

DESTDIR=%{buildroot} INIT_D="" MAN_D=%{_mandir} INSTALL=install ./install.sh

# Work around bug in installer. It installs the script in the wrong location if INIT_D="".
rm %{buildroot}/etc/init.d/laptop-mode

%{__mkdir_p} -m0755 %{buildroot}%{_initrddir}
%{__install} -Dp -m755 etc/init.d/laptop-mode %{buildroot}%{_initrddir}

%clean
%{__rm} -rf %{buildroot}

%preun
if [ $1 -eq 0 ]; then
	/sbin/service laptop-mode stop &>/dev/null || :
	/sbin/chkconfig --del laptop-mode
fi

%post
/sbin/chkconfig --add laptop-mode
/sbin/service laptop-mode start &>/dev/null || :
/sbin/service acpid restart &>/dev/null || :

%postun
/sbin/service laptop-mode condrestart &>/dev/null || :

%files
%defattr(-, root, root, 0755)

%doc COPYING Documentation/*.txt README.md
%docdir %{_mandir}
%doc %{_mandir}/man8/laptop-mode.conf.8
%doc %{_mandir}/man8/laptop_mode.8
%doc %{_mandir}/man8/lm-profiler.8
%doc %{_mandir}/man8/lm-profiler.conf.8
%doc %{_mandir}/man8/lm-syslog-setup.8
%config %{_sysconfdir}/acpi/actions/lm_*.sh
%config %{_sysconfdir}/acpi/events/lm_*
%config(noreplace) %{_sysconfdir}/laptop-mode/
%config %{_initrddir}/laptop-mode
/lib/udev/lmt-udev
/lib/systemd/system/laptop-mode.service
/lib/systemd/system/laptop-mode.timer
/lib/systemd/system/lmt-poll.service
/lib/udev/rules.d/99-laptop-mode.rules

%{_sysconfdir}/apm/event.d/*
%{_sysconfdir}/power/scripts.d/*
%{_sysconfdir}/power/event.d/*
#%{_usr}/sbin/*
%{_sbindir}/*
%{_usr}/share/laptop-mode-tools/modules/*
%{_usr}/share/laptop-mode-tools/module-helpers/*
%{_usr}/share/polkit-1/actions/org.linux.lmt.gui.policy
%{_usr}/lib/pm-utils/sleep.d/*
%{_usr}/lib/tmpfiles.d/laptop-mode.conf


%dir %{_sysconfdir}/acpi/events
%dir %{_sysconfdir}/acpi/actions
%dir %{_usr}/lib/pm-utils/sleep.d
%dir %{_usr}/lib/tmpfiles.d
%dir %{_usr}/share/laptop-mode-tools/modules
%dir %{_usr}/share/laptop-mode-tools/module-helpers
%dir %{_sysconfdir}/apm/event.d
%dir %{_sysconfdir}/power/scripts.d
%dir %{_sysconfdir}/power/event.d


%changelog
* Mon Mar  7 2016 Ritesh Raj Sarraf <rrs@researchut.com> - 1.69-1
- Updated to release 1.69

* Sun Sep 27 2015 Ritesh Raj Sarraf <rrs@researchut.com> - 1.68.1-1
- Updated to release 1.68.1

* Thu Aug 27 2015 Ritesh Raj Sarraf <rrs@researchut.com> - 1.68-1
- Updated to release 1.68.

* Thu Jul  2 2015 Ritesh Raj Sarraf <rrs@researchut.com> - 1.67-1
- Updated to release 1.67.

* Fri Sep 26 2014 Ritesh Raj Sarraf <rrs@researchut.com> - 1.66-1
- Updated to release 1.66.

* Wed Jun 18 2014 Ritesh Raj Sarraf <rrs@researchut.com> - 1.65-1
- Updated to release 1.65.

* Sun Sep  1 2013 Ritesh Raj Sarraf <rrs@researchut.com> - 1.64-1
- Updated to release 1.64.

* Sat Mar 23 2013 Ritesh Raj Sarraf <rrs@researchut.com> - 1.63-1
- Updated to release 1.63.

* Tue Oct 30 2012 Ritesh Raj Sarraf <rrs@researchut.com> - 1.62-1
- Updated to release 1.62.

* Thu May 17 2012 Ritesh Raj Sarraf <rrs@researchut.com> - 1.61-1
- Updated to release 1.61.

* Fri Oct 14 2011 Ritesh Raj Sarraf <rrs@researchut.com> - 1.60-1
- Updated to release 1.60.

* Mon Aug  8 2011 Ritesh Raj Sarraf <rrs@researchut.com> - 1.59-1
- Updated to release 1.59.

* Sat Jul 23 2011 Ritesh Raj Sarraf <rrs@researchut.com> - 1.58-1
- Updated to release 1.58.

* Sun Feb 27 2011 Ritesh Raj Sarraf <rrs@researchut.com> - 1.57-1
- Updated to release 1.57.

* Mon Feb 14 2011 Ritesh Raj Sarraf <rrs@researchut.com> - 1.56-1
- Updated to release 1.56.

* Wed May 26 2010 Ritesh Raj Sarraf <rrs@researchut.com> - 1.55-1
- Updated to release 1.55.

* Wed Mar 10 2010 Ritesh Raj Sarraf <rrs@researchut.com> - 1.54-1
- Updated to release 1.54.

* Sat Jan  2 2010 Ritesh Raj Sarraf <rrs@researchut.com> - 1.53-1
- Updated to release 1.53.

* Thu Oct  8 2009 Ritesh Raj Sarraf <rrs@researchut.com> - 1.52-1
- Updated to release 1.52.

* Tue Sep  1 2009 Ritesh Raj Sarraf <rrs@researchut.com> - 1.51-1
- Updated to release 1.51.

* Fri Jul 24 2009 Ritesh Raj Sarraf <rrs@researchut.com> - 1.50-1
- Updated to release 1.50.

* Sun Sep 07 2008 Bart Samwel <bart@samwel.tk> - 1.45-1
- Updated to release 1.45.

* Mon May 28 2007 Bart Samwel <bart@samwel.tk> - 1.34-1
- Updated to release 1.34.
- Added some files from upstream that were left out in earlier packages, such as lm-profiler.
- Restart acpid after %{__install} -Dping.

* Sun Oct 08 2006 Dag Wieers <dag@wieers.com> - 1.32-1
- Updated to release 1.32.

* Sun Apr 16 2006 Dag Wieers <dag@wieers.com> - 1.31-1
- Updated to release 1.31.

* Sat Apr 15 2006 Dag Wieers <dag@wieers.com> - 1.30-1
- Updated to release 1.30.

* Sun Apr 10 2005 Dag Wieers <dag@wieers.com> - 1.05-1
- Initial package. (using DAR)
