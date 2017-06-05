#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	OCaml module to store data using OCaml notation
Summary(pl.UTF-8):	Moduł OCamla do przechowywania danych w notacji OCamla
Name:		ocaml-data-notation
Version:	0.0.11
Release:	3
License:	LGPL v2.1+ with OCaml static compilation exception
Group:		Libraries
Source0:	https://forge.ocamlcore.org/frs/download.php/1310/%{name}-%{version}.tar.gz
# Source0-md5:	0ab9cd196b4a7f22a037ab96a477896f
URL:		https://forge.ocamlcore.org/projects/odn/
BuildRequires:	ocaml >= 3.10.2
BuildRequires:	ocaml-camlp4
BuildRequires:	ocaml-type_conv-devel >= 108.07.01
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		debug_package	%{nil}

%description
odn is an OCaml module to store data using OCaml notation.

This package contains files needed to run bytecode executables using
odn library.

%description -l pl.UTF-8
odn to moduł OCamla do przechowywania danych w notacji OCamla.

Ten pakiet zawiera binaria potrzebne do uruchamiania programów
używających biblioteki odn.

%package devel
Summary:	OCaml module to store data using OCaml notation - development part
Summary(pl.UTF-8):	Moduł OCamla do przechowywania danych w notacji OCamla - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using odn
library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki niezbędne do tworzenia programów używających
biblioteki odn.

%prep
%setup -q

%build
ocaml setup.ml -configure \
	--prefix %{_prefix} \
	--override bytecomp_c_compiler "%{__cc} %{rpmcflags} -fno-defer-pop -D_FILE_OFFSET_BITS=64 -D_REENTRANT -fPIC" \
	--override native_c_compiler "%{__cc} %{rpmcflags} -D_FILE_OFFSET_BITS=64 -D_REENTRANT"

ocaml setup.ml -all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml

export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
ocaml setup.ml -install

# move to dir pld ocamlfind looks
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/odn
mv $RPM_BUILD_ROOT%{_libdir}/ocaml/odn/META $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/odn
cat <<EOF >> $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/odn/META
directory="+odn"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.txt CHANGES.txt COPYING.txt README.txt
%dir %{_libdir}/ocaml/odn
%{_libdir}/ocaml/odn/odn.cma
%{_libdir}/ocaml/odn/pa_noodn.cma
%{_libdir}/ocaml/odn/pa_odn.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/odn/odn.cmxs
%endif
%{_libdir}/ocaml/site-lib/odn

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/odn/ODN.cmi
%{_libdir}/ocaml/odn/ODN.ml
%{_libdir}/ocaml/odn/pa_noodn.cmi
%{_libdir}/ocaml/odn/pa_noodn.ml
%{_libdir}/ocaml/odn/pa_odn.cmi
%{_libdir}/ocaml/odn/pa_odn.ml
%if %{with ocaml_opt}
%{_libdir}/ocaml/odn/ODN.cmx
%{_libdir}/ocaml/odn/odn.a
%{_libdir}/ocaml/odn/odn.cmxa
%endif
