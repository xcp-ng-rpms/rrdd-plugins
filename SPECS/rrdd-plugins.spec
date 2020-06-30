Name:           rrdd-plugins
Version:        1.10.7
Release:        1%{?dist}
Summary:        RRDD metrics plugins
License:        LGPL+linking exception
Group:          System/Hypervisor
URL:            https://github.com/xenserver/rrdd-plugins/

Source0: https://code.citrite.net/rest/archive/latest/projects/XSU/repos/rrdd-plugins/archive?at=v1.10.7&format=tar.gz&prefix=rrdd-plugins-1.10.7#/rrdd-plugins-1.10.7.tar.gz
Source1: SOURCES/rrdd-plugins/xcp-rrdd-iostat.service
Source2: SOURCES/rrdd-plugins/xcp-rrdd-squeezed.service
Source3: SOURCES/rrdd-plugins/xcp-rrdd-xenpm.service


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/rrdd-plugins/archive?at=v1.10.7&format=tar.gz&prefix=rrdd-plugins-1.10.7#/rrdd-plugins-1.10.7.tar.gz) = 17a36d125ab1cb8e9ccb57946e12680c76d5a641

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:  xs-opam-repo
BuildRequires:  forkexecd-devel
BuildRequires:  ocaml-xcp-idl-devel
BuildRequires:  ocaml-rrdd-plugin-devel
BuildRequires:  ocaml-xen-api-libs-transitional-devel
BuildRequires:  xen-ocaml-devel
BuildRequires:  blktap-devel
BuildRequires:  xen-dom0-libs-devel
BuildRequires:  xen-libs-devel
%{?systemd_requires}
BuildRequires: systemd

Requires:       jemalloc
Requires:       xsifstat
Requires:       xsiostat

%description
This package contains plugins registering to the RRD daemon and exposing
various metrics.

%prep
%autosetup -p1

%build
mkdir -p %{buildroot}
DESTDIR=%{buildroot} %{__make}

%install
rm -rf %{buildroot}
DESTDIR=%{buildroot} %{__make} install
%{__install} -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/xcp-rrdd-iostat.service
%{__install} -D -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/xcp-rrdd-squeezed.service
%{__install} -D -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/xcp-rrdd-xenpm.service

%clean
rm -rf %{buildroot}

%post
%systemd_post xcp-rrdd-iostat.service
%systemd_post xcp-rrdd-squeezed.service
%systemd_post xcp-rrdd-xenpm.service

%preun
%systemd_preun xcp-rrdd-iostat.service
%systemd_preun xcp-rrdd-squeezed.service
%systemd_preun xcp-rrdd-xenpm.service

%postun
%systemd_postun xcp-rrdd-iostat.service
%systemd_postun xcp-rrdd-squeezed.service
%systemd_postun xcp-rrdd-xenpm.service

%files
%defattr(-,root,root,-)
/etc/logrotate.d/xcp-rrdd-plugins
/etc/sysconfig/xcp-rrdd-plugins
/opt/xensource/libexec/xcp-rrdd-plugins/xcp-rrdd-iostat
/opt/xensource/libexec/xcp-rrdd-plugins/xcp-rrdd-squeezed
/opt/xensource/libexec/xcp-rrdd-plugins/xcp-rrdd-xenpm
/etc/xensource/bugtool/xcp-rrdd-plugins.xml
/etc/xensource/bugtool/xcp-rrdd-plugins/stuff.xml
%{_unitdir}/xcp-rrdd-iostat.service
%{_unitdir}/xcp-rrdd-squeezed.service
%{_unitdir}/xcp-rrdd-xenpm.service

%changelog
* Fri May 29 2020 Christian Lindig <christian.lindig@citrix.com> - 1.10.7-1
- CA-335964: Do not expose temporary VM UUIDs
- travis: follow validation suggestions

