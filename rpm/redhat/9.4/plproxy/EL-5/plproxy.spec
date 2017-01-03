%global pgmajorversion 94
%global pginstdir /usr/pgsql-9.4
%global sname plproxy

Summary:	PL/Proxy is database partitioning system implemented as PL language.
Name:		%{sname}%{pgmajorversion}
Version:	2.7
Release:	1%{?dist}
Group:		Applications/Databases
License:	BSD
URL:		https://plproxy.github.io
Source0:	https://plproxy.github.io/downloads/files/%{version}/%{sname}-%{version}.tar.gz
Patch0:		Makefile-pgxs.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	postgresql%{pgmajorversion}-devel flex >= 2.5.4
Requires:	postgresql%{pgmajorversion}

%description
PL/Proxy is database partitioning system implemented as PL language.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p1

%build
USE_PGXS=1 make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 make %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc README.md AUTHORS COPYRIGHT
%else
%license COPYRIGHT
%doc README.md AUTHORS COPYRIGHT
%endif
%{pginstdir}/lib/plproxy.so
%{pginstdir}/share/extension/plproxy--2.3.0--2.7.0.sql
%{pginstdir}/share/extension/plproxy--2.4.0--2.7.0.sql
%{pginstdir}/share/extension/plproxy--2.5.0--2.7.0.sql
%{pginstdir}/share/extension/plproxy--2.6.0--2.7.0.sql
%{pginstdir}/share/extension/plproxy--2.7.0.sql
%{pginstdir}/share/extension/plproxy--unpackaged--2.7.0.sql
%{pginstdir}/share/extension/plproxy.control

%changelog
* Mon Jan 2 2017 - Devrim Gündüz <devrim@gunduz.org> 2.7-1
- Update to 2.7

* Fri Sep 11 2015 - Devrim Gündüz <devrim@gunduz.org> 2.6-1
- Update to 2.6

* Tue Jan 15 2013 - Devrim Gündüz <devrim@gunduz.org> 2.5-1
- Update to 2.5

* Fri Jul 27 2012 - Devrim Gündüz <devrim@gunduz.org> 2.4-1
- Update to 2.4
- Update download URL.

* Mon Feb 13 2012 - Devrim Gündüz <devrim@gunduz.org> 2.3-1
- Update to 2.3

* Tue Oct 12 2010 - Devrim Gündüz <devrim@gunduz.org> 2.1-2
- Apply 9.0 related changes to spec file.
- Get rid of ugly hacks in spec.

* Sat May 15 2010 - Devrim Gündüz <devrim@gunduz.org> 2.1-1
- Update to 2.1

* Wed Oct 28 2009 - Devrim Gündüz <devrim@gunduz.org> 2.0.9-1
- Update to 2.0.9

* Mon Feb 2 2009 - Devrim Gündüz <devrim@gunduz.org> 2.0.8-1
- Update to 2.0.8

* Tue Oct 7 2008 - Devrim Gündüz <devrim@gunduz.org> 2.0.7-1
- Update to 2.0.7

* Sat Sep 20 2008 - Devrim Gündüz <devrim@gunduz.org> 2.0.6-1
- Update to 2.0.6

* Sun Jun 15 2008 - Devrim Gündüz <devrim@gunduz.org> 2.0.5-1
- Update to 2.0.5
- Remove scanner.c and scanner.h, they are no longer needed.

* Tue Aug 28 2007 - Devrim Gündüz <devrim@gunduz.org> 2.0.2-2
- Add pre-generated scanner.c and scanner.h as sources. Only very
recent versions of flex can compile plproxy.

* Tue Aug 28 2007 - Devrim Gündüz <devrim@gunduz.org> 2.0.2-1
- Initial build 
