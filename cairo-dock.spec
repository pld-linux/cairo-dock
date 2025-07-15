Summary:	MacOS-like Dock for GNOME
Summary(pl.UTF-8):	Dok w stylu MacOS dla GNOME
Name:		cairo-dock
Version:	2.2.0.4
Release:	2
License:	GPL v3+
Group:		Applications
#Source0Download: https://github.com/Cairo-Dock/cairo-dock-core/releases
Source0:	https://github.com/Cairo-Dock/cairo-dock-core/archive/2.2.0-4/cairo-dock-core-2.2.0-4.tar.gz
# Source0-md5:	dac87d416f5721af45c56abbac464fa4
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-format.patch
URL:		http://glx-dock.org/
BuildRequires:	cairo-devel
BuildRequires:	cmake >= 2.6
BuildRequires:	dbus-devel
BuildRequires:	dbus-glib
BuildRequires:	dbus-glib-devel
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gtk+2-devel >= 1:2.0
BuildRequires:	gtkglext-devel >= 1.2.0
BuildRequires:	librsvg-devel >= 2.0
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	xorg-lib-libXcomposite-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An light eye-candy fully themable animated dock for any Linux desktop.
It has a family-likeness with MacOS X dock, but with more options.

%description -l pl.UTF-8
Jasny, miły dla oka, w pełni obsługujący motywy, animowany dok dla
pulpitu linuksowego. Jest zbliżony do doka z MacOS X, ale ma więcej
opcji.

%package devel
Summary:	Header files for cairo-dock plugins development
Summary(pl.UTF-8):	Pliki nagłówkowe do tworzenia wtyczek cairo-docka
Group:		Development/Libraries
Requires:	cairo-devel
Requires:	dbus-devel
Requires:	dbus-glib-devel
Requires:	glib2-devel >= 2.0
Requires:	gtk+2-devel >= 1:2.0
Requires:	gtkglext-devel >= 1.0
Requires:	librsvg-devel >= 2.0
Requires:	libxml2-devel >= 2.0
Requires:	xorg-lib-libXcomposite-devel
Requires:	xorg-lib-libXinerama-devel
Requires:	xorg-lib-libXrender-devel
Requires:	xorg-lib-libXtst-devel

%description devel
Header files for cairo-dock plugins development.

%description devel -l pl.UTF-8
Pliki nagłówkowe do tworzenia wtyczek cairo-docka.

%prep
%setup -q -n cairo-dock-core-2.2.0-4
%patch -P0 -p1
%patch -P1 -p1

%build
install -d build
cd build
%cmake ..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# for plugins (see cairo-dock.pc)
install -d $RPM_BUILD_ROOT{%{_libdir}/cairo-dock,%{_datadir}/%{name}/plug-ins}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cairo-dock
%attr(755,root,root) %{_bindir}/cairo-dock-package-theme
%attr(755,root,root) %{_bindir}/launch-cairo-dock-with-delay
%attr(755,root,root) %{_libdir}/libgldi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgldi.so.2
%dir %{_libdir}/cairo-dock
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/ChangeLog.txt
%attr(755,root,root) %{_datadir}/%{name}/help_scripts.sh
%{_datadir}/%{name}/*.conf
%{_datadir}/%{name}/*.desktop
%{_datadir}/%{name}/*.png
%{_datadir}/%{name}/*.svg
%{_datadir}/%{name}/*.xpm
%dir %{_datadir}/%{name}/explosion
%{_datadir}/%{name}/explosion/*.png
%dir %{_datadir}/%{name}/gauges
%{_datadir}/%{name}/gauges/Battery
%{_datadir}/%{name}/gauges/Turbo-night-fuel
%dir %{_datadir}/%{name}/plug-ins
%dir %{_datadir}/%{name}/themes
%{_datadir}/%{name}/themes/_default_
%{_desktopdir}/cairo-dock.desktop
%{_desktopdir}/cairo-dock-cairo.desktop
%{_pixmapsdir}/cairo-dock.svg
%{_mandir}/man1/cairo-dock.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgldi.so
%{_includedir}/cairo-dock
%{_pkgconfigdir}/cairo-dock.pc
%{_pkgconfigdir}/gldi.pc
