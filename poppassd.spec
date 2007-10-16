Summary:	Eudora Poppassd modified to support PAM
Summary(pl.UTF-8):	Zmodyfikowany Poppasswd Eudory z obsługą PAM
Name:		poppassd
Version:	1.8.5
Release:	2
License:	BSD
Group:		Applications/System
#Source0Download: http://echelon.pl/pubs/poppassd.html
Source0:	http://echelon.pl/pubs/%{name}-%{version}.tar.gz
# Source0-md5:	502caa0c9e39d769040c7295d55a53d6
Source1:	%{name}.inetd
Source2:	%{name}.pam
Patch0:		%{name}-DESTDIR.patch
URL:		http://echelon.pl/pubs/poppassd.html
BuildRequires:	pam-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	rc-inetd
Obsoletes:	poppassd_pam
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Poppassd-ceti is a Qualcomm password changer daemon with PAM support
and several other improvements. This program is intended to be a
secure way to change system passwords via the Web. Methods that
involve calling SUID programs directly from the Web are especially
avoided. Poppassd strictly isolates the Web interface from actual
password manipulations. The program contains no known security bugs
that could be reported since it was released several years ago. This
version uses PAM, which means you can do anything PAM can. Currently,
there are PAM modules for almost all known authentication methods
available.

%description -l pl.UTF-8
Poppassd-ceti to pochodzący z Qualcomm demon zmieniający hasła z
dodaną obsługą PAM i kilkoma innymi rozszerzeniami. Program ten ma
udostępnić bezpieczny sposób zmiany haseł poprzez WWW. Szczególnie
unika się metod, w których programy SUID wywołuje się bezpośrednio z
serwera WWW. Poppassd ściśle oddziela interfejs WWW od właściwego
manipulowania na hasłach. Program nie zawiera znanych błędów
związanych z bezpieczeństwem, które mogłyby zostać zgłoszone od czasu
udostępnienia programu kilka lat temu. Ta wersja używa PAM, co
oznacza, że używając jej można zrobić wszystko, co może PAM. Aktualnie
są dostępne moduły PAM do prawie wszystkich znanych metod
uwierzytelnienia.

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig/rc-inetd,pam.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q rc-inetd reload
echo "You have to tune your /etc/tcpd/hosts.allow and /etc/tcpd/hosts.deny"
echo "to deny access from non-localhost - put there:"
echo "poppassd: http@localhost: allow"
echo "poppassd: ALL: deny"

%postun
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_sbindir}/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/poppassd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/%{name}
