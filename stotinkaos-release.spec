%define debug_package %{nil}
%define product_family StotinkaOS
%define release_name Final
%define base_release_version 6
%define full_release_version 6.6

Name:           stotinkaos-release
Version:        %{base_release_version}
Release:        6%{?dist}.12.2
Summary:        %{product_family} release file
Group:          System Environment/Base
License:        GPLv2
Obsoletes:      rawhide-release redhat-release-as redhat-release-es redhat-release-ws redhat-release-de comps rpmdb-redhat fedora-release redhat-release centos-release oraclelinux-release sl-release
Provides:	redhat-release centos-release
Source0:        centos-release-6-6.tar.gz

%description
%{product_family} release files

%prep
%setup -q -n centos-release-6

%build
echo OK

%install
rm -rf $RPM_BUILD_ROOT

# create /etc
mkdir -p $RPM_BUILD_ROOT/etc

# create /etc/system-release and /etc/redhat/release
echo "%{product_family} release %{full_release_version}%{?beta: %{beta}} (%{release_name})" > $RPM_BUILD_ROOT/etc/centos-release
ln -s centos-release $RPM_BUILD_ROOT/etc/redhat-release
ln -s centos-release $RPM_BUILD_ROOT/etc/system-release

# write cpe to /etc/system/release-cpe
echo "cpe:/o:centos:linux:%{version}:%{?beta:%{beta}}%{!?beta:GA}" > $RPM_BUILD_ROOT/etc/system-release-cpe

# create /etc/issue and /etc/issue.net
cp $RPM_BUILD_ROOT/etc/redhat-release $RPM_BUILD_ROOT/etc/issue
echo "Kernel \r on an \m" >> $RPM_BUILD_ROOT/etc/issue
cp $RPM_BUILD_ROOT/etc/issue $RPM_BUILD_ROOT/etc/issue.net
echo >> $RPM_BUILD_ROOT/etc/issue

# copy yum repos to /etc/yum.repos.d
mkdir -p $RPM_BUILD_ROOT/etc/yum.repos.d
for file in *.repo; do
    install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done

#create infra variable for yum
mkdir -p $RPM_BUILD_ROOT/etc/yum/vars/
install -m 644 infra $RPM_BUILD_ROOT/etc/yum/vars/


# copy GPG keys
mkdir -p -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
for file in RPM-GPG-KEY* ; do
    install -m 644 $file $RPM_BUILD_ROOT/etc/pki/rpm-gpg
done

# set up the dist tag macros
install -d -m 755 $RPM_BUILD_ROOT/etc/rpm
cat >> $RPM_BUILD_ROOT/etc/rpm/macros.dist << EOF
# dist macros.

%%rhel %{base_release_version}
%%centos %{base_release_version}
%%centos_ver %{base_release_version}
%%dist .el%{base_release_version}
%%el%{base_release_version} 1
EOF

mkdir -p ${RPM_BUILD_ROOT}%{_defaultdocdir}
ln -s /usr/share/doc/stotinkaos-release-6 ${RPM_BUILD_ROOT}%{_defaultdocdir}/redhat-release
ln -s /usr/share/doc/stotinkaos-release-6 ${RPM_BUILD_ROOT}%{_defaultdocdir}/centos-release

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc EULA GPL 
%attr(0644,root,root) /etc/redhat-release
%attr(0644,root,root) /etc/centos-release
/etc/system-release
%config(noreplace) %attr(0644,root,root) /etc/yum/vars/infra
%config %attr(0644,root,root) /etc/system-release-cpe
%config(noreplace) %attr(0644,root,root) /etc/issue
%config(noreplace) %attr(0644,root,root) /etc/issue.net
%config %attr(0644,root,root) /etc/yum.repos.d/*
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/*
/etc/rpm/macros.dist
%_defaultdocdir/redhat-release
%_defaultdocdir/centos-release

%changelog
* Sat Jan 31 2015 Ivaylo Kuzev <ivkuzev@gmail.com>
- Adapt to Centos/StotinkaOS 6.6

* Thu Dec  8 2011 Karanbir Singh <kbsingh@centos.org> - 6-2.el6.centos.org.7
- Build for CentOS-6.2

* Wed Aug 31 2011 Karanbir Singh <kbsingh@centos.org> - 6-1.el6.centos.5
- Build for CentOS 6.1

* Sat Jul  2 2011 Karanbir Singh <kbsingh@centos.org> - 6-0.el6.centos.5
- Add in Keys

* Wed Jun 29 2011 Karanbir Singh <kbsingh@centos.org> - 6-0.el6.centos.3
- we need the upstream release dir since other apps and vendors rely on it

* Tue Jun  7 2011 Karanbir Singh <kbsingh@centos.org> - 6-0.el6.centos.2
- Make sure we have a Provides for redhat-release

* Sat Feb 19 2011 Karanbir Singh <kbsingh@centos.org> - 6-0.el6.centos.1
- Adapt to CentOS Linux 6