* Tue May 19 2020 Christian Lindig <christian.lindig@citrix.com> - 1.9.7-1
- CA-339269 Average I/O latency in microseconds

* Mon Apr 06 2020 Christian Lindig <christian.lindig@citrix.com> - 1.8.7-1
- CA-336067 take average since last blktap reading

* Tue Jan 28 2020 Christian Lindig <christian.lindig@citrix.com> - 1.7.7-1
- CA-144246 prevent log spam when intellicache enabled
- maintenance: fix compiler warnings
- maintenance: update .travis.yml

* Wed Dec 11 2019 Pau Ruiz Safont <pau.safont@citrix.com> - 1.6.7-3
- Display rrdd-xenpm service as xenpm in logs.

* Fri Aug 23 2019 Edwin Török <edvin.torok@citrix.com> - 1.6.7-2
- bump packages after xs-opam update

* Mon Jul 29 2019 Christian Lindig <christian.lindig@citrix.com> - 1.6.7-1
- XSI-400 Try to stop xcp-rrdd-isostat filling log

* Thu Jan 17 2019 Christian Lindig <christian.lindig@citrix.com> - 1.5.7-1
- Replaced jbuild files with dune.

* Tue Dec 18 2018 Christian Lindig <christian.lindig@citrix.com> - 1.4.7-1
- CA-302328: Ignore extra stat fields with newer kernels
- Reduce compiler warnings
- Update Opam and Travis configuration

* Thu Oct 04 2018 Christian Lindig <christian.lindig@citrix.com> - 1.3.7-1
- CA-297055: Make loop tail recursive

* Tue May 01 2018 Christian Lindig <christian.lindig@citrix.com> - 1.2.7-1
- CA-288281: Cache tapdisk3 pids
- CA-288281: Use mmap/cstruct rather than read to get stats from blktap3

* Thu Mar 15 2018 Christian Lindig <christian.lindig@citrix.com> - 1.1.7-1
- CA-277850 replace xenops with ezxenstore

* Mon Jan 22 2018 Christian Lindig <christian.lindig@citrix.com> - 1.0.7-1
- CP-26596: Ported build from oasis to jbuilder.

* Mon Dec 4 2017 Marcello Seri <marcello.seri@citrix.com> - 1.0.6-1
- Replace old xenstore-compat with ezxenstore

* Thu Aug 3 2017 Marcello Seri <marcello.seri@citrix.com> - 1.0.5-1
- Drop unused dependency

* Wed Apr 26 2017 Christian Lindig <christian.lindig@citrix.com> - 1.0.4-2
- Fix typos in %preun, %postun

* Fri Apr 21 2017 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.0.4-1
- CA-248332: Fix race when new tapdisks appear causing metrics not to be recorded

* Mon Mar 13 2017 Marcello Seri <marcello.seri@citrix.com> - 1.0.3-2
- Update OCaml dependencies and build/install script after xs-opam-repo split

* Wed Oct 19 2016 Euan Harris <euan.harris@citrix.com> - 1.0.3-1
- Remove final vestiges of previous init system

* Mon Aug 22 2016 Rafal Mielniczuk <rafal.mielniczuk@citrix.com> - 1.0.2-2
- Package for systemd

* Tue Aug 16 2016 Christian Lindig <christian.lindig@citrix.com> - 1.0.2-1
- Update to 1.0.2
- Bump version to match new upstream version

* Mon May 16 2016 John Else <john.else@citrix.com> - 1.0.1-3
- Update to 1.0.1
- Bump release to 3 for upgrade against old versions

* Mon May 16 2016 Si Beaumont <simon.beaumont@citrix.com> - 1.0.0-2
- Re-run chkconfig on upgrade
- Stop service on uninstall

* Tue Apr 26 2016 Si Beaumont <simon.beaumont@citrix.com> - 1.0.0-1
- Update to 1.0.0

* Fri Jul 11 2014 John Else <john.else@citrix.com> - 0.1.0-1
- Initial package for planex
