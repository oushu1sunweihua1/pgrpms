%if 0%{?rhel} && 0%{?rhel} <= 6
%global systemd_enabled 0
%else
%global systemd_enabled 1
%endif

Summary:	PostgreSQL performance monitoring and auditing tool
Name:		pgcluu
Version:	3.0
Release:	1%{?dist}
License:	BSD
Source0:	https://github.com/darold/%{name}/archive/v%{version}.tar.gz
Patch0:		%{name}-systemd-rpm-paths.patch
URL:		http://%{name}.darold.net/
BuildArch:	noarch

%description
pgCluu is a PostgreSQL performances monitoring and auditing tool.
View reports of all statistics collected from your PostgreSQL
databases cluster. pgCluu will show you the entire information
of the PostgreSQL cluster and the system utilization

%prep
%setup -q
%patch0 -p0

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install PERL_INSTALL_ROOT=%{buildroot}

%if %{systemd_enabled}
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{name}_collectd.service %{name}.service %{name}.timer %{buildroot}%{_unitdir}/
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc ChangeLog
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}_collectd
%perl_vendorarch/auto/pgCluu/.packlist
%{_mandir}/man1/%{name}.1p.gz
%if %{systemd_enabled}
%{_unitdir}/%{name}_collectd.service
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.timer
%endif

%changelog
* Fri Sep 27 2019 Devrim Gündüz <devrim@gunduz.org> 3.0-1
- Update to 3.0

* Wed Jan 2 2019 Devrim Gündüz <devrim@gunduz.org> 2.9-1
- Update to 2.9

* Tue Dec 11 2018 Devrim Gündüz <devrim@gunduz.org> 2.8-1
- Update to 2.8

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.6-2.1
- Rebuild against PostgreSQL 11.0

* Sat Jul 15 2017 Devrim Gündüz <devrim@gunduz.org> 2.6-1
- Update to 2.6
- Install systemd related files.
- Add a patch to fix paths in unit files.

* Sat Aug 13 2016 Devrim Gündüz <devrim@gunduz.org> 2.5-1
- Update to 2.5

* Fri Sep 11 2015 Devrim Gündüz <devrim@gunduz.org> 2.4-1
- Update to 2.4
- Fix rpmlint warning (add %%build section)
- Update download URL

* Sun Jan 11 2015 Devrim Gündüz <devrim@gunduz.org> 2.2-1
- Update to 2.2

* Fri Sep 26 2014 Devrim Gündüz <devrim@gunduz.org> 2.1-1
- Update to 2.1

* Tue Apr 1 2014 Devrim Gündüz <devrim@gunduz.org> 2.0-1
- Update to 2.0

* Wed Jan 15 2014 Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
