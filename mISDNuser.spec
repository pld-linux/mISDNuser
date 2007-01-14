%define		_ver	%(echo %{version} | tr . _)
Summary:	Userspace part of Modular ISDN stack
Summary(pl):	Czê¶æ stosu modularnego ISDN (mISDN) dla przestrzeni u¿ytkonika
Name:		mISDNuser
Version:	1.0.3
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://www.misdn.org/downloads/releases/%{name}-%{_ver}.tar.gz
# Source0-md5:	c1c36841386222c2a35c110c8e63f3bc
Patch0:		%{name}-build.patch
URL:		http://www.isdn4linux.de/mISDN/
BuildRequires:	mISDN-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mISDN (modular ISDN) is intended to be the new ISDN stack for the
Linux 2.6 kernel, from the maintainer of the existing isdn4linux code.
This package contains the userspace libraries required to interface
directly to mISDN.

%description -l pl
mISDN (modularny ISDN) ma byæ nowym stosem ISDN dla j±dra Linuksa 2.6
tworzonym przez maintainera obecnego kodu isdn4linux. Ten pakiet
zawiera biblioteki przestrzeni u¿ytkownika potrzebne do bezpo¶redniej
komunikacji z mISDN.

%package devel
Summary:	Development files Modular ISDN stack
Summary(pl):	Pliki nag³ówkowe stosu modularnego ISDN
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the development files for userspace libraries
required to interface to mISDN, needed for compiling applications
which use mISDN directly such as OpenPBX.

%description devel -l pl
Ten pakiet zawiera pliki programistyczne dla bibliotek przestrzeni
u¿ytkownika s³u¿±cych do komunikacji z mISDN. Jest potrzebny do
kompilacji aplikacji u¿ywaj±cych bezpo¶rednio mISDN, takich jak
OpenPBX.

%package utils
Summary:	Debugging utilities for Modular ISDN stack
Summary(pl):	Narzêdzia diagnostyczne dla stosu modularnego ISDN
Group:		Applications/System

%description utils
mISDN (modular ISDN) is intended to be the new ISDN stack for the
Linux 2.6 kernel, from the maintainer of the existing isdn4linux code.
This package contains test utilities for mISDN.

%description utils -l pl
mISDN (modularny ISDN) ma byæ nowym stosem ISDN dla j±dra Linuksa 2.6
tworzonym przez maintainera obecnego kodu isdn4linux. Ten pakiet
zawiera narzêdzia testowe dla mISDN.

%prep
%setup -q -n %{name}-%{_ver}
%patch0 -p0
rm -rf voip

%build
%{__make} \
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
%attr(755,root,root) %{_libdir}/*.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_includedir}/mISDNuser

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
