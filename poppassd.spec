Summary:	Eudora Poppassd modified to support PAM
Summary(pl):	Zmodyfikowany Poppasswd Eudory z obs³ug± PAM
Name:		poppassd
Version:	1.8.3
Release:	2
License:	BSD ?
Group:		Applications/System
Source0:	http://echelon.pl/pubs/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Source2:	%{name}.pam
Patch0:		%{name}-DESTDIR.patch
URL:		http://echelon.pl/pubs/poppassd.html
BuildRequires:	pam-devel
PreReq:		rc-inetd
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

%description -l pl
Poppassd-ceti to pochodz±cy z Qualcomm demon zmieniaj±cy has³a z
dodan± obs³ug± PAM i kilkoma innymi rozszerzeniami. Program ten ma
udostêpniæ bezpieczny sposób zmiany hase³ poprzez WWW. Szczególnie
unika siê metod, w których programy SUID wywo³uje siê bezpo¶rednio z
serwera WWW. Poppassd ¶ci¶le oddziela interfejs WWW od w³a¶ciwego
manipulowania na has³ach. Program nie zawiera znanych b³êdów
zwi±zanych z bezpieczeñstwem, które mog³yby zostaæ zg³oszone od czasu
udostêpnienia programu kilka lat temu. Ta wersja u¿ywa PAM, co
oznacza, ¿e u¿ywaj±c jej mo¿na zrobiæ wszystko, co mo¿e PAM. Aktualnie
s± dostêpne modu³y PAM do prawie wszystkich znanych metod
uwierzytelnienia.

%prep
%setup -q
%patch0 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig/rc-inetd,pam.d}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi
echo "Warning!"
echo "You have to tune your hosts.allow/deny to deny access from non-localhost!"

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_sbindir}/%{name}
%attr(640,root,root) %config(noreplace) /etc/sysconfig/rc-inetd/poppassd
%attr(640,root,root) %config(noreplace) /etc/pam.d/%{name}
