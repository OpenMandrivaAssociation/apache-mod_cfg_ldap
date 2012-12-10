#Module-Specific definitions
%define mod_name mod_cfg_ldap
%define mod_conf A15_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Keeping apache VirtualHost configuration in a LDAP directory
Name:		apache-%{mod_name}
Version:	1.2
Release:	16
Group:		System/Servers
License:	BSD
URL:		http://sourceforge.net/projects/modcfgldap/
Source0: 	%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
BuildRequires:	openldap-devel
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
Epoch:		1

%description
mod_cfg_ldap allows you to keep your virtual host configuration in
a LDAP directory and update it in nearly realtime.

%prep

%setup -q -n %{mod_name}-%{version}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
%{_bindir}/apxs -c %{mod_name}.c -lldap_r

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean

%files
%doc AUTHORS ChangeLog INSTALL README TODO mod_cfg_ldap.schema
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1:1.2-16mdv2012.0
+ Revision: 772604
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.2-15
+ Revision: 678290
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.2-14mdv2011.0
+ Revision: 587948
- rebuild

* Fri Apr 23 2010 Funda Wang <fwang@mandriva.org> 1:1.2-13mdv2010.1
+ Revision: 538085
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.2-12mdv2010.1
+ Revision: 516076
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.2-11mdv2010.0
+ Revision: 406560
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.2-10mdv2009.1
+ Revision: 325673
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.2-9mdv2009.0
+ Revision: 234838
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.2-8mdv2009.0
+ Revision: 215555
- fix rebuild

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.2-7mdv2008.1
+ Revision: 181711
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.2-6mdv2008.0
+ Revision: 82544
- rebuild

* Sat Aug 18 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.2-5mdv2008.0
+ Revision: 65631
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 1.2-4mdv2007.1
+ Revision: 140656
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.2-3mdv2007.0
+ Revision: 79378
- Import apache-mod_cfg_ldap

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.2-3mdv2007.0
- rebuild

* Wed Dec 14 2005 Oden Eriksson <oeriksson@mandriva.com> 1:1.2-2mdk
- rebuilt against apache-2.2.0

* Mon Nov 28 2005 Oden Eriksson <oeriksson@mandriva.com> 1:1.2-1mdk
- fix versioning

* Sat Sep 17 2005 Buchan Milne <bgmilne@linux-mandrake.com> 2.0.54_1.2-3mdk
- Rebuild

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_1.2-2mdk
- fix deps

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_1.2-1mdk
- rename the package
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_1.2-4mdk
- use the %1

* Mon Feb 28 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_1.2-3mdk
- fix %%post and %%postun to prevent double restarts
- fix bug #6574

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_1.2-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Mon Feb 14 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_1.2-1mdk
- 1.2

* Tue Feb 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_1.1-1mdk
- rebuilt for apache 2.0.53

* Wed Sep 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.52_1.1-1mdk
- built for apache 2.0.52

* Fri Sep 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.51_1.1-1mdk
- built for apache 2.0.51

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_1.1-1mdk
- built for apache 2.0.50
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.49_1.1-1mdk
- 1.1
- built for apache 2.0.49

