%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pypi_name oslo.vmware
%global pkg_name oslo-vmware

%global with_doc 1

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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%description
%{common_desc}

%package -n python3-%{pkg_name}
Summary:        Oslo VMware library for OpenStack projects
%{?python_provide:%python_provide python3-%{pkg_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  git-core
# test dependencies
BuildRequires: python3-ddt
BuildRequires: python3-fixtures
BuildRequires: python3-mock
BuildRequires: python3-stestr
BuildRequires: python3-subunit
BuildRequires: python3-testtools
BuildRequires: python3-suds
BuildRequires: python3-oslo-concurrency
BuildRequires: python3-oslo-context
BuildRequires: python3-oslo-utils
BuildRequires: python3-oslo-i18n
BuildRequires: python3-eventlet
BuildRequires: python3-oslo-i18n
BuildRequires: python3-oslo-utils
BuildRequires: python3-requests >= 2.14.2
BuildRequires: python3-suds
BuildRequires: python3-netaddr
# Required to compile translation files
BuildRequires: python3-testscenarios
BuildRequires: python3-babel

BuildRequires: python3-lxml

Requires:  python3-pbr
Requires:  python3-eventlet
Requires:  python3-oslo-concurrency >= 3.26.0
Requires:  python3-oslo-context >= 2.19.2
Requires:  python3-oslo-i18n >= 3.15.3
Requires:  python3-oslo-utils
Requires:  python3-requests
Requires:  python3-stevedore >= 1.20.0
Requires:  python3-suds >= 0.6
Requires:  python3-urllib3
Requires:  python3-netaddr
Requires:  python-%{pkg_name}-lang = %{version}-%{release}

Requires:  python3-lxml
Requires:  python3-yaml >= 3.13

%description -n python3-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:    Documentation for OpenStack common VMware library

BuildRequires: python3-sphinx
BuildRequires: python3-sphinxcontrib-apidoc
BuildRequires: python3-openstackdocstheme

%description -n python-%{pkg_name}-doc
Documentation for OpenStack common VMware library.
%endif

%package -n python3-%{pkg_name}-tests
Summary:    Test subpackage for OpenStack common VMware library

Requires: python3-%{pkg_name} = %{version}-%{release}
Requires: python3-fixtures
Requires: python3-mock
Requires: python3-subunit
Requires: python3-testtools
Requires: python3-suds >= 0.6
Requires: python3-oslo-context
Requires: python3-oslo-utils
Requires: python3-oslo-i18n >= 3.15.3
Requires: python3-testscenarios

%description -n python3-%{pkg_name}-tests
Tests for OpenStack common VMware library.

%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo vmware library

%description -n python-%{pkg_name}-lang
Translation files for Oslo vmware library

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# FIXME(hguemar): we use system lxml from EL8 Appstream
sed -i 's/lxml.*/lxml/' requirements.txt



%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
sphinx-build-3 -b html doc/source doc/build/html

# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

# Generate i18n files
python3 setup.py compile_catalog -d build/lib/oslo_vmware/locale --domain oslo_vmware

%install
%{py3_install}

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python3_sitelib}/oslo_vmware/locale/*/LC_*/oslo_vmware*po
rm -f %{buildroot}%{python3_sitelib}/oslo_vmware/locale/*pot
mv %{buildroot}%{python3_sitelib}/oslo_vmware/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang oslo_vmware --all-name

%check
rm -f ./oslo_vmware/tests/test_hacking.py
export OS_TEST_PATH="./oslo_vmware/tests"
PYTHON=python3 stestr-3 --test-path $OS_TEST_PATH run

%files -n python3-%{pkg_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/oslo_vmware
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/oslo_vmware/tests

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python3-%{pkg_name}-tests
%{python3_sitelib}/oslo_vmware/tests

%files -n python-%{pkg_name}-lang -f oslo_vmware.lang
%license LICENSE

%changelog
