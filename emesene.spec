%define name emesene
%define version 0
%define snapshot 230507
%define date 20070523
%define release %mkrel 0.%date.1

Summary: OS independent MSN Messenger client
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://downloads.sourceforge.net/emesene/%{name}-%{snapshot}.tar.bz2
License: GPL
Group: Networking/Instant messaging
Url: http://emesene-msn.blogspot.com/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
Requires: python pygtk2.0
Requires: dbus-python
# gw for aplay
Requires: alsa-utils
# gw for egg.trayicon
Requires: gnome-python-extras
Requires: python-notify

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
%setup -q -n %name

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %buildroot%_datadir/
cp -r ../%name %buildroot%_datadir/
rm -rf %buildroot%_datadir/%name/docs \
      %buildroot%_datadir/%name/COPYING \
      %buildroot%_datadir/%name/emesene.bat \
      %buildroot%_datadir/%name/plugins_base/Winamp.py      

mkdir -p %buildroot%_bindir/
cat > %buildroot%_bindir/%name << EOF
#!/bin/sh
cd %_datadir/%name
exec ./%name
EOF

mkdir -p %buildroot%_datadir/applications
cat > %buildroot%_datadir/applications/mandriva-%name.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Emesene
Comment=OS Independent Msn Messenger
Exec=emesene
Icon=%_datadir/emesene/themes/default/userPanel.png
Categories=Network;X-MandrivaLinux-Internet-InstantMessaging;InstantMessaging;GTK;
EOF


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING docs/*
%attr(755,root,root) %_bindir/%name
%_datadir/%name
%_datadir/applications/mandriva-%name.desktop


