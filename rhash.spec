# Copyright 2025 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

%global _lto_cflags %{?_lto_cflags} -ffat-lto-objects

Name: rhash
Epoch: 100
Version: 1.4.4
Release: 1%{?dist}
Summary: Great utility for computing hash sums
License: MIT
URL: https://github.com/rhash/RHash/tags
Source0: %{name}_%{version}.orig.tar.gz
%if 0%{?rhel} == 7
BuildRequires: openssl11-devel
%else
BuildRequires: openssl-devel
%endif
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: gettext
BuildRequires: make
BuildRequires: pkgconfig

%description
RHash is a console utility for calculation and verification of magnet
links and a wide range of hash sums like CRC32, MD4, MD5, SHA1, SHA256,
SHA512, SHA3, AICH, ED2K, Tiger, DC++ TTH, BitTorrent BTIH, GOST R
34.11-94, RIPEMD-160, HAS-160, EDON-R, Whirlpool and Snefru.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
export CFLAGS="%{optflags}"
export LDFLAGS="-g %{?__global_ldflags}"
%if 0%{?rhel} == 7
export CFLAGS="$CFLAGS -I%{_includedir}/openssl11"
export LDFLAGS="$LDFLAGS -L%{_libdir}/openssl11"
%endif
%configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir} \
    --enable-gettext \
    --enable-openssl-runtime \
    --extra-cflags="$CFLAGS" \
    --extra-ldflags="$LDFLAGS"
%make_build \
    build

%install
%make_install \
    install-gmo \
    install-lib-headers \
    install-lib-so-link \
    install-pkg-config
find %{buildroot} -type f -name '*.la' -exec rm -rf {} \;

%if 0%{?suse_version} > 1500 || 0%{?sle_version} > 150000
%package -n librhash1
Summary: LibRHash Shared Library

%description -n librhash1
LibRHash Shared Library.

%package -n rhash-devel
Summary: Development files for librhash
Requires: rhash = %{epoch}:%{version}-%{release}
Requires: librhash1 = %{epoch}:%{version}-%{release}

%description -n rhash-devel
The rhash-devel package contains libraries and header files for
developing applications that use librhash.

%post -n librhash1 -p /sbin/ldconfig
%postun -n librhash1 -p /sbin/ldconfig

%files
%license COPYING
%config(noreplace) %{_sysconfdir}/rhashrc
%{_bindir}/*
%{_datadir}/locale/*/*/*
%{_mandir}/*/*

%files -n librhash1
%{_libdir}/*.so.*

%files -n rhash-devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%endif

%if !(0%{?suse_version} > 1500) && !(0%{?sle_version} > 150000)
%package -n rhash-devel
Summary: Development files for librhash
Requires: rhash = %{epoch}:%{version}-%{release}

%description -n rhash-devel
The rhash-devel package contains libraries and header files for
developing applications that use librhash.

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%config(noreplace) %{_sysconfdir}/rhashrc
%{_bindir}/*
%{_datadir}/locale/*/*/*
%{_libdir}/*.so.*
%{_mandir}/*/*

%files -n rhash-devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%endif

%changelog
