%global modname pyspike
%global srcname PySpike

# Effectively this is commit which was transformed into release on PyPi
%global commit d985f3a8de6ae840c8a127653b3d9affb1a8aa40
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           python-%{modname}
Version:        0.3.0
Release:        1%{?dist}
Summary:        Python library for the numerical analysis of spiketrain similarity

License:        BSD
URL:            https://pypi.python.org/pypi/pyspike
Source0:        https://github.com/mariomulansky/PySpike/archive/%{commit}/%{modname}-%{version}.tar.gz
# https://github.com/mariomulansky/PySpike/pull/18
Patch0:         0001-py3-absolute_import.patch
Patch1:         0002-py3-xrange-range.patch
Patch2:         0003-py3-division.patch
Patch3:         0004-add-metadata-and-testing-under-py3.patch
Patch4:         0005-stop-using-package_data.patch

%description
%{summary}.

PySpike is a Python library for the numerical analysis of spike train
similarity. Its core functionality is the implementation of the bivariate ISI
and SPIKE distance as well as SPIKE-Synchronization. Additionally, it provides
functions to compute multivariate profiles, distance matrices, as well as
averaging and general spike train processing. All computation intensive parts
are implemented in C via cython to reach a competitive performance (factor
100-200 over plain Python).

%package doc
Summary:        Documentation and examples for %{name}
BuildRequires:  python3-sphinx
Requires:       (python-matplotlib or python3-matplotlib)
BuildArch:      noarch

%description doc
Documentation and examples for %{name}.

%package -n python2-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{modname}}
%{?python_provide:%python_provide python2-%{srcname}}
BuildRequires:  python2-devel Cython
%if 0%{?fedora} > 23
BuildRequires:  python2-numpy
Requires:       python2-numpy
%else
BuildRequires:  numpy
Requires:       numpy
%endif

%description -n python2-%{modname}
%{summary}.

PySpike is a Python library for the numerical analysis of spike train
similarity. Its core functionality is the implementation of the bivariate ISI
and SPIKE distance as well as SPIKE-Synchronization. Additionally, it provides
functions to compute multivariate profiles, distance matrices, as well as
averaging and general spike train processing. All computation intensive parts
are implemented in C via cython to reach a competitive performance (factor
100-200 over plain Python).

Python 2 version.

%package -n python3-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{modname}}
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires:  python3-devel python3-Cython
BuildRequires:  python3-numpy
Requires:       python3-numpy

%description -n python3-%{modname}
%{summary}.

PySpike is a Python library for the numerical analysis of spike train
similarity. Its core functionality is the implementation of the bivariate ISI
and SPIKE distance as well as SPIKE-Synchronization. Additionally, it provides
functions to compute multivariate profiles, distance matrices, as well as
averaging and general spike train processing. All computation intensive parts
are implemented in C via cython to reach a competitive performance (factor
100-200 over plain Python).

Python 3 version.

%prep
%autosetup -n %{srcname}-%{commit} -p1
# Remove online images from Readme
sed -i -e "/\.\. image:/,+1d" Readme.rst

%build
%py2_build
%py3_build

pushd doc
  PYTHONPATH=`readlink -f ../build/lib.*-%{python3_version}` sphinx-build-%{python3_version} -b html . _build
  rm -f _build/.buildinfo
popd

%install
%py2_install
%py3_install

%check
PYTHONPATH=%{buildroot}%{python2_sitearch} nosetests-%{python2_version} test/ -v
PYTHONPATH=%{buildroot}%{python3_sitearch} nosetests-%{python3_version} test/ -v

%files doc
%doc doc/_build
%doc examples

%files -n python2-%{modname}
%license License.txt
%doc Changelog Readme.rst
%{python2_sitearch}/%{modname}*

%files -n python3-%{modname}
%license License.txt
%doc Changelog Readme.rst
%{python3_sitearch}/%{modname}*

%changelog
* Sun Dec 13 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.3.0-1
- Initial package
