Summary:	Eudora Poppassd modified to support PAM
Summary(pl):	Zmodyfikowany Poppasswd Eudory ze wsparciem dla PAM
Name:		poppassd
Version:	1.8.2
Release:	1
License:	BSD ?
Group:		Applications/System
Source0:	http://echelon.pl/pubs/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Patch0:		%{name}-DESTDIR.patch
URL:		http://echelon.pl/pubs/poppassd.html
BuildRequires:	pam-devel
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

%prep
%setup -q
%patch0 -p0

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/rc-inetd/

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/rc-inetd/poppassd

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi
echo "Warning!"
echo "You have to tune your hosts.allow/deny to deny access from non-locahost!"

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
fi


%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_sbindir}/%{name}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/rc-inetd/poppassd
