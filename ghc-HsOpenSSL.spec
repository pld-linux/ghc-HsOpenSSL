#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	HsOpenSSL
Summary:	Partial OpenSSL binding for Haskell
Name:		ghc-%{pkgname}
Version:	0.11.4.18
Release:	0.1
License:	- (enter GPL/GPL v2/GPL v3/LGPL/BSD/BSD-like/other license name here)
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/HsOpenSSL
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	486670000d5e3e3425f4dc38152380b0
URL:		http://hackage.haskell.org/package/HsOpenSSL
BuildRequires:	ghc >= 6.12.3
BuildRequires:	openssl-devel
%if %{with prof}
BuildRequires:	ghc-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
HsOpenSSL is an OpenSSL binding for Haskell. It can generate RSA and
DSA keys, read and write PEM files, generate message digests, sign and
verify messages, encrypt and decrypt messages. It has also some
capabilities of creating SSL clients and servers.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.md %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/OpenSSL
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/OpenSSL/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/OpenSSL/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/OpenSSL/DH
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/OpenSSL/DH/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/OpenSSL/DH/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/OpenSSL/EVP
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/OpenSSL/EVP/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/OpenSSL/EVP/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/OpenSSL/SSL
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/OpenSSL/SSL/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/OpenSSL/SSL/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/OpenSSL/X509
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/OpenSSL/X509/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/OpenSSL/X509/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/OpenSSL/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/OpenSSL/DH/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/OpenSSL/EVP/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/OpenSSL/SSL/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/OpenSSL/X509/*.p_hi
%endif
