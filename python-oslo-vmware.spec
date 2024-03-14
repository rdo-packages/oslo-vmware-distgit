%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2ef3fe0ec2b075ab7458b5f8b702b20b13df2318
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%global pypi_name oslo.vmware
%global pkg_name oslo-vmware

%global with_doc 1

%global common_desc \
The Oslo project intends to produce a python library containing infrastructure \
code shared by OpenStack projects. The APIs provided by the project should be \
high quality, stable, consistent and generally useful. \
The Oslo VMware library provides support for common VMware operations and APIs.

Name:           python-%{pkg_name}
Version:        4.4.0
Release:        1%{?dist}
Summary:        Oslo VMware library for OpenStack projects

License:        Apache-2.0
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

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  git-core
Requires:  python-%{pkg_name}-lang = %{version}-%{release}

%description -n python3-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:    Documentation for OpenStack common VMware library

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


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini
sed -i '/sphinx-build/ s/-W//' tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
%tox -e docs

# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif


%install
%pyproject_install

# Generate i18n files
python3 setup.py compile_catalog -d %{buildroot}%{python3_sitelib}/oslo_vmware/locale --domain oslo_vmware


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
%tox -e %{default_toxenv}

%files -n python3-%{pkg_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/oslo_vmware
%{python3_sitelib}/*.dist-info
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
* Thu Mar 14 2024 RDO <dev@lists.rdoproject.org> 4.4.0-1
- Update to 4.4.0

