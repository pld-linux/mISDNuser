
%define         mISDNuser_version           %(echo %{version} |tr . _)

Summary:	Userspace part of Modular ISDN stack
Name:		mISDNuser
Version:	1.0.3
Release:	1
License:	LGPL
Group:		Libraries
URL:		http://www.isdn4linux.de/mISDN/
Source0:	http://www.misdn.org/downloads/releases/%{name}-1_0_3.tar.gz
# Source0-md5:	c1c36841386222c2a35c110c8e63f3bc
Patch0:		%{name}-build.patch
BuildRequires:	mISDN-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mISDN (modular ISDN) is intended to be the new ISDN stack for the
Linux 2.6 kernel, from the maintainer of the existing isdn4linux code.
This package contains the userspace libraries required to interface
directly to mISDN.

%package devel
Summary:	Development files Modular ISDN stack
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
mISDN (modular ISDN) is intended to be the new ISDN stack for the
Linux 2.6 kernel, from the maintainer of the existing isdn4linux code.
This package contains the development files for userspace libraries
required to interface to mISDN, needed for compiling applications
which use mISDN directly such as OpenPBX.

%package utils
Summary:	Debugging utilities for Modular ISDN stack
Group:		Applications/System

%description utils
mISDN (modular ISDN) is intended to be the new ISDN stack for the
Linux 2.6 kernel, from the maintainer of the existing isdn4linux code.
This package contains test utilities for mISDN.

%prep
%setup -q -n %{name}-%{mISDNuser_version}
%patch0 -p0
rm -rf voip

%build
%{__make} CFLAGS="-I`pwd`/include %{rpmcflags}" MISDNDIR=`pwd`

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install INSTALL_PREFIX=$RPM_BUILD_ROOT MISDNDIR=`pwd` LIBDIR=%_libdir

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %_libdir/*.so.*
%exclude %{_bindir}/*

%files devel
%defattr(644,root,root,755)
%_includedir/mISDNuser
%_libdir/*.so
%exclude %_libdir/*.a

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
