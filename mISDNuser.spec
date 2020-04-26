#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_with	capi		# API 2.0 support
%bcond_without	gui		# Qt based GUI
#
Summary:	Userspace part of Modular ISDN stack
Summary(pl.UTF-8):	Część stosu modularnego ISDN (mISDN) dla przestrzeni użytkownika
Name:		mISDNuser
Version:	2.0.19
Release:	2
License:	LGPL v2.1
Group:		Libraries
# git clone git://git.misdn.eu/mISDNuser.git
# git archive --format=tar --prefix=mISDNuser-2.0.19/ v2.0.19 | xz > ../mISDNuser-2.0.19.tar.xz
Source0:	%{name}-%{version}.tar.xz
# Source0-md5:	fb4bf6c110bea0a30486015ca56e80d8
Patch0:		git.patch
Patch1:		x32.patch
URL:		http://www.isdn4linux.de/mISDN/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake
%{?with_capi:BuildRequires:	capi4k-utils-devel >= 3:3.27}
BuildRequires:	libtool >= 2:2
%{?with_capi:BuildRequires:	spandsp-devel}
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with gui}
BuildRequires:	QtCore-devel >= 4
BuildRequires:	qt4-qmake >= 4
%endif
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
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

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
Summary:	Static mISDN library
Summary(pl.UTF-8):	Statyczna biblioteka mISDN
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static mISDN library.

%description static -l pl.UTF-8
Statyczna biblioteka mISDN.

%package utils
Summary:	Debugging utilities for Modular ISDN stack
Summary(pl.UTF-8):	Narzędzia diagnostyczne dla stosu modularnego ISDN
Group:		Applications/System
Obsoletes:	mISDN-init < 2

%description utils
mISDN (modular ISDN) is intended to be the new ISDN stack for the
Linux 2.6 kernel, from the maintainer of the existing isdn4linux code.
This package contains test utilities for mISDN.

%description utils -l pl.UTF-8
mISDN (modularny ISDN) ma być nowym stosem ISDN dla jądra Linuksa 2.6
tworzonym przez maintainera obecnego kodu isdn4linux. Ten pakiet
zawiera narzędzia testowe dla mISDN.

%package capi
Summary:	mISDN CAPI support
Summary(pl.UTF-8):	mISDN - obsługa CAPI
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	capi4k-utils-libs

%description capi
mISDN CAPI support.

%description capi -l pl.UTF-8
mISDN - obsługa CAPI.

%package gui
Summary:	GUI application for mISDN
Summary(pl.UTF-8):	Aplikacja z graficznym interfejsem użytkownika do mISDN
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description gui
GUI application for mISDN.

%description gui -l pl.UTF-8
Aplikacja z graficznym interfejsem użytkownika do mISDN.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	QMAKE="/usr/bin/qmake-qt4" \
	%{?with_capi:--enable-capi --enable-softdsp} \
	%{?with_gui:--enable-gui} \
	%{!?with_static_libs:--disable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/run/mISDNcapid

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with capi}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/capi/lib*.la
# sample
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/capi20.conf
%endif

install -d $RPM_BUILD_ROOT/lib
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/udev $RPM_BUILD_ROOT/lib

install -d $RPM_BUILD_ROOT%{systemdtmpfilesdir}
cat >$RPM_BUILD_ROOT%{systemdtmpfilesdir}/mISDNcapid.conf <<EOF
d /var/run/mISDNcapid 755 root root -
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmisdn.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmisdn.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmisdn.so
%{_libdir}/libmisdn.la
%{_includedir}/mISDN

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmisdn.a
%endif

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/isdn_text2wireshark
%attr(755,root,root) %{_bindir}/l1oipctrl
%attr(755,root,root) %{_bindir}/misdn_E1test
%attr(755,root,root) %{_bindir}/misdn_bridge
%attr(755,root,root) %{_bindir}/misdn_info
%attr(755,root,root) %{_bindir}/misdn_log
%attr(755,root,root) %{_sbindir}/misdn_cleanl2
%attr(755,root,root) %{_sbindir}/misdn_rename
/lib/udev/rules.d/45-misdn.rules

%if %{with capi}
%files capi
%defattr(644,root,root,755)
%doc capi20/capi20.conf.sample
%attr(755,root,root) %{_sbindir}/mISDNcapid
%attr(755,root,root) %{_libdir}/capi/lib_capi_mod_misdn.so*
%dir /var/run/mISDNcapid
%{systemdtmpfilesdir}/mISDNcapid.conf
%endif

%if %{with gui}
%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qmisdnwatch
%endif
