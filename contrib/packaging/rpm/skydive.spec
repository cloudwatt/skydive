#debuginfo not supported with Go
%global debug_package %{nil}
%global gopath      %{_datadir}/gocode

# commit or tagversion need to be defined on command line
%if %{defined commit}
%define source %{commit}
%define tag 0.git%{commit}
%endif

%if %{defined tagversion}
%define source %{tagversion}
%endif

%{!?tagversion:%define tagversion 0.6.0}
%{!?source:%define source 0.6.0}
%{!?tag:%define tag 1}

Name:           skydive
Version:        %{tagversion}
Release:        %{tag}%{dist}
Summary:        Real-time network topology and protocols analyzer.
License:        ASL 2.0
URL:            https://github.com/skydive-project/skydive
ExclusiveArch:  x86_64
Source0:        https://github.com/skydive-project/skydive/archive/skydive-%{source}.tar.gz
Requires:       libpcap
BuildRequires:  make
BuildRequires:  golang >= 1.5
BuildRequires:  systemd
BuildRequires:  libpcap-devel

%description
Skydive is an open source real-time network topology and protocols analyzer.
It aims to provide a comprehensive way of what is happening in the network
infrastrure.

Skydive agents collect topology informations and flows and forward them to a
central agent for further analysis. All the informations a stored in an
Elasticsearch database.

Skydive is SDN-agnostic but provides SDN drivers in order to enhance the
topology and flows informations. Currently only the Neutron driver is provided
but more drivers will come soon.

%package analyzer
Summary:          Skydive analyzer
Requires:         %{name} = %{version}-%{release}
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description analyzer
Collects data captured by the Skydive agents.

%package agent
Summary:          Skydive agent
Requires:         %{name} = %{version}-%{release}
Requires:         openvswitch >= %{openvswitch_version}
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description agent
The Skydive agent has to be started on each node where the topology and
flows informations will be captured.

%prep
%setup -q -n skydive-%{source}/src/github.com/skydive-project/skydive

%build
rm -rf %{buildroot}
export GOPATH=%{_builddir}/skydive-%{source}
export PATH=$PATH:$GOPATH/bin
export GO15VENDOREXPERIMENT=1
# compile govendor locally
go install github.com/kardianos/govendor
make install

%install
export GOPATH=%{_builddir}/skydive-%{source}
install -d %{buildroot}%{_bindir}
install -p -m 755 $GOPATH/bin/skydive %{buildroot}%{_bindir}/skydive
for bin in agent analyzer
do
  install -D -m 644 contrib/systemd/skydive-${bin}.service %{buildroot}%{_unitdir}/skydive-${bin}.service
done
install -D -m 644 etc/skydive.yml.default %{buildroot}/%{_sysconfdir}/skydive/skydive.yml

%post agent
%systemd_post %{basename:%{name}-agent.service}

%preun agent
%systemd_preun %{basename:%{name}-agent.service}

%postun agent
%systemd_postun

%post analyzer
%systemd_post %{basename:%{name}-analyzer.service}

%preun analyzer
%systemd_preun %{basename:%{name}-analyzer.service}

%postun analyzer
%systemd_postun

%files
%defattr(-,root,root,-)
%doc README.md LICENSE
%{_bindir}/skydive
%config(noreplace) %{_sysconfdir}/skydive/skydive.yml

%files agent
%defattr(-,root,root,-)
%{_unitdir}/skydive-agent.service

%files analyzer
%defattr(-,root,root,-)
%{_unitdir}/skydive-analyzer.service

%changelog
* Thu Sep 15 2016 Sylvain Baubeau <sbaubeau@redhat.com> - 0.5.0-1
- Gremlin improvements:
  - Allow filtering flows in Gremlin query
  - Add bandwidth calculation
  - New steps: Count, Both
  - New predicates: Lt, Gt, Lte, Gte, Between, Inside, Outside
- Scaling improvements
- Use protobuf instead of JSON for analyzer - agent communications
- Switch Docker image to Ubuntu
- Improved release pipeline (executables, Docker image)

* Thu Aug 4 2016 Sylvain Baubeau <sbaubeau@redhat.com> - 0.4.0-1
- Bump to version 0.4.0

* Fri Jul 29 2016 Nicolas Planel <nplanel@redhat.com> - 0.3.0-2
- Update spec file to use govendor on go version >=1.5

* Wed Apr 27 2016 Sylvain Baubeau <sbaubeau@redhat.com> - 0.3.0-1
- Bump to version 0.3.0

* Fri Mar 25 2016 Sylvain Baubeau <sbaubeau@redhat.com> - 0.2.0-1
- Bump to version 0.2.0

* Mon Feb 1 2016 Sylvain Baubeau <sbaubeau@redhat.com> - 0.1.0-1
- Initial release of RPM
