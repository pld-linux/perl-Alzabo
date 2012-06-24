#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	Alzabo
Summary:	Alzabo - a data modelling tool and RDBMS-OO mapper
Summary(pl.UTF-8):	Alzabo - narzędzie do modelowania danych i mapper RDBMS-OO
Name:		perl-Alzabo
Version:	0.92
Release:	1
Epoch:		1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{version}.tar.gz
# Source0-md5:	2f44fbd329a1b05a31e287fb73c5a43f
URL:		http://search.cpan.org/dist/Alzabo/
BuildRequires:	perl-Module-Build
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl-Class-Factory-Util >= 1.3
BuildRequires:	perl-DBI >= 1.25
BuildRequires:	perl-Exception-Class >= 0.97
BuildRequires:	perl-Params-Validate >= 0.58
BuildRequires:	perl-Test-Pod
BuildRequires:	perl-Tie-IxHash
# provided by perl-modules
#BuildRequires:	perl-Storable >= 0.7
#BuildRequires:	perl-Test-Harness >= 1.26
#BuildRequires:	perl-Test-Simple >= 0.47
#BuildRequires:	perl-Time-HiRes
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'perl(DBD::mysql)' 'perl(DBD::Pg)' 'perl(Alzabo::.*)'
# FIXME: is this a proper directory?
%define		alzabo_root_dir	%{_datadir}/alzabo

%description
Alzabo is a two-fold program. Its first function is as a data
modelling tool. Through either a schema creation interface or a custom
Perl program, you can create a set of schema, table, column, etc.
objects that represent your data model. Alzabo is also capable of
reverse engineering an existing data model.

Its second function is as a RDBMS to object mapping system. Once you
have created a schema, you can use the Alzabo::Runtime::Table and
Alzabo::Runtime::Row classes to access its data. These classes offer a
high level interface to common operations such as SQL SELECT, INSERT,
DELETE, and UPDATE commands.

To take it a step further, you could then aggregate a set of rows from
different tables into a larger container object which could understand
the logical relationship between these tables. The Alzabo::MethodMaker
module can be very helpful in this regard.

%description -l pl.UTF-8
Alzabo to program do dwóch rzeczy. Pierwszą funkcją jest narzędzie do
modelowania danych. Poprzez interfejs do tworzenia schematu lub własny
program w Perlu można tworzyć zbiór obiektów schematów, tabel, kolumn
itp. reprezentujących model danych. Alzabo potrafi także wykonywać
reverse engineering istniejącego modelu danych.

Druga funkcja to system mapowania RDBMS na obiekty. Po stworzeniu
schematu można użyć klas Alzabo::Runtime::Table i Alzabo::Runtime::Row
do dostępu do danych. Te klasy oferują wysokopoziomowy interfejs do
takich operacji SQL jak SELECT, INSERT, DELETE czy UPDATE.

Co więcej, można wtedy gromadzić zbiór wierszy z różnych tabel w
większy obiekt kontenerowy, który może rozumieć logiczne relacje
pomiędzy tabelami. Moduł Alzabo::MethodMaker może być w tym bardzo
pomocny.

%prep
%setup -q -n %{pdir}-%{version}

cat >pld_config <<'EOF'
s!"'CONFIG'"!(
	root_dir	=> '%{alzabo_root_dir}/',
	mason_web_dir	=> undef,
	mason_extension	=> undef,
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

# get rid of pod documentation.spec
rm -f $RPM_BUILD_ROOT%{perl_vendorlib}/Alzabo/*.pod
rm -f $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Alzabo/.packlist

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
