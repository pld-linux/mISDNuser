%define		_snap 20090602
Summary:	Userspace part of Modular ISDN stack v2
Summary(pl.UTF-8):	Część stosu modularnego ISDN (mISDN v2) dla przestrzeni użytkonika
Name:		mISDNuser
Version:	2.0
Release:	0.%{_snap}.1
License:	LGPL
Group:		Libraries
Source0:	http://www.linux-call-router.de/download/lcr-1.5/%{name}_%{_snap}.tar.gz
# Source0-md5:	3288ec912031e5840f2d07134ab8d3d6
Patch0:		%{name}-build.patch
URL:		http://www.misdn.org/
BuildRequires:	linux-libc-headers >= 2.6.29
BuildConflicts:	mISDN-devel < 2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mISDN (modular ISDN) is the new ISDN stack for the Linux 2.6 kernel,
from the maintainer of the existing isdn4linux code. mISDN v2 has been
included in the mainline kernel since 2.6.29. This package contains
the userspace libraries required to interface directly to mISDN.

%description -l pl.UTF-8
mISDN (modularny ISDN) jest nowym stosem ISDN dla jądra Linuksa 2.6
tworzonym przez maintainera obecnego kodu isdn4linux. Wersja druga
mISDN jest już włączona do oficjalnego kodu jądra, od wersji
2.6.29. Ten pakiet zawiera biblioteki przestrzeni użytkownika
potrzebne do bezpośredniej komunikacji z mISDN.

%package devel
Summary:	Development files Modular ISDN stack
Summary(pl.UTF-8):	Pliki nagłówkowe stosu modularnego ISDN
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	linux-libc-headers >= 2.6.29

%description devel
This package contains the development files for userspace libraries
required to interface to mISDN, needed for compiling applications
which use mISDN directly such as OpenPBX.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki programistyczne dla bibliotek przestrzeni
użytkownika służących do komunikacji z mISDN. Jest potrzebny do
kompilacji aplikacji używających bezpośrednio mISDN, takich jak
OpenPBX.

%package static
Summary:	Static libraries for Modular ISDN stack
Summary(pl.UTF-8):	Biblioteki statyczne stosu modularnego ISDN
Group:		Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains static libraries for userspace libraries
required to interface to mISDN, needed for compiling applications
which use mISDN directly such as OpenPBX.

%description static -l pl.UTF-8
Ten pakiet zawiera bibliotek statyczne przestrzeni użytkownika
służących do komunikacji z mISDN. Jest potrzebny do kompilacji
aplikacji używających bezpośrednio mISDN, takich jak OpenPBX.

%package utils
Summary:	Utilities for Modular ISDN stack
Summary(pl.UTF-8):	Narzędzia dla stosu modularnego ISDN
Group:		Applications/System

%description utils
mISDN (modular ISDN) is intended to be the new ISDN stack for the
Linux 2.6 kernel, from the maintainer of the existing isdn4linux code.
This package contains utilities for mISDN.

%description utils -l pl.UTF-8
mISDN (modularny ISDN) ma być nowym stosem ISDN dla jądra Linuksa
2.6 tworzonym przez maintainera obecnego kodu isdn4linux. Ten pakiet
zawiera narzędzia dla mISDN.

%prep
%setup -q -n %{name}
%patch0 -p1

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
%doc
%attr(755,root,root) %{_libdir}/*.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_includedir}/mISDNuser

%files static
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.a

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
