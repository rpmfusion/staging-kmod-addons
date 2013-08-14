# drivers that we ship; to be synced with staging-kmod.spec
%global stgdrvs ASUS_OLED BCM_WIMAX CSR_WIFI DGRP  ECHO ET131X  FB_XGI FT1000 IDE_PHISON LINE6_USB NET_VENDOR_SILICOM PRISM2_USB R8187SE RTL8192U RTS5139 SLICOSS SOLO6X10 SPEAKUP TOUCHSCREEN_CLEARPAD_TM1217 TOUCHSCREEN_SYNAPTICS_I2C_RMI4 TRANZPORT USB_ENESTORAGE USB_SERIAL_QUATECH2 USB_WPAN_HCD USBIP_CORE VT6655 VT6656 WIMAX_GDM72XX WLAGS49_H25 W35UND WLAGS49_H2 ZCACHE ZRAM ZSMALLOC


# makes handling for rc kernels a whole lot easier:
#global prever rc8

Name:          staging-kmod-addons
Version:       3.10.5
Release:       %{?prever:0.}1%{?prever:.%{prever}}%{?dist}
Summary:       Documentation and shared parts for the kmod-staging packages

Group:         System Environment/Kernel
License:       GPLv2
URL:           http://www.kernel.org/
# use the script from Source1 to create this archive; call it like this: 
#  bash $(rpm --eval '%{_sourcedir}')/create-linux-staging-tarball.sh 2.6.30.8
Source0:       linux-staging-%{version}%{?prever:-%{prever}}.tar.bz2
Source1:       create-linux-staging-tarball.sh
Source2:       usbip-server.service
Source3:       usbip-client.service
Source4:       usbip.configuration
Provides:      staging-kmod-common = %{version}-%{release}
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: glib2-devel libtool pkgconfig
BuildRequires: libsysfs-devel
BuildRequires: %{_sysconfdir}/rpm/macros.systemd

%description
Documentation for some of the kernel modules from linux-staging.


%package -n usbip
License:       GPLv2+
Summary:       USB/IP userspace
Group:         System Environment/Daemons
Requires:      %{name} = %{version}
Requires:      hwdata
Requires:       systemd-units
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description -n usbip
Userspace for USB/IP from linux-staging


%package -n usbip-devel
License:       GPLv2+
Summary:       USB/IP headers and development libraries
Group:         System Environment/Libraries
Requires:      usbip%{?_isa} = %{version}

%description -n usbip-devel
This package contains headers and static libraries for USB/IP userspace
development


%prep
%setup -q -n linux-staging-%{version}%{?prever:-%{prever}}
# docs only for drivers that we ship
mkdir .doc
for driver in %{stgdrvs} ; do
  subdirectory="$(grep ${driver} drivers/staging/Makefile | awk '{print $3}')"
  for file in TODO README ; do
    if [[ -e "drivers/staging/${subdirectory}${file}" ]] ; then
      cp -l "drivers/staging/${subdirectory}${file}" .doc/${subdirectory%%/}-$(basename ${subdirectory}${file})
    fi
  done
done


%build
# Build usbip userspace
cd drivers/staging/usbip/userspace
# this man page file got removed for 3.7:
# http://git.kernel.org/linus/4faf3a8d1838b86e7b66441da9a088f347e1c56b
sed -i 's/usbip_bind_driver.8//' Makefile.am
./autogen.sh
%configure --disable-static --with-usbids-dir=/usr/share/hwdata
make %{?_smp_mflags}


