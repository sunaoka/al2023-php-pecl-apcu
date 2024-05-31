%global php_name   php

%global pecl_name  apcu

# we don't want -z defs linker flag
%undefine _strict_symbol_defs_build

%global with_zts   0%{!?_without_zts:%{?__zts%{php_name}:1}}
%global ini_name   40-%{pecl_name}.ini

%global have_devel 1

Summary:       APCu - APC User Cache
Name:          %{php_name}%{php_ver}-pecl-%{pecl_name}
Version:       5.1.23
Release:       1%{?dist}.0.1
License:       PHP
Group:         Development/Languages
URL:           http://pecl.php.net/package/%{pecl_name}

Source0:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source1:       %{pecl_name}.ini

BuildRequires: %{php_name}-devel
BuildRequires: php%{?pear_ver}-pear

Requires:      php(zend-abi) = %{expand:%{%{php_name}_zend_api}}
Requires:      php(api) = %{expand:%{%{php_name}_core_api}}

Provides:      %{php_name}-pecl(%{pecl_name}) = %{version}
Provides:      %{php_name}-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:      %{php_name}-%{pecl_name} = %{version}-%{release}
Provides:      %{php_name}-%{pecl_name}%{?isa} = %{version}-%{release}

%description
APC User Caching

%package devel
Summary:       Development files for %{name}
Group:         Development/Languages
BuildArch:     noarch

Requires:      %{php_name}-devel
Requires:      %{name} = %{version}

%description devel
Development files for building against the PECL %{pecl_name} module.

%prep
%setup -qc

%{?_licensedir:sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml}

mv %{pecl_name}-%{version} NTS
cd NTS

# Some packages provide their license in the file 'COPYING'; we expect
# to find it in 'LICENSE'
if [ ! -f LICENSE ] && [ -f COPYING ]
then
  cp COPYING LICENSE
fi

# Perform package-specific operations
cd ..

%if %{with_zts}
# Duplicate sources tree for ZTS build
cp -pr NTS ZTS
%endif

%build
cd NTS
%if 0%{?__phpize%{?php_ver}}
%{expand:%{__phpize%{?php_ver}}}
%else
%{_bindir}/phpize
%endif
%configure \
    --enable-%{pecl_name} \
%if 0%{?__phpconfig%{?php_ver}}
    --with-php-config=%{expand:%{__phpconfig%{?php_ver}}}
%else
    --with-php-config=%{_bindir}/php-config
%endif
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%if 0%{?__ztsphpize%{?php_ver}}
%{expand:%{__ztsphpize%{?php_ver}}}
%else
%{_bindir}/zts-phpize
%endif
%configure \
    --enable-%{pecl_name} \
%if 0%{?__ztsphpconfig%{?php_ver}}
    --with-php-config=%{expand:%{__ztsphpconfig%{?php_ver}}}
%else
    --with-php-config=%{_bindir}/zts-php-config
%endif
make %{?_smp_mflags}
%endif

%install
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{SOURCE1} %{buildroot}%{expand:%{%{php_name}_inidir}}/%{ini_name}

install -D -m 644 package.xml %{buildroot}%{expand:%{pecl%{?pear_ver}_xmldir}}/%{name}.xml

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{expand:%{%{php_name}_ztsinidir}}/%{ini_name}
%endif

# Documentation
cd NTS
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do
    install -Dpm 644 $i %{buildroot}%{expand:%{pecl%{?pear_ver}_docdir}}/%{pecl_name}/$i
done

%check
cd NTS
# minimal load test of NTS extension
%if 0%{?__%{php_name}}
%{expand:%{__%{php_name}}} \
%else
%{_bindir}/php \
%endif
    --no-php-ini \
    --define extension_dir=modules \
    --define extension=%{pecl_name}.so \
    --modules | grep -i '^%{pecl_name}$'

# upstream test suite for NTS extension
NO_INTERACTION=true make test

%if %{with_zts}
cd ../ZTS
# minimal load test of ZTS extension
%if 0%{?__zts%{php_name}}
%{expand:%{__zts%{php_name}}} \
%else
%{_bindir}/zts-php \
%endif
    --no-php-ini \
    --define extension_dir=modules \
    --define extension=%{pecl_name}.so \
    --modules | grep -i '^%{pecl_name}$'

# upstream test suite for ZTS extension
NO_INTERACTION=true make test
%endif

%files
%license NTS/LICENSE
%{expand:%{pecl%{?pear_ver}_xmldir}}/%{name}.xml

%config(noreplace) %{expand:%{%{php_name}_inidir}}/%{ini_name}
%{expand:%{%{php_name}_extdir}}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{expand:%{%{php_name}_ztsinidir}}/%{ini_name}
%{expand:%{%{php_name}_ztsextdir}}/%{pecl_name}.so
%endif

%{_datadir}/doc/pecl%{?pear_ver}/%{pecl_name}

%if 0%{?have_devel}
%files devel
%{_includedir}/%{php_name}/ext/%{pecl_name}
%endif

%changelog
* Fri May 31 2024 SUNAOKA Norifumi <tquirk@amazon.com> - 5.1.23-1
- Update 5.1.23
- Removed panel

* Mon Oct 08 2018 Trinity Quirk <tquirk@amazon.com> - 5.1.12-3
- Removed arch-specific requirement for -devel subpackage

* Mon Oct 08 2018 Trinity Quirk <tquirk@amazon.com> - 5.1.12-2
- Made checks load modules by filename

* Tue Jul 24 2018 Trinity Quirk <tquirk@amazon.com> - 5.1.12-1
- Package created via download from pecl.php.net.
