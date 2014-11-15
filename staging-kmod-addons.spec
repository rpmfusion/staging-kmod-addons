# drivers that we ship; to be synced with staging-kmod.spec
%global stgdrvs BCM_WIMAX FB_XGI FT1000 LINE6_USB LTE_GDM724X PRISM2_USB R8188EU RTL8192U  SPEAKUP TOUCHSCREEN_CLEARPAD_TM1217 TOUCHSCREEN_SYNAPTICS_I2C_RMI4 USB_WPAN_HCD VT6655 VT6656 WIMAX_GDM72XX


# makes handling for rc kernels a whole lot easier:
#global prever rc8

Name:          staging-kmod-addons
Version:       3.17.2
Release:       %{?prever:0.}1%{?prever:.%{prever}}%{?dist}
Summary:       Documentation and shared parts for the kmod-staging packages

Group:         System Environment/Kernel
License:       GPLv2
URL:           http://www.kernel.org/
# use the script from Source1 to create this archive; call it like this: 
#  bash $(rpm --eval '%{_sourcedir}')/create-linux-staging-tarball.sh 2.6.30.8
Source0:       linux-staging-%{version}%{?prever:-%{prever}}.tar.xz
Source1:       create-linux-staging-tarball.sh
Provides:      staging-kmod-common = %{version}-%{release}
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch

%description
Documentation for some of the kernel modules from linux-staging.


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
# nothing to build


%install
# nothing to install


%files
%defattr(-,root,root,-)
%doc COPYING .doc/*


%changelog
* Sat Nov 15 2014 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3.17.2-1
- Update to 3.17.2
- sync driverlist with staging-kmod
- drop usbip stuff, is now a porper driver
- make package noarch

* Tue Sep 09 2014 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3.16.2-1
- Update to 3.16.2
- drop RTS5139 (left stating)

* Sun Jul 13 2014 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3.15.4-1
- Update to 3.15.4
- drop ECHI and R8187SE (left)
- adjust downloadscript for file movements
- add BR /usr/include/libudev.h

* Wed Apr 30 2014 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3.14.2-1
- Update to 3.14.2
- remove ZRAM and ZSMALLOC, as they left staging

* Sat Feb 15 2014 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3.13.3-1
- Update to 3.13.3
- switch from bz2 to xz

* Fri Dec 20 2013 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3.12.6-1
- Update to 3.12.6
- drop ASUS_OLED, dropped upstream
- enable LTE_GDM724X and R8188EU
- conditionalize BR, as macros.systemd is somewhere else in f20

* Fri Sep 20 2013 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3.11.1-1
- Update to 3.11.1
- drop csr, dropped upstream

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
