%global sname tds_fdw

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	TDS Foreign Data Wrapper for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	2.0.3
Release:	1%{?dist}
License:	BSD
Source0:	https://github.com/tds-fdw/%{sname}/archive/v%{version}.zip
URL:		https://github.com/tds-fdw/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel freetds-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server freetds

Obsoletes:	%{sname}%{pgmajorversion} < 2.0.2-2

%description
This library contains a single PostgreSQL extension, a foreign data wrapper
called "tds_fdw". It can be used to communicate with Microsoft SQL
Server and Sybase databases.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for tds_fdw
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:  llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:  llvm13-devel clang13-devel
Requires:	llvm13
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for tds_fdw
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make}  DESTDIR=%{buildroot} %{?_smp_mflags} install

# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__install} -m 644 ForeignSchemaImporting.md %{buildroot}%{pginstdir}/doc/extension/ForeignSchemaImporting-%{sname}.md
%{__install} -m 644 ForeignServerCreation.md %{buildroot}%{pginstdir}/doc/extension/ForeignServerCreation-%{sname}.md
%{__install} -m 644 ForeignTableCreation.md %{buildroot}%{pginstdir}/doc/extension/ForeignTableCreation-%{sname}.md
%{__install} -m 644 UserMappingCreation.md %{buildroot}%{pginstdir}/doc/extension/UserMappingCreation-%{sname}.md
%{__install} -m 644 Variables.md %{buildroot}%{pginstdir}/doc/extension/Variables-%{sname}.md
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%{__rm} -f %{buildroot}/%{pginstdir}/doc/extension/README.%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/*%{sname}.md
%{pginstdir}/share/extension/%{sname}--%{version}.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/lib/%{sname}.so

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Sat Oct 22 2022 Devrim G??nd??z <devrim@gunduz.org> - 2.0.3-1
- Update to 2.0.3
- Split llvm stuff into its own subpackage.

* Wed Jun 2 2021 Devrim G??nd??z <devrim@gunduz.org> - 2.0.2-3
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim G??nd??z <devrim@gunduz.org> - 2.0.2-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Sun Sep 27 2020 - Devrim G??nd??z <devrim@gunduz.org> 2.0.2-1
- Update to 2.0.2

* Wed Dec 4 2019 - Devrim G??nd??z <devrim@gunduz.org> 2.0.1-1
- Update to 2.0.1

* Sat Jan 19 2019 - Devrim G??nd??z <devrim@gunduz.org> 2.0.0-alpha.3
- Update to 2.0.0-alpha.3 for testing repo only.

* Mon Oct 15 2018 Devrim G??nd??z <devrim@gunduz.org> - 2.0.0-alpha.2_1.1
- Rebuild against PostgreSQL 11.0

* Tue Jul 31 2018 - Devrim G??nd??z <devrim@gunduz.org> 2.0.0-alpha.2
- Update to 2.0.0-alpha.2 for testing repo only.

* Fri Oct 28 2016 - Devrim G??nd??z <devrim@gunduz.org> 1.0.8-1
- Update to 1.0.8
- Change links to point to github.

* Thu Jan 7 2016 - Devrim G??nd??z <devrim@gunduz.org> 1.0.7-1
- Update to 1.0.7
- Apply 9.5 doc layout.

* Mon Jan 4 2016 - Devrim G??nd??z <devrim@gunduz.org> 1.0.6-1
- Update to 1.0.6

* Fri Sep 25 2015  - Devrim G??nd??z <devrim@gunduz.org> 1.0.5-1
- Initial packaging for PostgreSQL RPM Repository
