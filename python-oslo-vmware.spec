%global sname oslo.vmware

Name:           python-oslo-vmware
Version:        0.11.1
Release:        2%{?dist}
Summary:        Oslo VMware library for OpenStack projects

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://pypi.python.org/packages/source/o/%{sname}/%{sname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr

Requires:  python-stevedore
Requires:  python-netaddr
Requires:  python-iso8601
Requires:  python-six
Requires:  python-babel
Requires:  python-suds
Requires:  python-eventlet
Requires:  python-oslo-concurrency
Requires:  python-oslo-i18n
Requires:  python-oslo-utils
Requires:  python-requests
Requires:  PyYAML

%description
The Oslo project intends to produce a python library containing infrastructure
code shared by OpenStack projects. The APIs provided by the project should be
high quality, stable, consistent and generally useful.

The Oslo VMware library offers session and API call management for VMware ESX/VC
server.

%package doc
Summary:    Documentation for OpenStack common VMware library
Group:      Documentation

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx

%description doc
Documentation for OpenStack common VMware library.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__python2} setup.py build

# generate html docs
export PYTHONPATH="$( pwd ):$PYTHONPATH"
%{__python2} setup.py build_sphinx

# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

%files
%license LICENSE
%doc README.rst
%{python2_sitelib}/oslo
%{python2_sitelib}/oslo_vmware
%{python2_sitelib}/*.egg-info
%{python2_sitelib}/*-nspkg.pth

%files doc
%license LICENSE
%doc doc/build/html

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 31 2015 Alan Pevec <apevec@redhat.com> - 0.11.1-1
- Upstream 0.11.1

* Tue Feb 24 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 0.10.0-1
- Upstream 0.10.0

* Sun Sep 21 2014 Alan Pevec <apevec@redhat.com> - 0.6.0-1
- Upstream 0.6.0

* Thu Sep 11 2014 Haïkel Guémar <hguemar@fedoraproject.org> - 0.5.0-1
- Upstream 0.5.0

* Fri Aug 1 2014 Jon Bernard <jobernar@redhat.com> - 0.3-3
- Fix mistake in runtime requirements

* Wed Jul 2 2014 Jon Bernard <jobernar@redhat.com> - 0.3-2
- Update spec file to build successfully on el6

* Wed Jun 25 2014 Jon Bernard <jobernar@redhat.com> - 0.3-1
- Initial package from Alan Pevec <apevec@redhat.com>
  with cleanups by Jon Bernard
