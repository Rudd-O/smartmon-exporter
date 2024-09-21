%define debug_package %{nil}
%define mybuildnumber %{?build_number}%{?!build_number:1}

Summary:        Export S.M.A.R.T. disk attributes for Prometheus
Name:           smartmon-exporter
Version:        0.1.3
Release:        %{mybuildnumber}%{?dist}
License:        GPL
Group:          System administration tools
Source:         %{name}-%{version}.tar.gz
URL:            https://github.com/Rudd-O/%{name}

BuildArch:      noarch

BuildRequires:  make sed

%if 0%{?fedora} > 29
BuildRequires:  systemd-rpm-macros
%else
%define _unitdir %{_prefix}/lib/systemd/system
%endif

Requires:       smartmontools
Requires:       hdparm
Requires:       bash

%description
This service will make available S.M.A.R.T. data over a standard Prometheus
exporter interface.

%prep
%autosetup

%build
make PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir} SBINDIR=%{_sbindir} UNITDIR=%{_unitdir}

%install
make install DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir} SBINDIR=%{_sbindir} UNITDIR=%{_unitdir}

%files
%defattr(-,root,root)
%attr(0755, root, root) %{_sbindir}/%{name}
%attr(0644, root, root) %{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}

%post
%if 0%{?fedora} > 29
%systemd_post %{name}.service
%else
systemctl --system try-restart %{name}.service || true
%endif

%preun
%if 0%{?fedora} > 29
%systemd_preun %{name}.service
%else
systemctl --system try-restart %{name}.service || true
%endif

%postun
%if 0%{?fedora} > 29
%systemd_postun_with_restart %{name}.service
%else
systemctl --system try-restart %{name}.service || true
%endif

%changelog
* Mon Apr 20 2020 Manuel Amador <rudd-o@rudd-o.com> 0.0.1-1
- First RPM packaging release
