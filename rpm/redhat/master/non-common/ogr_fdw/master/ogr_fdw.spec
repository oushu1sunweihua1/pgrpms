%global sname ogr_fdw

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	PostgreSQL foreign data wrapper for OGR
Name:		%{sname}_%{pgmajorversion}
Version:	1.0.12
Release:	3%{?dist}
License:	BSD
Source0:	https://github.com/pramsey/pgsql-ogr-fdw/archive/v%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
Patch2:		ogr_fdw-makefile-gdal31.patch
URL:		https://github.com/pramsey/pgsql-ogr-fdw
BuildRequires:	postgresql%{pgmajorversion}-devel gdal31-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server gdal31-libs

Obsoletes:	%{sname}%{pgmajorversion} < 1.0.12-3

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
This library contains a PostgreSQL extension, a Foreign Data Wrapper (FDW)
handler of PostgreSQL which provides easy way for interacting with OGR.

%prep
%setup -q -n pgsql-ogr-fdw-%{version}
%patch0 -p0
%patch2 -p0

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif
%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{pginstdir}/
%{__install} -d %{buildroot}%{pginstdir}/bin/
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
%{__install} -m 755 README.md %{buildroot}%{pginstdir}/share/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{_docdir}/pgsql/extension/README.md

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/share/extension/README-%{sname}.md
%attr (755,root,root) %{pginstdir}/bin/ogr_fdw_info
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--1.0.sql
%{pginstdir}/share/extension/%{sname}.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
  %endif
 %endif
%endif

%changelog
* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.0.12-3
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Aug 20 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.12-2
- Rebuild against GDAL 3.1.2

* Wed Aug 12 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.12-1
- Update to 1.0.12

* Mon Nov 4 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.9-1
- Update to 1.0.9

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.8-2.1
- Rebuild for PostgreSQL 12

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.8-2
- Use our gdal30 package

* Wed Aug 7 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.8-1
- Update to 1.0.8
- Use our gdal23 packages

* Tue Oct 16 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0.7-1
- Update to 1.0.7
- Install bitcode files.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0.5-1.1
- Rebuild against PostgreSQL 11.0

* Sun Jul 1 2018 Devrim Gündüz <devrim@gunduz.org> 1.0.5-1
- Update to 1.0.5

* Sat Oct 14 2017 Devrim Gündüz <devrim@gunduz.org> 1.0.4-1
- Update to 1.0.4

* Sat Aug 13 2016 Devrim Gündüz <devrim@gunduz.org> 1.0.2-1
- Update to 1.0.2

* Wed Jan 06 2016 Devrim Gündüz <devrim@gunduz.org> 1.0.1-1
- Update to 1.0.1

* Mon Sep 21 2015 - Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
