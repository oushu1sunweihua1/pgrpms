%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	A wrapper library for the Firebird C API
Name:		libfq
Version:	0.4.3
Release:	2%{dist}
Source:		https://github.com/ibarwick/%{name}/archive/%{version}.tar.gz
URL:		https://github.com/ibarwick/%{name}
License:	PostgreSQL
Group:		Development/Libraries/C and C++
BuildRequires:	firebird-devel

%if 0%{?rhel} && 0%{?rhel} == 7
BuildRequires:	firebird-libfbclient
Requires:	firebird-libfbclient
%else
BuildRequires:	libfbclient2
Requires:	libfbclient2
%endif

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
A wrapper library for the Firebird C API, loosely based on libpq for PostgreSQL.

%prep
%setup -q -n %{name}-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

./configure --prefix=%{_prefix} \
	--with-ibase=%{_includedir}/firebird --libdir=%{_libdir}/

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
%{__rm} %{buildroot}%{_libdir}/%{name}.la

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%{_libdir}/%{name}.a
%{_libdir}/%{name}.so
%{_libdir}/%{name}-%version.so
%{_includedir}/%{name}-expbuffer.h
%{_includedir}/%{name}-int.h
%{_includedir}/%{name}.h

%changelog
* Wed Oct 19 2022 Devrim Gündüz <devrim@gunduz.org> - 0.4.3-2
- Remove .la file, per
  https://fedoraproject.org/wiki/Changes/RemoveLaFiles

* Mon Feb 21 2022 Devrim Gündüz <devrim@gunduz.org> - 0.4.3-1
- Update to 0.4.3

* Tue Oct 20 2020 Devrim Gündüz <devrim@gunduz.org> - 0.4.2-1
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  firebird_fdw dependency. This is an improved version of the upstream
  spec file.