%install
# Install usbip userspace
cd drivers/staging/usbip/userspace
%makeinstall
rm -f %{buildroot}%{_libdir}/*.la
mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE2} %{buildroot}%{_unitdir}
install -m 644 %{SOURCE3} %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/default
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/default/usbip


%post -n usbip
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun -n usbip
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable usbip-server.service > /dev/null 2>&1 || :
    /bin/systemctl stop usbip-server.service > /dev/null 2>&1 || :
    /bin/systemctl --no-reload disable usbip-client.service > /dev/null 2>&1 || :
    /bin/systemctl stop usbip-client.service > /dev/null 2>&1 || :
fi

%postun -n usbip
/sbin/ldconfig
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart usbip-server.service >/dev/null 2>&1 || :
    /bin/systemctl try-restart usbip-client.service >/dev/null 2>&1 || :
fi


%files -n usbip-devel
%defattr(-,root,root,-)
%doc drivers/staging/usbip/userspace/COPYING
%{_includedir}/*
%{_libdir}/libusbip.so

%files
%defattr(-,root,root,-)
%doc COPYING .doc/*

%files -n usbip
%defattr(-,root,root,-)
%doc COPYING
%{_sbindir}/usbip*
%{_libdir}/libusbip.so.*
%{_mandir}/man8/*
%{_unitdir}/*
%config(noreplace) %{_sysconfdir}/default/*


%changelog
* Wed Aug 14 2013 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3.10.5-1
- Update to 3.10.5
- add /etc/rpm/macros.systemd as BR

* Sat May 18 2013 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3.9.2-1
- Update to 3.9.2
- disable SB105X - does not compile
- disable ZCACHE - latest version not buildable as module

* Fri Mar 01 2013 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3.8.1-1
- Update to 3.8.1 and enable a few more drivers

* Mon Jan 14 2013 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3.7.2-1
- Update to 3.7.2
- work around missing usbip_bind_driver.8, which is referenced from Makefile.am

* Thu Oct 11 2012 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3.6.1-1
- Update to 3.6.1

* Tue Jul 31 2012 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3.5-1.1
- Update to 3.5
- Disable Mei, now a proper driver

* Wed Jul 25 2012 Jonathan Dieter <jdieter@gmail.com> - 3.4.2-3
- Split USB/IP userspace into subpackage
- Add systemd service for server

* Mon Jul 16 2012 Jonathan Dieter <jdieter@gmail.com> - 3.4.2-2
- Enable userspace for USB/IP
- Add devel subpackage
- Remove noarch as userspace is dependent on architecture

* Sun Jun 17 2012 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3.4.2-1
- Update to 3.4.2
- Enable USB_WPAN_HCD 
- disable XVMALLOC and enable replacement ZSMALLOC
- update create-linux-staging-tarball.sh to include drivers/video/sis/, 
  needed for FB_XGI

* Mon May 14 2012 Nicolas Chauvet <kwizart@gmail.com> - 3.3-1.1
- Rebuilt for release

* Wed Mar 21 2012 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3.3-1
- update to 3.3

* Tue Jan 24 2012 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3.2.1-1.1
- update to 3.2.1
- drop ATH6K_LEGACY (replaced by a proper driver)
- drop DRM_PSB (enabled in Fedora)
- add RTS5139

* Sun Nov 06 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3.1-1
- update to 3.1 (no new drivers)

* Mon Aug 01 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.6.40-3
- update to 3.0 aka 2.6.40
- Enable BRCMSMAC, BRCMFMAC, DRM_PSB, INTEL_MEI, RTS_PSTOR, XVMALLOC, ZCACHE 
- Drop RT2860, RT2870, RT3070, RT3090, SAMSUNG_LAPTOP dropped upstream
- bump release to 3 to avoid tagging problems in cvs

* Sun May 29 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.6.38.7-2.1
- Enable ATH6K_LEGACY BCM_WIMAX BRCM80211 EASYCAP FT1000_USB R8712U SBE_2T3E3
  SLICOSS SOLO6X10 TOUCHSCREEN_CLEARPAD_TM1217 TOUCHSCREEN_SYNAPTICS_I2C_RMI4
  USB_ENESTORAGE ZRAM

* Tue May 24 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.6.38.7-1
- Update to 2.6.38.7

* Thu Jan 06 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.6.35.10-1
- update to 2.6.35.10

* Sat Oct 30 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.6.35.6-1
- update to 2.6.35.6 for F14
- enable FB_XGI

* Sun Aug 08 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.6.34.2-1.1
- update to 2.6.34.2, which is hitting updates-testing for F13
- enable phison (#1338)

* Sun Apr 25 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.6.33.2-2
- enable echo

* Fri Apr 16 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.6.33.2-1
- update to 2.6.33.2 for F13

* Sat Feb 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.6.32.8-1
- update to 2.6.32.8 for updates-testing kernel

* Wed Dec 02 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.6.32-0.1.rc1
- enable HYPERV, RT3090, RTL8192E, VT6656
- drop AGNX, dropped upstream
- support RC's better

* Sun Nov 01 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.6.31.5-2
- enable FB_UDL RTL8192SU VT6655

* Sun Nov 01 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.6.31.5-1
- update to 2.6.31.5

* Fri Oct 23 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.6.30.8-2
- enable VIDEO_GO7007

* Tue Oct 20 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.6.30.8-1
- initial package
