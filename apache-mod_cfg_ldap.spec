#Module-Specific definitions
%define mod_name mod_cfg_ldap
%define mod_conf A15_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Keeping apache VirtualHost configuration in a LDAP directory
Name:		apache-%{mod_name}
Version:	1.2
Release:	18
Group:		System/Servers
License:	BSD
URL:		https://sourceforge.net/projects/modcfgldap/
Source0: 	https://downloads.sourceforge.net/project/modcfgldap/mod_cfg_ldap/%{version}/mod_cfg_ldap-%{version}.tar.gz
Source1:	%{mod_conf}.xz
BuildRequires:	pkgconfig(ldap)
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
%autosetup -p1 -n %{mod_name}-%{version}
sed -i -e 's,ldap_r,ldap,g' Makefile

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
%{_bindir}/apxs -c %{mod_name}.c -lldap

%install
install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
xzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
	systemctl restart httpd
fi

%postun
if [ "$1" = "0" ]; then
	if [ -f %{_var}/lock/subsys/httpd ]; then
		systemctl restart httpd
	fi
fi

%files
%doc AUTHORS ChangeLog INSTALL README TODO mod_cfg_ldap.schema
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
