%define 	name 	emesene
%define 	version 2.12.3
%define 	release %mkrel 1

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
