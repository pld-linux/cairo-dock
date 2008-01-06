Summary:	MacOS-like Dock for GNOME
Summary(pl.UTF-8):	Dok w stylu MacOS dla GNOME
Name:		cairo-dock
Version:	1.4.5.1
Release:	0.1
License:	GPL v3+
Group:		Applications
Source0:	http://download.berlios.de/cairo-dock/%{name}-sources-20071214.tar.bz2
# Source0-md5:	5c826e7bb4ac15dc398e59d7f698d1e3
URL:		http://developer.berlios.de/projects/cairo-dock/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cairo-devel
BuildRequires:	dbus-glib
BuildRequires:	gnome-vfs2-devel >= 2.0
BuildRequires:	gtk+2-devel >= 1:2.0
BuildRequires:	libgnomeui-devel >= 2.0
BuildRequires:	librsvg-devel >= 2.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
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
# probably doesn't require base

%description devel
Header files for cairo-dock plugins development.

%description devel -l pl.UTF-8
Pliki nagłówkowe do tworzenia wtyczek cairo-docka.

%prep
%setup -q -c

%build
cd opt/cairo-dock
DOCKDIR=$(pwd)
cd cairo-dock
%{__autoconf}
%{__aclocal}
%{__automake}
%configure
%{__make} -j1

cd ../plug-ins

# To fix: logout
for dir in clock file-manager rhythmbox dustbin file-manager-gnome rendering; do
	cd $dir
	PACKAGES="gtk+-2.0 cairo librsvg-2.0"
	PACKAGE_LIBS=
	# WTF ???
	PACKAGE_CFLAGS="-I${DOCKDIR}/cairo-dock/src"
	%{__autoconf}
	%{__aclocal}
	if [ $dir = rhythmbox ]; then
		%{__libtoolize}
		PACKAGES="$PACKAGES dbus-glib-1 dbus-1"
	elif [ $dir = file-manager-gnome ]; then
		PACKAGES="$PACKAGES gnome-vfs-2.0 libgnomeui-2.0"
		PACKAGE_CFLAGS="$PACKAGE_CFLAGS -I${DOCKDIR}/plug-ins/file-manager/src"
	elif [ $dir = rendering ]; then
		%{__libtoolize}
	fi
	%{__automake}
	PACKAGE_LIBS="$PACKAGE_LIBS `pkg-config --libs $PACKAGES`" \
	PACKAGE_CFLAGS="$PACKAGE_CFLAGS `pkg-config --cflags $PACKAGES` " \
	%configure
	%{__make} -j1 \
		pkgdatadir=/usr/share/cairo-dock/plug-in/$dir
	cd ..
done

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C opt/cairo-dock/cairo-dock install \
	DESTDIR=$RPM_BUILD_ROOT

# To fix: logout
for dir in clock file-manager rhythmbox dustbin file-manager-gnome rendering; do
	%{__make} -C opt/cairo-dock/plug-ins/$dir install \
		DESTDIR=$RPM_BUILD_ROOT \
		pkgdatadir=/usr/share/cairo-dock/plug-in/$dir
done

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cairo-dock
%attr(755,root,root) %{_libdir}/libcd-clock.so.1.0.0
%attr(755,root,root) %ghost %{_libdir}/libcd-clock.so.1
%attr(755,root,root) %{_libdir}/libcd-clock.so
%attr(755,root,root) %{_libdir}/libcd-dustbin.so.1.0.0
%attr(755,root,root) %ghost %{_libdir}/libcd-dustbin.so.1
%attr(755,root,root) %{_libdir}/libcd-dustbin.so
%attr(755,root,root) %{_libdir}/libcd-rendering.so.1.0.0
%attr(755,root,root) %ghost %{_libdir}/libcd-rendering.so.1
%attr(755,root,root) %{_libdir}/libcd-rendering.so
%attr(755,root,root) %{_libdir}/libcd-rhythmbox.so.1.0.0
%attr(755,root,root) %ghost %{_libdir}/libcd-rhythmbox.so.1
%attr(755,root,root) %{_libdir}/libcd-rhythmbox.so
%attr(755,root,root) %{_libdir}/libfile-manager-gnome.so.1.0.0
%attr(755,root,root) %ghost %{_libdir}/libfile-manager-gnome.so.1
%attr(755,root,root) %{_libdir}/libfile-manager-gnome.so
%attr(755,root,root) %{_libdir}/libfile-manager.so.1.0.0
%attr(755,root,root) %ghost %{_libdir}/libfile-manager.so.1
%attr(755,root,root) %{_libdir}/libfile-manager.so
%dir %{_datadir}/cairo-dock
%{_datadir}/cairo-dock/*.svg
%{_datadir}/cairo-dock/*.conf
%{_datadir}/cairo-dock/plug-in
%{_datadir}/cairo-dock/readme-basic-view
%{_datadir}/cairo-dock/*.conf
%{_datadir}/cairo-dock/themes

%files devel
%defattr(644,root,root,755)
%{_includedir}/cairo-dock
%{_includedir}/file-manager
%{_pkgconfigdir}/cairo-dock.pc
%{_pkgconfigdir}/file-manager.pc
