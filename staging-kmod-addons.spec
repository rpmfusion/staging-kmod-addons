# drivers that we ship; to be synced with staging-kmod.spec
%global stgdrvs ASUS_OLED BCM_WIMAX EASYCAP ECHO EPL ET131X FB_UDL FB_XGI FT1000_USB  HECI IDE_PHISON  INTEL_MEI LINE6_USB RTS_PSTOR RAMZSWAP R8187SE RTL8192SU RTL8192E RTL8192U RTS5139 SLICOSS SOLO6X10 SPEAKUP TOUCHSCREEN_CLEARPAD_TM1217 TOUCHSCREEN_SYNAPTICS_I2C_RMI4 USB_ENESTORAGE USB_WPAN_HCD W35UND PRISM2_USB VT6655 VT6656 ZCACHE ZRAM ZSMALLOC


# makes handling for rc kernels a whole lot easier:
#global prever rc8

Name:          staging-kmod-addons
Version:       3.4.2
Release:       %{?prever:0.}1%{?prever:.%{prever}}%{?dist}
Summary:       Documentation and shared parts for the kmod-staging packages

Group:         System Environment/Kernel
License:       GPLv2
URL:           http://www.kernel.org/
# use the script from Source1 to create this archive; call it like this: 
#  bash $(rpm --eval '%{_sourcedir}')/create-linux-staging-tarball.sh 2.6.30.8
Source0:       linux-staging-%{version}%{?prever:-%{prever}}.tar.bz2
Source1:       create-linux-staging-tarball.sh

Provides:      staging-kmod-common = %{version}-%{release}
BuildArch:     noarch
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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
echo "Nothing to build"


%install
rm -rf $RPM_BUILD_ROOT; mkdir $RPM_BUILD_ROOT
echo "Nothing to install"


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING .doc/*


%changelog
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

* Sun Dec 02 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.6.32-0.1.rc1
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
