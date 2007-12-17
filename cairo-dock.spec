#
Summary:	MacOS-like Dock for GNOME
Name:		cairo-dock
Version:	1.4.5.1
Release:	1
License:	GPLv3+
Group:		Applications
Source0:	http://download.berlios.de/cairo-dock/%{name}-sources-20071214.tar.bz2
# Source0-md5:	5c826e7bb4ac15dc398e59d7f698d1e3
URL:		http://developer.berlios.de/projects/cairo-dock/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cairo-devel
#BuildRequires:	intltool
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An light eye-candy fully themable animated dock for any Linux desktop.
It has a family-likeness with OSX dock, but with more options.

%prep
%setup -q -n opt/%{name}

%build
# if ac/am/* rebuilding is necessary, do it in this order and add
# appropriate BuildRequires
#%%{__intltoolize}
#%%{__gettextize}
#%%{__libtoolize}
#%%{__autoheader}
# if not running libtool or automake, but config.sub is too old:
#cp -f /usr/share/automake/config.sub .
cd cairo-dock
%{__autoconf}
%{__aclocal}
%{__automake}
%configure
%{__make}
cd ..

cd plug-ins
# To fix: logout
for dir in clock file-manager rhythmbox dustbin file-manager-gnome rendering; do
	cd $dir
	PACKAGES="gtk+-2.0 cairo librsvg-2.0"
	PACKAGE_LIBS=
	PACKAGE_CFLAGS="-I$RPM_BUILD_DIR/opt/cairo-dock/cairo-dock/src"
	%{__autoconf}
	%{__aclocal}
	if [ $dir = rhythmbox ]; then
		%{__libtoolize}
		PACKAGES="$PACKAGES dbus-glib-1 dbus-1"
	elif [ $dir = file-manager-gnome ]; then
		PACKAGES="$PACKAGES gnome-vfs-2.0 libgnomeui-2.0"
		PACKAGE_CFLAGS="$PACKAGE_CFLAGS -I$RPM_BUILD_DIR/opt/cairo-dock/plug-ins/file-manager/src"
	elif [ $dir = rendering ]; then
		%{__libtoolize}
	fi
	%{__automake}
	PACKAGE_LIBS="$PACKAGE_LIBS `pkg-config --libs $PACKAGES`" PACKAGE_CFLAGS="$PACKAGE_CFLAGS `pkg-config --cflags $PACKAGES` " %configure
	%{__make} pkgdatadir=/usr/share/cairo-dock/plug-in/$dir
	cd ..
done
cd ..

%install
rm -rf $RPM_BUILD_ROOT

cd cairo-dock
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
cd ..

cd plug-ins
# To fix: logout
for dir in clock file-manager rhythmbox dustbin file-manager-gnome rendering; do
	cd $dir
	%{__make} install \
		DESTDIR=$RPM_BUILD_ROOT \
		pkgdatadir=/usr/share/cairo-dock/plug-in/$dir
	cd ..
done
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cairo-dock

#%files devel
%{_includedir}/cairo-dock
%{_includedir}/file-manager
%{_libdir}/libcd-clock.so
%attr(755,root,root)    %{_libdir}/libcd-clock.so.1
%attr(755,root,root)    %{_libdir}/libcd-clock.so.1.0.0
%{_libdir}/libcd-dustbin.la
%{_libdir}/libcd-dustbin.so
%attr(755,root,root)    %{_libdir}/libcd-dustbin.so.1
%attr(755,root,root)    %{_libdir}/libcd-dustbin.so.1.0.0
%{_libdir}/libcd-rendering.la
%{_libdir}/libcd-rendering.so
%attr(755,root,root)    %{_libdir}/libcd-rendering.so.1
%attr(755,root,root)    %{_libdir}/libcd-rendering.so.1.0.0
%{_libdir}/libcd-rhythmbox.la
%{_libdir}/libcd-rhythmbox.so
%attr(755,root,root)    %{_libdir}/libcd-rhythmbox.so.1
%attr(755,root,root)    %{_libdir}/libcd-rhythmbox.so.1.0.0
%{_libdir}/libfile-manager-gnome.la
%{_libdir}/libfile-manager-gnome.so
%attr(755,root,root)    %{_libdir}/libfile-manager-gnome.so.1
%attr(755,root,root)    %{_libdir}/libfile-manager-gnome.so.1.0.0
%{_libdir}/libfile-manager.la
%{_libdir}/libfile-manager.so
%attr(755,root,root)    %{_libdir}/libfile-manager.so.1
%attr(755,root,root)    %{_libdir}/libfile-manager.so.1.0.0
%{_pkgconfigdir}/cairo-dock.pc
%{_pkgconfigdir}/file-manager.pc

%dir %{_datadir}/cairo-dock
%{_datadir}/cairo-dock/*.svg
%{_datadir}/cairo-dock/*.conf
%{_datadir}/cairo-dock/plug-in
%{_datadir}/cairo-dock/readme-basic-view
%{_datadir}/cairo-dock/*.conf
%{_datadir}/cairo-dock/themes
