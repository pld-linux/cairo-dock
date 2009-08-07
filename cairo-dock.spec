Summary:	MacOS-like Dock for GNOME
Summary(pl.UTF-8):	Dok w stylu MacOS dla GNOME
Name:		cairo-dock
Version:	2.0.8
Release:	0.1
License:	GPL v3+
Group:		Applications
Source0:	http://download.berlios.de/cairo-dock/%{name}-%{version}.tar.bz2
# Source0-md5:	bf591fb0833c41c8d6dec327d847b681
URL:		http://developer.berlios.de/projects/cairo-dock/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	cairo-devel
BuildRequires:	dbus-glib
BuildRequires:	glitz-devel
BuildRequires:	gnome-vfs2-devel >= 2.0
BuildRequires:	gtkglext-devel >= 1.2.0
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
Requires:	cairo-devel
Requires:	glitz-devel
Requires:	gtk+2-devel >= 1:2.0
Requires:	librsvg-devel >= 2.0
# doesn't require base

%description devel
Header files for cairo-dock plugins development.

%description devel -l pl.UTF-8
Pliki nagłówkowe do tworzenia wtyczek cairo-docka.

%prep
%setup -q

%build
DOCKDIR=$(pwd)
%{__autoconf}
%{__aclocal}
%{__automake}
%configure
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cairo-dock
%dir %{_datadir}/cairo-dock
%{_datadir}/cairo-dock
#%{_datadir}/cairo-dock/*.conf
%{_datadir}/cairo-dock/themes

%files devel
%defattr(644,root,root,755)
%{_includedir}/cairo-dock
%{_pkgconfigdir}/cairo-dock.pc
%attr(755,root,root) %{_libdir}/libcairo-dock.so
