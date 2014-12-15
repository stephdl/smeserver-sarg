# $Id: smeserver-sarg.spec,v 1.1 2013/03/03 22:03:08 unnilennium Exp $
# Authority: dungog
# Name: Stephen Noble

Summary: SME server Sarg
%define name smeserver-sarg
Name: %{name}
%define version 2.3.1
%define release 1
Version: %{version}
Release: %{release}%{?dist}
License: Freely distributable
Group: Apache/php/caching
Source: %{name}-%{version}.tar.gz
BuildRoot: /var/tmp/e-smith-buildroot
BuildRequires:  e-smith-devtools
BuildArchitectures: noarch
Requires: smeserver-release >= 9
Requires: sarg >= 2.3
AutoReqProv: no

%changelog
* Fri Sep 18 2009 Stephen Noble <support@dungog.net> 2.2.1-6.sme 
- allow valid userpanel users access [SME 2931]

* Tue Jan 9 2007 Stephen Noble <support@dungog.net>
- add db setting for lastlog correctly
- [2.2.1-4]

* Tue Jan 9 2007 Stephen Noble <support@dungog.net>
- remove duplicate access_log [sme 2217]
- add db setting for lastlog, ie 365 = 1yr
- [2.2.1-3]

* Tue Nov 14 2006 Stephen Noble <support@dungog.net>
- requires sarg >= 2.2
- cosmetic update of /var/www/sarg/index.htm
- [2.2.1-2]

* Tue Oct 17 2006 Stephen Noble <support@dungog.net>
- update to sarg 2.2.1
- removed sarg binary, use seperate sarg rpm + dependancies
- [2.2.1-1]

* Tue Oct 17 2006 Stephen Noble <support@dungog.net>
- add index.html files to avoid confusion and 404 errors
- removed -p option (ip only) now sorts users as well
- [1.4.1-6]

* Sun Oct 15 2006 Stephen Noble <support@dungog.net>
- db setting to use dansguardian instead of squid
- /usr/bin/sarglog [squid|dansguardian]

* Sun Oct 08 2006 Michel Van hees <michel@vanhees.cc>
- Bug fixing in cron script
- Make report by name and by ip

* Mon May 22 2006 Michel Van hees <michel@vanhees.cc>
- Bug fixing

* Tue May 9 2006 Michel Van hees <michel@vanhees.cc>
- Integrate binary

* Sun May 7 2006 Michel Van hees <michel@vanhees.cc>
- Debug cron job

* Mon May 1 2006 Michel Van hees <michel@vanhees.cc>
- start developpement

%description
Sarg templates for SME Server release 7

%prep
%setup

%build
perl createlinks
%{__mkdir_p} root/usr/share/sarg/
%{__mkdir_p} root/etc/sarg/images/
%{__mkdir_p} root/etc/sarg/languages/
%{__mkdir_p} root/etc/sarg/fonts/



#mkdir -p          root/etc/e-smith/db/configuration/defaults/sarg
#echo "service"  > root/etc/e-smith/db/configuration/defaults/sarg/type
#echo "squid"    > root/etc/e-smith/db/configuration/defaults/sarg/logfile
#echo "English"  > root/etc/e-smith/db/configuration/defaults/sarg/language
#echo "bytes"    > root/etc/e-smith/db/configuration/defaults/sarg/values

%install
rm -rf $RPM_BUILD_ROOT
(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
/sbin/e-smith/genfilelist $RPM_BUILD_ROOT \
    --file '/usr/bin/sarglog' 'attr(755,root,root)' \
     > %{name}-%{version}-filelist
echo "%doc " >> %{name}-%{version}-filelist

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%preun
%post
#new installs
#if [ $1 = 1 ] ; then
#  /sbin/e-smith/expand-template /etc/httpd/conf/httpd.conf
#  /etc/rc.d/init.d/httpd-e-smith sigusr1
#  /etc/e-smith/events/actions/navigation-conf > /dev/null 2>&1
#fi

#/sbin/e-smith/expand-template /etc/sarg/sarg.conf
#/sbin/e-smith/expand-template /etc/cron.daily/sarg
#/sbin/e-smith/expand-template /etc/cron.weekly/sarg
#/sbin/e-smith/expand-template /etc/cron.monthly/sarg


#/etc/e-smith/events/actions/initialize-default-databases

echo ''
echo 'optional settings for sarg, first option is default'
echo ''
#echo 'config setprop sarg language [English|Dutch|French|German|Spanish|Italian|...]'
echo 'config setprop sarg values [bytes|abbreviation]'
echo 'config setprop sarg logfile [squid|dansguardian]'
echo 'config setprop sarg lastlog [0|365|num.of.days.to.keep.logs]'
echo ''
echo 'expand-templates shortcut with /usr/bin/sarglog or signal-event sarg-update'
echo ''
echo "useage"
echo "sarglog (squid|dansguardian)"

%postun
#uninstalls
if [ $1 = 0 ] ; then
  DBS=`find /home/e-smith/db/navigation -type f -name "navigation.*"`
  for db in $DBS ; do
    /sbin/e-smith/db $db delete sarg 2>/dev/null
  done

  /sbin/e-smith/expand-template /etc/httpd/conf/httpd.conf
  /etc/rc.d/init.d/httpd-e-smith sigusr1
fi

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
