%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pypi_name oslo.vmware
%global pkg_name oslo-vmware
%global common_desc \
The Oslo project intends to produce a python library containing infrastructure \
code shared by OpenStack projects. The APIs provided by the project should be \
high quality, stable, consistent and generally useful. \
The Oslo VMware library provides support for common VMware operations and APIs.

%if 0%{?fedora} >= 24
%global with_python3 1
%endif

Name:           python-%{pkg_name}
Version:        XXX
Release:        XXX
Summary:        Oslo VMware library for OpenStack projects

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:      noarch

%description
%{common_desc}

%package -n python2-%{pkg_name}
Summary:        Oslo VMware library for OpenStack projects
%{?python_provide:%python_provide python2-%{pkg_name}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  git
# test dependencies
BuildRequires: python-ddt
BuildRequires: python-fixtures
BuildRequires: python-lxml
BuildRequires: python-mock
BuildRequires: python-mox3
BuildRequires: python-subunit
BuildRequires: python-testrepository
BuildRequires: python-testscenarios
BuildRequires: python-testtools
BuildRequires: python-suds
BuildRequires: python-oslo-utils
BuildRequires: python-oslo-i18n
# Required to compile translation files
BuildRequires: python-babel

Requires:  python-eventlet
Requires:  python-lxml
Requires:  python-netaddr
Requires:  python-oslo-concurrency >= 3.8.0
Requires:  python-oslo-i18n >= 2.1.0
Requires:  python-oslo-utils
Requires:  python-requests
Requires:  python-six
Requires:  python-stevedore >= 1.20.0
Requires:  python-suds >= 0.6
Requires:  python-urllib3
Requires:  PyYAML
Requires:  python-%{pkg_name}-lang = %{version}-%{release}

%description -n python2-%{pkg_name}
%{common_desc}

%package -n python-%{pkg_name}-doc
Summary:    Documentation for OpenStack common VMware library

BuildRequires: python-sphinx
BuildRequires: python-openstackdocstheme
BuildRequires: python-eventlet
BuildRequires: python-netaddr
BuildRequires: python-oslo-concurrency
BuildRequires: python-oslo-i18n
BuildRequires: python-oslo-utils
BuildRequires: python-requests >= 2.3.0
BuildRequires: python-suds


%description -n python-%{pkg_name}-doc
Documentation for OpenStack common VMware library.

%package -n python2-%{pkg_name}-tests
Summary:    Test subpackage for OpenStack common VMware library

Requires: python2-%{pkg_name} = %{version}-%{release}
Requires: python-fixtures
Requires: python-mock
Requires: python-mox3
Requires: python-subunit
Requires: python-testrepository
Requires: python-testscenarios
Requires: python-testtools
Requires: python-suds >= 0.6
Requires: python-oslo-utils
Requires: python-oslo-i18n >= 2.1.0

%description -n python2-%{pkg_name}-tests
Tests for OpenStack common VMware library.

%if 0%{?with_python3}
%package -n python3-%{pkg_name}
Summary:        Oslo VMware library for OpenStack projects
%{?python_provide:%python_provide python3-%{pkg_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
# test dependencies
BuildRequires: python3-ddt
BuildRequires: python3-fixtures
BuildRequires: python3-lxml
BuildRequires: python3-mock
BuildRequires: python3-mox3
BuildRequires: python3-subunit
BuildRequires: python3-testrepository
BuildRequires: python3-testscenarios
BuildRequires: python3-testtools
BuildRequires: python3-coverage
BuildRequires: python3-suds >= 0.6
BuildRequires: python3-oslo-utils
BuildRequires: python3-oslo-i18n

Requires:  python3-eventlet
Requires:  python3-lxml
Requires:  python3-netaddr
Requires:  python3-oslo-concurrency >= 3.8.0
Requires:  python3-oslo-i18n >= 2.1.0
Requires:  python3-oslo-utils
Requires:  python3-requests
Requires:  python3-six
Requires:  python3-stevedore
Requires:  python3-suds >= 0.6
Requires:  python3-urllib3
Requires:  python3-PyYAML
Requires:  python-%{pkg_name}-lang = %{version}-%{release}

%description -n python3-%{pkg_name}
%{common_desc}

The Oslo VMware library offers session and API call management for VMware ESX/VC
server.
%endif

%if 0%{?with_python3}
%package -n python3-%{pkg_name}-tests
Summary:    Test subpackage for OpenStack common VMware library

Requires: python3-%{pkg_name} = %{version}-%{release}
Requires: python3-fixtures
Requires: python3-mock
Requires: python3-mox3
Requires: python3-subunit
Requires: python3-testrepository
Requires: python3-testscenarios
Requires: python3-testtools
Requires: python3-coverage
Requires: python3-suds
Requires: python3-oslo-utils
Requires: python3-oslo-i18n >= 2.1.0

%description -n python3-%{pkg_name}-tests
Tests for OpenStack common VMware library.
%endif

%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo vmware library

%description -n python-%{pkg_name}-lang
Translation files for Oslo vmware library

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

%build
%py2_build

# generate html docs
%{__python2} setup.py build_sphinx -b html

# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

# Generate i18n files
%{__python2} setup.py compile_catalog -d build/lib/oslo_vmware/locale

%if 0%{?with_python3}
%py3_build
%endif

%install
%py2_install

%if 0%{?with_python3}
%py3_install
%endif

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/oslo_vmware/locale/*/LC_*/oslo_vmware*po
rm -f %{buildroot}%{python2_sitelib}/oslo_vmware/locale/*pot
mv %{buildroot}%{python2_sitelib}/oslo_vmware/locale %{buildroot}%{_datadir}/locale
%if 0%{?with_python3}
rm -rf %{buildroot}%{python3_sitelib}/oslo_vmware/locale
%endif

# Find language files
%find_lang oslo_vmware --all-name

%check
%{__python2} setup.py test
%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py test
%endif

%files -n python2-%{pkg_name}
%doc README.rst
%license LICENSE
%{python2_sitelib}/oslo_vmware
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/oslo_vmware/tests

%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE

%files -n python2-%{pkg_name}-tests
%{python2_sitelib}/oslo_vmware/tests

%files -n python-%{pkg_name}-lang -f oslo_vmware.lang
%license LICENSE

%if 0%{?with_python3}
%files -n python3-%{pkg_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/oslo_vmware
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/oslo_vmware/tests
%endif

%if 0%{?with_python3}
%files -n python3-%{pkg_name}-tests
%{python3_sitelib}/oslo_vmware/tests
%endif

%changelog
