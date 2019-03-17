# https://software.opensuse.org/download.html?project=home%3Adismine&package=valentina
# https://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/RPM_Guide/index.html
# https://rpm.org/documentation.html

####################################################################################################

Name:          valentina
Summary:       Pattern Making Application
Version:       0.6.1
Release:       165.32
License:       GPL-3.0+
Group:         Graphics
URL:           https://bitbucket.org/dismine/valentina
# Packager:      Roman Telezhinskyi <dismine@gmail.com>
Source0:       https://bitbucket.org/dismine/valentina/get/v%{version}.tar.bz2
# % {name}-% {version}.tar.xz

BuildRoot:     %{_tmppath}/%{name}-%{version}-build

####################################################################################################

Conflicts: seamly2d

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

BuildRequires: pkgconfig(Qt5Concurrent)
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Network)
BuildRequires: pkgconfig(Qt5OpenGL)
BuildRequires: pkgconfig(Qt5PrintSupport)
BuildRequires: pkgconfig(Qt5Svg)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: pkgconfig(Qt5Xml)
BuildRequires: pkgconfig(Qt5XmlPatterns)
BuildRequires: qt5-qtbase-devel >= 5.2.0
BuildRequires: qt5-qtsvg-devel >= 5.2.0
BuildRequires: qt5-qttools-devel >= 5.2.0
BuildRequires: qt5-qtxmlpatterns-devel  >= 5.2.0

Requires: poppler-utils
Requires: qt5-qtbase-gui >= 5.2.0
Requires: qt5-qtsvg >= 5.2.0
Requires: qt5-qtxmlpatterns >= 5.2.0

####################################################################################################

%description
Valentina is a cross-platform patternmaking program which allows
designers to create and model patterns of clothing. This software
allows pattern creation, using either standard sizing tables or an
individual’s set of measurements. It blends new technologies with
traditional methods to create a unique pattern making tool.

####################################################################################################

# Disables debug packages and stripping of binaries:
%global _enable_debug_package 0
%global __debug_install_post %{nil}
%global debug_package %{nil}

####################################################################################################

%prep
# %setup -q -n %{name}-%{version}
rm -rf %{name}-%{version}
tar -xjf %{SOURCE0}
mv dismine-valentina-* %{name}-%{version}

####################################################################################################

%build
qmake-qt5 PREFIX=%{_prefix} Valentina.pro -r "CONFIG += noTests noRunPath no_ccache noDebugSymbols"
%{__make} %{?jobs:-j %jobs}

####################################################################################################

%install
export NO_DEBUGINFO_STRIP_DEBUG=true
%{__make} INSTALL_ROOT=%{buildroot} install

gzip -9c dist/debian/%{name}.1 > dist/debian/%{name}.1.gz &&
%{__install} -Dm 644 dist/debian/%{name}.1.gz %{buildroot}%{_mandir}/man1/%{name}.1.gz

gzip -9c dist/debian/tape.1 > dist/debian/tape.1.gz &&
%{__install} -Dm 644 dist/debian/tape.1.gz %{buildroot}%{_mandir}/man1/tape.1.gz

cp dist/debian/valentina.sharedmimeinfo dist/debian/%{name}.xml &&
%{__install} -Dm 644 dist/debian/%{name}.xml %{buildroot}%{_datadir}/mime/packages/%{name}.xml

cp dist/debian/valentina.mime dist/debian/%{name} &&
%{__install} -Dm 644 dist/debian/%{name} %{buildroot}%{_libdir}/mime/packages/%{name}

####################################################################################################

%post
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/mime/packages &>/dev/null || :

####################################################################################################

%postun
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
  /usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
fi

####################################################################################################

%posttrans
/usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

####################################################################################################

%files
%defattr(-,root,root,-)
%doc README.txt LICENSE_GPL.txt
%doc %{_mandir}/man1/%{name}.1*
%doc %{_mandir}/man1/tape.1*
%{_bindir}/valentina
%{_bindir}/tape
%{_libdir}/libvpropertyexplorer.so
%{_libdir}/libvpropertyexplorer.so.*
%{_libdir}/libqmuparser.so
%{_libdir}/libqmuparser.so.*
%dir %{_libdir}/mime
%dir %{_libdir}/mime/packages
%{_libdir}/mime/packages/%{name}
%dir %{_datadir}/mime
%dir %{_datadir}/mime/packages
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/tape.desktop
%{_datadir}/pixmaps/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/diagrams.rcc
%dir %{_datadir}/%{name}/translations
%{_datadir}/%{name}/translations/*.qm
%dir %{_datadir}/%{name}/tables
%dir %{_datadir}/%{name}/tables/multisize
%{_datadir}/%{name}/tables/multisize/*.vst
%dir %{_datadir}/%{name}/tables/templates
%{_datadir}/%{name}/tables/templates/*.vit
%dir %{_datadir}/%{name}/labels
%{_datadir}/%{name}/labels/*.xml

####################################################################################################

%clean
rm -f dist/debian/%{name}.1.gz dist/debian/tape.1.gz dist/debian/%{name}.xml dist/debian/%{name}
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

####################################################################################################

%changelog
* Tue Oct 23 2018 Roman Telezhynskyi
 - Auto build
