%global sname multicorn2
%global pname multicorn

%if 0%{?fedora} >= 35
%{expand: %%global pyver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global pyver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
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

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	Multicorn Python bindings for Postgres FDW
Name:		%{sname}_%{pgmajorversion}
Version:	2.3
Release:	1%{?dist}
License:	PostgreSQL
Source0:	https://github.com/pgsql-io/%{sname}/archive/refs/tags/v%{version}.tar.gz
Patch0:		%{sname}-python-destdir.patch
URL:		https://github.com/pgsql-io/%{version}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
BuildRequires:	python3-devel

Obsoletes:	%{pname}%{pgmajorversion} < 1.4.0-10
Obsoletes:	%{pname}_%{pgmajorversion} < 1.4.0-10

# Provide versionless multicorn. This will simplify using
# bigquery_fdw package.
Provides:	%{sname} = %{version}

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
Multicorn Python3 Wrapper for Postgresql Foreign Data Wrapper. Tested
on Linux w/ Python 3.6+ & Postgres 10+.

The Multicorn Foreign Data Wrapper allows you to fetch foreign data in
Python in your PostgreSQL server.

Multicorn2 is distributed under the PostgreSQL license. See the LICENSE
file for details.The Multicorn Foreign Data Wrapper allows you to write
foreign data wrappers in Python.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for Multicorn
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} == 1315
Requires:	llvm
%endif
%if 0%{?suse_version} >= 1500
Requires:	llvm10
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 5.0
%endif

%description llvmjit
This packages provides JIT support for Multicorn
%endif

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

export PYTHON_OVERRIDE="python%{pyver}"
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif
export PYTHON_OVERRIDE="python%{pyver}"
PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc README.md
%dir %{python3_sitearch}/%{pname}-%{version}-py%{pyver}.egg-info
%{python3_sitearch}/%{pname}-%{version}-py%{pyver}.egg-info/*
%{python3_sitearch}/%{pname}/__pycache__/*.pyc
%{python3_sitearch}/%{pname}/_*.so
%{python3_sitearch}/%{pname}/fsfdw/*.py
%{python3_sitearch}/%{pname}/fsfdw/__pycache__/*.pyc
%{python3_sitearch}/%{pname}/*.py
%{pginstdir}/doc/extension/%{pname}.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}*.sql
%{pginstdir}/share/extension/%{pname}.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{pname}*.bc
    %{pginstdir}/lib/bitcode/%{pname}/src/*.bc
%endif

%changelog
* Sat Jun 11  2022 Devrim G??nd??z <devrim@gunduz.org> 2.3-1
- Switch to new repo

* Tue Oct 27 2020 Devrim G??nd??z <devrim@gunduz.org> 1.4.0-4
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim G??nd??z <devrim@gunduz.org> 1.4.0-3
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Tue May 19 2020 - Devrim G??nd??z <devrim@gunduz.org> 1.4.0-2
- Provide versionless multicorn. This will simplify using
  bigquery_fdw package.

* Sat Mar 21 2020 - Devrim G??nd??z <devrim@gunduz.org> 1.4.0-1
- Update to 1.4.0

* Mon Oct 15 2018 Devrim G??nd??z <devrim@gunduz.org> - 1.3.5-1.1
- Rebuild against PostgreSQL 11.0

* Fri Jan 12 2018 - Devrim G??nd??z <devrim@gunduz.org> 1.3.5-1
- Update to 1.3.5, per #2888 .

* Tue Nov 21 2017 - Devrim G??nd??z <devrim@gunduz.org> 1.3.4-1
- Update to 1.3.4, per #2888 .

* Mon Mar 6 2017 - Devrim G??nd??z <devrim@gunduz.org> 1.3.3-1
- Update to 1.3.3, per #2224 .

* Thu Mar 3 2016 - Devrim G??nd??z <devrim@gunduz.org> 1.3.2-1
- Update to 1.3.2

* Mon Jan 18 2016 - Devrim G??nd??z <devrim@gunduz.org> 1.3.1-1
- Update to 1.3.1

* Thu Dec 10 2015 - Devrim G??nd??z <devrim@gunduz.org> 1.2.4-1
- Update to 1.2.4

* Wed Jan 21 2015 - Devrim G??nd??z <devrim@gunduz.org> 1.2.3-1
- Initial packaging for PostgreSQL RPM Repository
