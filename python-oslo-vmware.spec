# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pypi_name oslo.vmware
%global pkg_name oslo-vmware
%global common_desc \
The Oslo project intends to produce a python library containing infrastructure \
code shared by OpenStack projects. The APIs provided by the project should be \
high quality, stable, consistent and generally useful. \
The Oslo VMware library provides support for common VMware operations and APIs.

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

%package -n python%{pyver}-%{pkg_name}
Summary:        Oslo VMware library for OpenStack projects
%{?python_provide:%python_provide python%{pyver}-%{pkg_name}}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  git
# test dependencies
BuildRequires: python%{pyver}-ddt
BuildRequires: python%{pyver}-fixtures
BuildRequires: python%{pyver}-mock
BuildRequires: python%{pyver}-mox3
BuildRequires: python%{pyver}-stestr
BuildRequires: python%{pyver}-subunit
BuildRequires: python%{pyver}-testtools
BuildRequires: python%{pyver}-suds
BuildRequires: python%{pyver}-oslo-context
BuildRequires: python%{pyver}-oslo-utils
BuildRequires: python%{pyver}-oslo-i18n
# Required to compile translation files
BuildRequires: python%{pyver}-testscenarios
BuildRequires: python%{pyver}-babel

# Handle python2 exception
%if %{pyver} == 2
BuildRequires: python-lxml
%else
BuildRequires: python%{pyver}-lxml
%endif

Requires:  python%{pyver}-pbr
Requires:  python%{pyver}-eventlet
Requires:  python%{pyver}-oslo-concurrency >= 3.26.0
Requires:  python%{pyver}-oslo-context >= 2.19.2
Requires:  python%{pyver}-oslo-i18n >= 3.15.3
Requires:  python%{pyver}-oslo-utils
Requires:  python%{pyver}-requests
Requires:  python%{pyver}-six
Requires:  python%{pyver}-stevedore >= 1.20.0
Requires:  python%{pyver}-suds >= 0.6
Requires:  python%{pyver}-urllib3
Requires:  python%{pyver}-netaddr
Requires:  python-%{pkg_name}-lang = %{version}-%{release}

# Handle python2 exception
%if %{pyver} == 2
Requires:  python-lxml
Requires:  PyYAML
%else
Requires:  python%{pyver}-lxml
Requires:  python%{pyver}-PyYAML
%endif

%description -n python%{pyver}-%{pkg_name}
%{common_desc}

%package -n python-%{pkg_name}-doc
Summary:    Documentation for OpenStack common VMware library

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-openstackdocstheme
BuildRequires: python%{pyver}-eventlet
BuildRequires: python%{pyver}-oslo-concurrency
BuildRequires: python%{pyver}-oslo-i18n
BuildRequires: python%{pyver}-oslo-utils
BuildRequires: python%{pyver}-requests >= 2.14.2
BuildRequires: python%{pyver}-suds
BuildRequires: python%{pyver}-netaddr


%description -n python-%{pkg_name}-doc
Documentation for OpenStack common VMware library.

%package -n python%{pyver}-%{pkg_name}-tests
Summary:    Test subpackage for OpenStack common VMware library

Requires: python%{pyver}-%{pkg_name} = %{version}-%{release}
Requires: python%{pyver}-fixtures
Requires: python%{pyver}-mock
Requires: python%{pyver}-mox3
Requires: python%{pyver}-subunit
Requires: python%{pyver}-testtools
Requires: python%{pyver}-suds >= 0.6
Requires: python%{pyver}-oslo-context
Requires: python%{pyver}-oslo-utils
Requires: python%{pyver}-oslo-i18n >= 3.15.3
Requires: python%{pyver}-testscenarios

%description -n python%{pyver}-%{pkg_name}-tests
Tests for OpenStack common VMware library.

%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo vmware library

%description -n python-%{pkg_name}-lang
Translation files for Oslo vmware library

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# FIXME(hguemar): requirements blocks 0.20.1 due to lp#1696094
# but eventlet 0.20.1-2 package has backported the fix
sed -i '/eventlet/s/!=0.20.1,//' requirements.txt
# FIXME(hguemar): we use system lxml from EL7
sed -i '/lxml/s/,>=3.4.1//' requirements.txt

%build
%{pyver_build}

# generate html docs
%{pyver_bin} setup.py build_sphinx -b html

# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

# Generate i18n files
%{pyver_bin} setup.py compile_catalog -d build/lib/oslo_vmware/locale

%install
%{pyver_install}

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{pyver_sitelib}/oslo_vmware/locale/*/LC_*/oslo_vmware*po
rm -f %{buildroot}%{pyver_sitelib}/oslo_vmware/locale/*pot
mv %{buildroot}%{pyver_sitelib}/oslo_vmware/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang oslo_vmware --all-name

%check
export OS_TEST_PATH="./oslo_vmware/tests"
stestr-%{pyver} --test-path $OS_TEST_PATH run

%files -n python%{pyver}-%{pkg_name}
%doc README.rst
%license LICENSE
%{pyver_sitelib}/oslo_vmware
%{pyver_sitelib}/*.egg-info
%exclude %{pyver_sitelib}/oslo_vmware/tests

%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE

%files -n python%{pyver}-%{pkg_name}-tests
%{pyver_sitelib}/oslo_vmware/tests

%files -n python-%{pkg_name}-lang -f oslo_vmware.lang
%license LICENSE

%changelog
