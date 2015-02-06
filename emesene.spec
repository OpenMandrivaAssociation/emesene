%define 	name 	emesene
%define 	version 2.12.3
%define release 2

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	IM client for the Windows Live Messenger network and others
URL:		http://blog.emesene.org/
License:	Python Software Foundation License and GPLv3 and LGPLv3
Group:		Networking/Instant messaging
# Official tar.gz cleaned: 
#1. remove 'dlls' directory
#2. remove 'emesene/e3/papylib/papyon'
Source0:	%{name}-%{version}-0.tar.gz
Patch0:		emesene-2.12.3-desktop.patch
BuildArch:	noarch

Requires:	python >= 2.5
Requires:	python-dnspython
Requires:	pylint
Requires:	python-OpenSSL
Requires:	python-imaging
Requires:	dbus-python
Requires:	gnome-python-gtkspell

Requires:	%{name}-gui = %{version}-%{release}

Suggests:	python-webkitgtk
Suggests:	python-xmpp
Suggests:	python-papyon >= 0.5.5
Suggests: 	python-notify

Provides:       emesene2 = %{version}-%{release}

%description
Emesene is an OS independent Windows Live Messenger client writed in python and
GTK. The main idea is to make a client similar to the official Windows Live
Messenger client but kepping it simple and with a nice GUI.
 
Emesene is a python/GTK MSN messenger clone, it uses msnlib (MSNP9)
and try to be a nice looking and simple MSN client.

You can login, send formated messages, smilies, use autoreply, change
status, change nick, send nudges and all the stuff you can do in a
normal MSN client except, file transfers,custom emoticons and display
picture.

%package	gtk2
Summary:        emesene GTK interface for emesene client
Group:          Networking/Instant messaging
Provides:       emesene-gui = %{version}-%{release}
Requires:       pygtk2.0 >= 2.12
Requires:       %{name} = %{version}-%{release}

%description	gtk2
This contains the GTK interface for emesene.

%package	qt4
Summary:        emesene Qt4 interface for emesene client
Group:          Networking/Instant messaging
Provides:       emesene-gui = %{version}-%{release}
Requires:	python-qt4 >= 4.6
Requires:       %{name} = %{version}-%{release}

%description	qt4
This contains the Qt4 interface for emesene.

%prep
%setup -q -n %{name}
%patch0 -p0

find -name \*~ |xargs rm -fv

%build
python setup.py build_ext -ilm

%install
rm -rf $RPM_BUILD_ROOT %name.lang

install -D -m 644 docs/man/%name.1 %buildroot%_mandir/man1/%name.1
install -D -m 644 %name/data/pixmaps/%name.png %buildroot%_datadir/icons/hicolor/48x48/apps/%name.png
install -D -m 644 %name/data/icons/hicolor/scalable/apps/%name.svg %buildroot%_datadir/icons/hicolor/scalable/apps/%name.svg
install -D -m 644 %name/data/share/applications/emesene.desktop %buildroot%_datadir/applications/%name.desktop

cd %{name}

sed -i '/import e3dummy/d' emesene.py

# Copying files
mkdir -p %buildroot%_datadir/%{name}
cp -r * %buildroot%_datadir/%{name}

cd %buildroot%_datadir/%name

#delete Unity file
find . -type f -name UnityLauncher.py -exec rm -rf '{}' +
find . -type f -name .gitignore -exec rm -rf '{}' +
rm -rf debug*.list MANIFEST.in *.nsi *WINDOWS.txt *.translations setup.py *.developers %name.pot
find . -type f -name extension.py -exec chmod 755 '{}' +
find . -type f -name plugin_base.py -exec chmod 755 '{}' +
find . -type f -name e3_example.py -exec chmod 755 '{}' +
find . -type f -name emesene.py -exec chmod 755 '{}' +
find . -type f -name debugger.py -exec chmod 755 '{}' +
find . -type f -name SingleInstance.py -exec chmod 755 '{}' +
find . -type f -name pluginmanager.py -exec chmod 755 '{}' +

mkdir -p %buildroot%_bindir/
cat > %buildroot%_bindir/%name << EOF
#!/bin/sh
cd %_datadir/%name
exec ./%name
EOF

