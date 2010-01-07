%define name emesene
%define version 1.6
%define release %mkrel 1

Summary: OS independent MSN Messenger client
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://downloads.sourceforge.net/emesene/%{name}-%{version}.tar.gz
Patch: emesene-1.5-desktopentry.patch
License: GPLv2+ and LGPLv2+
Group: Networking/Instant messaging
Url: http://emesene-msn.blogspot.com/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: python-devel
Requires: python
Requires: pygtk2.0
Requires: dbus-python
# gw for aplay
Requires: alsa-utils
# gw for egg.trayicon
Requires: gnome-python-extras
#gw spell checker:
Suggests: gnome-python-gtkspell
#gw for wink animations:
Suggests: cabextract gnash
Suggests: python-notify

%description
Emesene is an OS independent MSN Messenger client writed in python and
GTK. The main idea is to make a client similar to the official MSN
Messenger client but kepping it simple and with a nice GUI.

 
Emesene is a python/gtk MSN messenger clone, it uses msnlib (MSNP9)
and try to be a nice looking and simple MSN client.

You can login, send formated messages, smilies, use autoreply, change
status, change nick, send nudges and all the stuff you can do in a
normal MSN client except, file transfers,custom emoticons and display
picture.

%prep
%setup -q
%patch -p2
find -name \*~ |xargs rm -fv

%build
python setup.py build_ext -i

%install
rm -rf $RPM_BUILD_ROOT %name.lang

install -D -m 644 misc/%name.1 %buildroot%_mandir/man1/%name.1
install -D -m 644 misc/%name.png %buildroot%_datadir/icons/hicolor/48x48/apps/%name.png
install -D -m 644 misc/%name.svg %buildroot%_datadir/icons/hicolor/scalable/apps/%name.png
install -D -m 644 misc/%name.desktop %buildroot%_datadir/applications/%name.desktop

mkdir -p %buildroot%_libdir/
cp -r ../%name-%version %buildroot%_libdir/%name
cd %buildroot%_libdir/%name
rm -rf COPYING README GPL LGPL emesene.bat Winamp.py misc/%name.desktop misc/%name.1 libmimic build setup.py po/templates/ %name.pot PKG-INFO PSF debug*.list MANIFEST.in
cd po
for dir in *;do echo "%lang($dir) %_libdir/%name/po/$dir" >> $RPM_BUILD_DIR/%name-%version/%name.lang
done





mkdir -p %buildroot%_bindir/
cat > %buildroot%_bindir/%name << EOF
#!/bin/sh
cd %_libdir/%name
exec ./%name
EOF

%if %mdkversion < 200900
%post
%update_icon_cache hicolor
%postun
%clean_icon_cache hicolor
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %name.lang
%defattr(-,root,root)
%doc README COPYING
%attr(755,root,root) %_bindir/%name
%_mandir/man1/%name.1*
%_datadir/icons/hicolor/*/apps/%name.png
%dir %_libdir/%name
%_libdir/%name/%name
%_libdir/%name/*.py
%_libdir/%name/*.png
%_libdir/%name/abstract
%_libdir/%name/conversation_themes
%_libdir/%name/emesenelib
%_libdir/%name/hotmlog.htm
%_libdir/%name/libmimic.so
%_libdir/%name/misc
%_libdir/%name/plugins_base
%_libdir/%name/smilies
%_libdir/%name/sound_themes
%_libdir/%name/themes
%dir %_libdir/%name/po
%_datadir/applications/%name.desktop


