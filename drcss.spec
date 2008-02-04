%define name    drcss
%define version 2.0
%define release %mkrel 1

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Dell Remote Console Switch Software
License:        Commercial
Group:          Office
Source0:        setup.bin
Requires:       java
BuildRequires:  ImageMagick
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
The DellTM Remote Console Switch Software is a cross-platform management
application that allows you to view and control the Dell 2161DS Console Switch
and all its attached servers. The cross-platform design ensures compatibility
with most popular operating systems and hardware platforms. The Remote Console
Switch Software provides secure switch-based authentication, data transfers,
and username/password storage. Each 2161DS Console Switch handles
authentication and access control individually for more decentralized system
control.

%prep
%setup -q -c -T
# skip = (JREREALSIZE / 32768) + 1 + JRESTART
dd if=%{SOURCE0} of=installer.zip bs=32768 skip=643 count=344
unzip installer.zip
%setup -D -T -n '%{name}-%{version}/$IA_PROJECT_DIR$

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_datadir}/drcss
install -d -m 755 %{buildroot}%{_bindir}
install -m 644 build/*.jar %{buildroot}%{_datadir}/drcss
install -m 644 build/*.dat %{buildroot}%{_datadir}/drcss

unzip build/help_zg_ia_sf.jar -d %{buildroot}%{_datadir}/drcss/help || /bin/true
rm -f {buildroot}%{_datadir}/drcss/help_zg_ia_sf.jar

cat > %{buildroot}%{_bindir}/drcss<< 'EOF'
#!/bin/sh
for jar in \
    MibII.jar \
    MibAvocentDs.jar \
    hsqldb.jar \
    brand.jar \
    avctVideo.jar \
    avctProtocols.jar \
    avctAVWorksServices.jar \
    avctAVWorksNmm.jar \
    avctAVWorksGenericNmm.jar \
    avctAVWorksExplorer.jar \
    avctAVWorksAvrNmm.jar \
    avctViewerApi.jar \
    avctUtil.jar \
    avctNet.jar \
    avctGUI.jar \
    avctDB.jar \
    lax.jar; do
    CLASSPATH="$CLASSPATH:%{_datadir}/drcss/$jar"
done
export CLASSPATH
cd %{_datadir}/drcss
java \
    -Duser.variant=dell \
    com.avocent.avworks.explorer.JFrameExplorer
EOF
chmod 755 %{buildroot}%{_bindir}/drcss

install -d -m 755 %{buildroot}%{_datadir}/icons
convert images/gnome-dellicon32.gif %{buildroot}%{_datadir}/icons/drcss.png

install -d -m 755 %{buildroot}%{_datadir}/applications
cat >  %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=drcss
Comment=Dell Remote Console Switch Software
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc src/license_en.txt
%{_datadir}/drcss
%{_bindir}/drcss
%{_datadir}/icons/drcss.png
%{_datadir}/applications/mandriva-%{name}.desktop