%files
%doc COPYING GPL LGPL
%attr(755,root,root) %_bindir/%name
%_datadir/%name/
%exclude %_datadir/%name/gui/gtkui
%exclude %_datadir/%name/gui/qt4ui
%_datadir/icons/hicolor/*/apps/%name.*
%_datadir/applications/%name.desktop
%_mandir/man1/%name.1*

%files gtk2
%_datadir/%name/gui/gtkui

%files qt4
%_datadir/%name/gui/qt4ui


%changelog
* Mon Jun 04 2012 Alexander Khrukin <akhrukin@mandriva.org> 2.12.3-1mdv2012.0
+ Revision: 802339
- version update 2.12.3

* Tue Apr 05 2011 Funda Wang <fwang@mandriva.org> 1.6.3-3
+ Revision: 650511
- fix linkage

  + Götz Waschk <waschk@mandriva.org>
    - fix icon extension on the scalable icon

* Wed Nov 03 2010 Götz Waschk <waschk@mandriva.org> 1.6.3-2mdv2011.0
+ Revision: 593002
- rebuild for new python 2.7

* Mon Jul 19 2010 Götz Waschk <waschk@mandriva.org> 1.6.3-1mdv2011.0
+ Revision: 554910
- new version

* Thu Jun 24 2010 Luis Medinas <lmedinas@mandriva.org> 1.6.2-1mdv2010.1
+ Revision: 549087
-new version
-Fixes a few critical bugs from the last version

* Mon Apr 19 2010 Götz Waschk <waschk@mandriva.org> 1.6.1-1mdv2010.1
+ Revision: 536709
- new version
- update file list

* Thu Jan 07 2010 Götz Waschk <waschk@mandriva.org> 1.6-1mdv2010.1
+ Revision: 487046
- new version
- update file list

* Fri Nov 06 2009 Götz Waschk <waschk@mandriva.org> 1.5.1-1mdv2010.1
+ Revision: 460839
- new version
- update file list

* Fri Aug 21 2009 Götz Waschk <waschk@mandriva.org> 1.5-4mdv2010.0
+ Revision: 418997
- replace some requirements by suggestions
- suggest gnash

* Fri Aug 21 2009 Götz Waschk <waschk@mandriva.org> 1.5-3mdv2010.0
+ Revision: 418956
- silent update of 1.5
- enable mimic support
- no more noarch
- add man page
- add icons to the default locations
- use upstream desktop entry
- many spec file fixes
- add comment about libmimic

* Fri Aug 21 2009 Götz Waschk <waschk@mandriva.org> 1.5-2mdv2010.0
+ Revision: 418882
- update deps

* Thu Aug 20 2009 Götz Waschk <waschk@mandriva.org> 1.5-1mdv2010.0
+ Revision: 418697
- update to new version 1.5

* Tue Sep 09 2008 Adam Williamson <awilliamson@mandriva.org> 1.0.1-3mdv2009.0
+ Revision: 283158
- doh, it already required pygtk2. can people PLEASE stop using multiple
  requires per line? it's utterly unreadable.

* Tue Sep 09 2008 Adam Williamson <awilliamson@mandriva.org> 1.0.1-2mdv2009.0
+ Revision: 282890
- requires pygtk2.0 (reported on forums by Simon Rogers)

* Mon Jul 21 2008 Götz Waschk <waschk@mandriva.org> 1.0.1-1mdv2009.0
+ Revision: 239334
- new version

* Tue Apr 08 2008 Götz Waschk <waschk@mandriva.org> 1.0-1mdv2009.0
+ Revision: 192406
- new version

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Dec 03 2007 Götz Waschk <waschk@mandriva.org> 0-0.20071202.1mdv2008.1
+ Revision: 114564
- new version

* Tue Aug 21 2007 Götz Waschk <waschk@mandriva.org> 0-0.20070821.1mdv2008.0
+ Revision: 68236
- new snapshot r801

* Tue Jul 03 2007 Götz Waschk <waschk@mandriva.org> 0-0.20070703.1mdv2008.0
+ Revision: 47631
- new version

* Thu May 24 2007 Götz Waschk <waschk@mandriva.org> 0-0.20070523.1mdv2008.0
+ Revision: 30608
- new version

