%global sname pg_squeeze
%global pgsqueezerelversion 1_5_0

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	A PostgreSQL extension for automatic bloat cleanup
Name:		%{sname}_%{pgmajorversion}
Version:	1.5.0
Release:	1%{?dist}
License:	PostgreSQL
Source0:	https://github.com/cybertec-postgresql/pg_squeeze/archive/REL%{pgsqueezerelversion}.tar.gz
URL:		https://github.com/cybertec-postgresql/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 1.3.0-2

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
pg_squeeze is an extension that removes unused space from a table and
optionally sorts tuples according to particular index (as if CLUSTER
command was executed concurrently with regular reads / writes).

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_squeeze
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
Requires:	llvm => 5.0
%endif

%description llvmjit
This packages provides JIT support for pg_squeeze
%endif

%prep
%setup -q -n %{sname}-REL%{pgsqueezerelversion}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension/
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%clean
%{__rm} -rf %{buildroot}

%files
%license LICENSE
%defattr(644,root,root,755)
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/lib/%{sname}.so
%doc %{pginstdir}/doc/extension/README-%{sname}.md

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Thu Oct 6 2022 Devrim G??nd??z <devrim@gunduz.org> - 1.5.0-1
- Update to 1.5.0
- Split llvmjit into its own subpackage.

* Fri Feb 18 2022 John Harvey <john.harvey@crunchydata.com> - 1.4.1-2
- Update license to match source code

* Fri Sep 24 2021 Devrim G??nd??z <devrim@gunduz.org> - 1.4.1-1
- Update to 1.4.1

* Mon Sep 13 2021 Devrim G??nd??z <devrim@gunduz.org> - 1.4.0-1
- Update to 1.4.0

* Wed Jun 2 2021 Devrim G??nd??z <devrim@gunduz.org> - 1.3.1-1
- Update to 1.3.1
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim G??nd??z <devrim@gunduz.org> - 1.3.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Sat Sep 26 2020 Devrim G??nd??z <devrim@gunduz.org> - 1.3.0-1
- Update to 1.3.0

* Thu Sep 26 2019 Devrim G??nd??z <devrim@gunduz.org> - 1.2.0-1.1
- Rebuild for PostgreSQL 12

* Mon Aug 26 2019 Devrim G??nd??z <devrim@gunduz.org> - 1.2.0-1
- Update to 1.2.0

* Mon Nov 5 2018 Devrim G??nd??z <devrim@gunduz.org> - 1.1.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
