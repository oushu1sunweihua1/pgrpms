%global sname plsh

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

Summary:	Sh shell procedural language handler for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.20220917
Release:	1%{?dist}
License:	BSD
Source0:	https://github.com/petere/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/petere/plsh
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 1.20200522-2

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
PL/sh is a procedural language handler for PostgreSQL that
allows you to write stored procedures in a shell of your choice.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for plsh
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
This packages provides JIT support for plsh
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)

%{pginstdir}/lib/%{sname}.so
%doc NEWS COPYING README.md
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc COPYING
%else
%license COPYING
%endif
%{pginstdir}/share/extension/%{sname}--1--2.sql
%{pginstdir}/share/extension/%{sname}--2.sql
%{pginstdir}/share/extension/%{sname}--unpackaged--1.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Thu Sep 29 2022 Devrim G??nd??z <devrim@gunduz.org> - 1.20220917-1
- Update to 1.20220917
- Update llvm code

* Tue Oct 27 2020 Devrim G??nd??z <devrim@gunduz.org> - 1.20200522-3
- Remove pgxs patches, and  export PATH instead.

* Tue Oct 27 2020 Devrim G??nd??z <devrim@gunduz.org> - 1.20200522-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Wed Aug 12 2020 Devrim G??nd??z <devrim@gunduz.org> - 1.20200522-1
- Update to 1.20200522

* Thu Sep 26 2019 Devrim G??nd??z <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Sun Jan 20 2019 Devrim G??nd??z <devrim@gunduz.org> - 1.20171014-1.2
- Fix PostgreSQL 11 builds

* Mon Oct 15 2018 Devrim G??nd??z <devrim@gunduz.org> - 1.20171014-1.1
- Rebuild against PostgreSQL 11.0

* Tue Mar 27 2018 - Devrim G??nd??z <devrim@gunduz.org> 1.20171014
- Update to 1.20171014

* Tue Jan 26 2016 - Devrim G??nd??z <devrim@gunduz.org> 1.20130823-2
- Cosmetic cleanup
- Use more macros for unified spec file

* Mon Mar 17 2014 - Devrim G??nd??z <devrim@gunduz.org> 1.20130823-1
- Update to 1.20130823
- Update download URL

* Tue Nov 27 2012 - Devrim G??nd??z <devrim@gunduz.org> 1.20121018-1
- Rewrite the spec file based on the new version, and update
  to 1.20121018

* Sun Jan 20 2008 - Devrim G??nd??z <devrim@gunduz.org> 1.3-2
- Move .so file to the correct directory

* Tue Jan 15 2008 - Devrim G??nd??z <devrim@gunduz.org> 1.3-1
- Initial RPM packaging for Fedora
