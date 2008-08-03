%define name viewarch
%define realname ViewARCH
%define realversion 0.0.12-9
%define version %(echo %realversion | sed 's/-/_/g')
%define release %mkrel 5

Summary: An archive browser for GNU arch
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{realname}-%{realversion}.tar.bz2
Patch0: %name-confpath.patch
License: GPL
Group: Networking/WWW
Url: http://arch.bluegate.org/viewarch.html
BuildRoot: %{_tmppath}/%{name}-buildroot
Requires: tla
Requires: python
Requires: apache
BuildArch: noarch

%description
An archive browser for GNU arch.

%prep
%setup -q -n %realname-%realversion -q
%patch0 -p0 -b .confpath

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p %buildroot/%_datadir/%name/lib
mkdir -p %buildroot/%_sysconfdir/%name
mkdir -p %buildroot/%_sysconfdir/httpd/conf/webapps.d
mkdir -p %buildroot/%_var/www/cgi-bin

/bin/cp -a cgi/viewarch.cgi %buildroot/%_var/www/cgi-bin/viewarch.cgi

perl -pi -e "s:^LIB_DIR = None:LIB_DIR = '%_datadir/%name/lib':" \
    %buildroot/%_var/www/cgi-bin/viewarch.cgi

/bin/cp -r lib/{*.py,*.pot} %buildroot/%_datadir/%name/lib/

perl -pi -e "s:^#!/usr/local/bin/python:#!/usr/bin/python:" \
    %buildroot/%_datadir/%name/lib/*.py

/bin/cp -r locale %buildroot/%_datadir/%name/
/bin/cp -r templates %buildroot/%_datadir/%name/

/bin/cp -r viewarch.conf.dist %buildroot/%_sysconfdir/%name/viewarch.conf

cat > %buildroot/%_sysconfdir/httpd/conf/webapps.d/%name.conf <<EOF
<IfModule mod_alias.c>
    ScriptAlias /%name/ /%_var/www/cgi-bin/viewarch.cgi
</IfModule>

<Directory /var/www/%name>
    AllowOverride All
    Options ExecCGI
    DirectoryIndex viewarch.cgi
    Order allow,deny
    Allow from all
</Directory>
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_webapp

%postun
%_postun_webapp

%files
%defattr(-,root,root)
%_datadir/%name
%_var/www/cgi-bin/viewarch.cgi
%config(noreplace) %_sysconfdir/httpd/conf/webapps.d/%name.conf
%dir %_sysconfdir/%name
%config(noreplace) %_sysconfdir/%name/viewarch.conf

