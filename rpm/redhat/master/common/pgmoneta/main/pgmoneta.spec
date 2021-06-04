%global sname	pgmoneta

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.0
Release:	1%{dist}
Summary:	Backup / restore for PostgreSQL
License:	BSD
URL:		https://github.com/%{sname}/%{sname}
Source0:	https://github.com/%{sname}/%{sname}/archive/%{version}.tar.gz

BuildRequires:	gcc cmake make python3-docutils
BuildRequires:	libev libev-devel openssl openssl-devel systemd systemd-devel
Requires:	libev openssl systemd gzip postgresql%{pgmajorversion}

%description
pgmoneta is a backup / restore solution for PostgreSQL.

%prep
%setup -q -n %{sname}-%{version}

%build

%{__mkdir} build
cd build
cmake -DCMAKE_BUILD_TYPE=Release .. -DCMAKE_INSTALL_PREFIX=/usr
%{__make}

%install
cd build
%{__make} install DESTDIR=%{buildroot}

%{__mkdir} -p %{buildroot}%{_sysconfdir}/%{sname}
%{__mv} %{buildroot}/usr/etc/%{sname}/%{sname}.conf %{buildroot}%{_sysconfdir}/%{sname}

%files
%license LICENSE
%{_bindir}/%{sname}
%{_bindir}/%{sname}-admin
%{_bindir}/%{sname}-cli
%config %{_sysconfdir}/%{sname}/%{sname}.conf
%{_libdir}/libpgmoneta.so*
%dir %{_docdir}/%{sname}
%{_docdir}/%{sname}/*
%{_mandir}/man1/%{sname}*
%{_mandir}/man5/%{sname}*

%changelog
* Fri May 28 2021 Devrim Gündüz <devrim@gunduz.org> 0.1.0-1
- Initial packaging for PostgreSQL RPM repository. Took spec
  file from upstream.