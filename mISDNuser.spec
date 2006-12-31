# Don't build the debugging utils by default.
%bcond_with utils

Name:		mISDN
Version:	1.0.3
Release:	1
Summary:	Userspace part of Modular ISDN stack

Group:		System Environment/Libraries
License:	LGPL
URL:		http://www.isdn4linux.de/mISDN/
Source0:	http://www.misdn.org/downloads/releases/mISDNuser-1_0_3.tar.gz
# From mISDN-1.0.4
Source1:	mISDNif.h
Source2:	mISDN.rules
Patch0:		mISDN-build.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(pre): fedora-usermgmt
Requires(postun): fedora-usermgmt

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%package devel
Summary:	Development files Modular ISDN stack
Group:		System Environment/Libraries
Requires:	mISDN = %{version}-%{release}

%package utils
Summary:	Debugging utilities for Modular ISDN stack
Group:		Applications/System

%description
mISDN (modular ISDN) is intended to be the new ISDN stack for the
Linux 2.6 kernel, from the maintainer of the existing isdn4linux
code. This package contains the userspace libraries required to
interface directly to mISDN.

%description devel
mISDN (modular ISDN) is intended to be the new ISDN stack for the
Linux 2.6 kernel, from the maintainer of the existing isdn4linux
code. This package contains the development files for userspace
libraries required to interface to mISDN, needed for compiling
applications which use mISDN directly such as OpenPBX.

%description utils
mISDN (modular ISDN) is intended to be the new ISDN stack for the
Linux 2.6 kernel, from the maintainer of the existing isdn4linux
code. This package contains test utilities for mISDN.

%prep
%setup -q -n mISDNuser-1_0_3
%patch0 -p0
mkdir include/linux
cp %SOURCE1 include/linux
rm -rf voip

%build
make CFLAGS="-I`pwd`/include $RPM_OPT_FLAGS" MISDNDIR=`pwd`


%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL_PREFIX=$RPM_BUILD_ROOT MISDNDIR=`pwd` LIBDIR=%_libdir
mkdir $RPM_BUILD_ROOT/%{_includedir}/mISDNuser/linux
install -m0644 %SOURCE1 $RPM_BUILD_ROOT/%{_includedir}/mISDNuser/linux/mISDNif.h
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/udev/rules.d
install -m0644 %SOURCE2 $RPM_BUILD_ROOT/%{_sysconfdir}/udev/rules.d/mISDN.rules

%clean
rm -rf $RPM_BUILD_ROOT

%post 
/sbin/ldconfig
/usr/sbin/fedora-groupadd 31 -r misdn &>/dev/null || :
/usr/sbin/fedora-useradd  31 -r -s /sbin/nologin -d / -M \
		-c 'Modular ISDN' -g misdn misdn &>/dev/null || :

%postun
/sbin/ldconfig
test "$1" != 0 || /usr/sbin/fedora-userdel  misdn &>/dev/null || :
test "$1" != 0 || /usr/sbin/fedora-groupdel misdn &>/dev/null || :

%files 
%defattr(-,root,root,-)
%_libdir/*.so.*
%doc COPYING.LIB LICENSE
%config(noreplace) %{_sysconfdir}/udev/rules.d/mISDN.rules
%exclude %_bindir/*

%files devel
%defattr(-,root,root,-)
%_includedir/mISDNuser
%_libdir/*.so
%exclude %_libdir/*.a

%if 0%{?with_utils}
%files utils
%defattr(-,root,root,-)
%_bindir/*
%endif

%changelog
* Sat Dec 16 2006 David Woodhouse <dwmw2@infradead.org> 1.0.3-1
- Update to 1.0.3-1

* Tue Oct 17 2006 David Woodhouse <dwmw2@infradead.org> 0-1.cvs20061010
- Initial import
