%define realname ViewARCH
%define realversion 0.0.12-9

Summary: An archive browser for GNU arch
Name:    viewarch
Version: %(echo %realversion | sed 's/-/_/g')
Release: 10
Source0: %{realname}-%{realversion}.tar.bz2
Patch0: %name-confpath.patch
License: GPL
Group: Networking/WWW
Url: http://arch.bluegate.org/viewarch.html
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
rm -rf %{buildroot}

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
rm -rf %{buildroot}



%files
%defattr(-,root,root)
%_datadir/%name
%_var/www/cgi-bin/viewarch.cgi
%config(noreplace) %_sysconfdir/httpd/conf/webapps.d/%name.conf
%dir %_sysconfdir/%name
%config(noreplace) %_sysconfdir/%name/viewarch.conf



%changelog
* Wed Dec 08 2010 Oden Eriksson <oeriksson@mandriva.com> 0.0.12_9-8mdv2011.0
+ Revision: 615390
- the mass rebuild of 2010.1 packages

* Sun Jan 17 2010 Guillaume Rousse <guillomovitch@mandriva.org> 0.0.12_9-7mdv2010.1
+ Revision: 492716
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Wed Sep 09 2009 Thierry Vignaud <tv@mandriva.org> 0.0.12_9-6mdv2010.0
+ Revision: 434672
- rebuild

* Sun Aug 03 2008 Thierry Vignaud <tv@mandriva.org> 0.0.12_9-5mdv2009.0
+ Revision: 261850
- rebuild

* Wed Jul 30 2008 Thierry Vignaud <tv@mandriva.org> 0.0.12_9-4mdv2009.0
+ Revision: 255522
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0.0.12_9-2mdv2008.1
+ Revision: 136570
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Thu Aug 10 2006 Olivier Thauvin <nanardon@mandriva.org>
+ 08/10/06 01:39:12 (55286)
- rebuild

* Thu Aug 10 2006 Olivier Thauvin <nanardon@mandriva.org>
+ 08/10/06 01:38:12 (55285)
Import viewarch

* Thu Mar 02 2006 Olivier Thauvin <nanardon@mandriva.org> 
- initial rpm

