#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define	pdir	Alzabo
Summary:	Alzabo - A data modelling tool and RDBMS-OO mapper
Summary(pl):	Alzabo - narzêdzie do modelowania danych i mapper RDBMS-OO
Name:		perl-Alzabo
Version:	0.82
Release:	1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{version}.tar.gz
# Source0-md5:	b2de87a8d2a5b7a95f3f2f19abaaffad
BuildRequires:	perl-Module-Build
BuildRequires:	perl-devel >= 1:5.6
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl-Class-Factory-Util >= 1.3
BuildRequires:	perl-DBI >= 1.25
BuildRequires:	perl-Exception-Class >= 0.97
BuildRequires:	perl-Params-Validate >= 0.58
BuildRequires:	perl-Storable >= 0.7
BuildRequires:	perl-Test-Harness >= 1.26
BuildRequires:	perl-Test-Pod
BuildRequires:	perl-Test-Simple >= 0.47
BuildRequires:	perl-Tie-IxHash
BuildRequires:	perl-Time-HiRes
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define _noautoreq	'perl(DBD::mysql)' 'perl(DBD::Pg)'
# FIXME: is this a proper directory?
%define	alzabo_root_dir	%{_datadir}/alzabo

%description
Alzabo is a two-fold program. Its first function is as a data modelling
tool. Through either a schema creation interface or a custom Perl program,
you can create a set of schema, table, column, etc. objects that represent
your data model. Alzabo is also capable of reverse engineering an existing
data model.

Its second function is as a RDBMS to object mapping system. Once you
have created a schema, you can use the Alzabo::Runtime::Table and
Alzabo::Runtime::Row classes to access its data. These classes offer a
high level interface to common operations such as SQL SELECT, INSERT,
DELETE, and UPDATE commands.

To take it a step further, you could then aggregate a set of rows from
different tables into a larger container object which could understand
the logical relationship between these tables.  The Alzabo::MethodMaker
module can be very helpful in this regard.

%description -l pl
Alzabo to program do dwóch rzeczy. Pierwsz± funkcj± jest narzêdzie do
modelowania danych. Poprzez interfejs do tworzenia schematu lub w³asny
program w Perlu mo¿na tworzyæ zbiór obiektów schematów, tabel, kolumn
itp. reprezentuj±cych model danych. Alzabo potrafi tak¿e wykonywaæ
reverse engineering istniej±cego modelu danych.

Druga funkcja to system mapowania RDBMS na obiekty. Po stworzeniu
schematu mo¿na u¿yæ klas Alzabo::Runtime::Table i Alzabo::Runtime::Row
do dostêpu do danych. Te klasy oferuj± wysokopoziomowy interfejs do
takich operacji SQL jak SELECT, INSERT, DELETE czy UPDATE.

Co wiêcej, mo¿na wtedy gromadziæ zbiór wierszy z ró¿nych tabel w
wiêkszy obiekt kontenerowy, który mo¿e rozumieæ logiczne relacje
pomiêdzy tabelami. Modu³ Alzabo::MethodMaker mo¿e byæ w tym bardzo
pomocny.

%prep
%setup -q -n %{pdir}-%{version}

cat >pld_config <<'EOF'
s!"'CONFIG'"!(
    root_dir        => '%{alzabo_root_dir}/',
    mason_web_dir   => undef,
    mason_extension => undef,
)!;
EOF

%build
%{__perl} -pw pld_config < inc/Alzabo/Config.pm.tmpl > lib/Alzabo/Config.pm
%{__perl} Build.PL \
	--dist \
	installdirs=vendor \
	destdir=$RPM_BUILD_ROOT
./Build

%{?with_tests:./Build test}

%install
rm -rf $RPM_BUILD_ROOT

./Build install

install -d $RPM_BUILD_ROOT%{alzabo_root_dir}
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a eg/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes TODO
%{perl_vendorlib}/*.pm
%{perl_vendorlib}/Alzabo
%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}
%{alzabo_root_dir}
