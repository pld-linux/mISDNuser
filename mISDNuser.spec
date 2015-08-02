%define		_ver	%(echo %{version} | tr . _).1
Summary:	Userspace part of Modular ISDN stack
Summary(pl.UTF-8):	Część stosu modularnego ISDN (mISDN) dla przestrzeni użytkownika
Name:		mISDNuser
Version:	1.1.9
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://www.misdn.org/downloads/releases/%{name}-%{_ver}.tar.gz
# Source0-md5:	16f44afd62c60eefbb5cc930c64a342f
Patch0:		%{name}-build.patch
URL:		http://www.isdn4linux.de/mISDN/
BuildRequires:	mISDN-devel >= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mISDN (modular ISDN) is intended to be the new ISDN stack for the
Linux 2.6 kernel, from the maintainer of the existing isdn4linux code.
This package contains the userspace libraries required to interface
directly to mISDN.

%description -l pl.UTF-8
mISDN (modularny ISDN) ma być nowym stosem ISDN dla jądra Linuksa 2.6
tworzonym przez maintainera obecnego kodu isdn4linux. Ten pakiet
zawiera biblioteki przestrzeni użytkownika potrzebne do bezpośredniej
komunikacji z mISDN.

%package devel
Summary:	Development files Modular ISDN stack
Summary(pl.UTF-8):	Pliki nagłówkowe stosu modularnego ISDN
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	mISDN-devel

%description devel
This package contains the development files for userspace libraries
required to interface to mISDN, needed for compiling applications
which use mISDN directly such as OpenPBX.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki programistyczne dla bibliotek przestrzeni
użytkownika służących do komunikacji z mISDN. Jest potrzebny do
kompilacji aplikacji używających bezpośrednio mISDN, takich jak
OpenPBX.

%package utils
Summary:	Debugging utilities for Modular ISDN stack
Summary(pl.UTF-8):	Narzędzia diagnostyczne dla stosu modularnego ISDN
Group:		Applications/System

%description utils
mISDN (modular ISDN) is intended to be the new ISDN stack for the
Linux 2.6 kernel, from the maintainer of the existing isdn4linux code.
This package contains test utilities for mISDN.

%description utils -l pl.UTF-8
mISDN (modularny ISDN) ma być nowym stosem ISDN dla jądra Linuksa 2.6
tworzonym przez maintainera obecnego kodu isdn4linux. Ten pakiet
zawiera narzędzia testowe dla mISDN.

%prep
%setup -q -n %{name}-%{_ver}
%patch0 -p0
rm -rf voip

%build
%{__make} -j1 \
	CC="%{__cc}" \
	CFLAGS="-I`pwd`/include %{rpmcflags}" \
	MISDNDIR=`pwd`

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL_PREFIX=$RPM_BUILD_ROOT \
	MISDNDIR=`pwd` \
	LIBDIR=%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libisdnnet.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libisdnnet.so.0
%attr(755,root,root) %{_libdir}/libmISDN.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmISDN.so.0
%attr(755,root,root) %{_libdir}/libsuppserv.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsuppserv.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libisdnnet.so
%attr(755,root,root) %{_libdir}/libmISDN.so
%attr(755,root,root) %{_libdir}/libsuppserv.so
%{_includedir}/mISDNuser

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/loadfirm
%attr(755,root,root) %{_bindir}/mISDNdebugtool
%attr(755,root,root) %{_bindir}/misdnportinfo
%attr(755,root,root) %{_bindir}/sendhwctrl
%attr(755,root,root) %{_bindir}/testcon
%attr(755,root,root) %{_bindir}/testcon_l2
%attr(755,root,root) %{_bindir}/testlayer1
%attr(755,root,root) %{_bindir}/testlayer3
%attr(755,root,root) %{_bindir}/testlib
%attr(755,root,root) %{_bindir}/tstlib
