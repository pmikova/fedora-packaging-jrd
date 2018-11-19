Summary: Application for extraction and decompilation of JVM byte code
Name: java-runtime-decompiler
Version: 2.0
Release: 1%{?dist}
License: GPLv3
URL: https://github.com/pmikova/java-runtime-decompiler
Source0: https://github.com/pmikova/%{name}/archive/%{name}-%{version}.tar.gz
Source1: java-runtime-decompiler
Source2: java-runtime-decompiler.1
Source3: jrd.desktop
BuildArch: noarch
BuildRequires: maven-local
BuildRequires: byteman
BuildRequires: rsyntaxtextarea
# depends on devel, not runtime (needs tools.jar)
BuildRequires: java-devel = 1:1.8.0
BuildRequires: google-gson
BuildRequires: desktop-file-utils
Requires: java-devel = 1:1.8.0

%description
This application can access JVM memory at runtime,
extract byte code from the JVM and decompile it.
%package javadoc
Summary: Javadoc for %{name}
Requires: %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}

%build
pushd runtime-decompiler
%pom_remove_dep com.sun:tools
%pom_add_dep com.sun:tools
%pom_remove_plugin :maven-jar-plugin
popd
%mvn_build 

%install
%mvn_install
install -d -m 755 $RPM_BUILD_ROOT%{_mandir}/man1/
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_mandir}/man1/
install -d -m 755 $RPM_BUILD_ROOT%{_bindir}
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/
cp -r %{_builddir}/%{name}-%{name}-%{version}/runtime-decompiler/src/plugins/ $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/

install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor="fedora"                     \
--dir=${RPM_BUILD_ROOT}%{_datadir}/applications %{SOURCE3}

%files -f .mfiles
%attr(755, root, -) %{_bindir}/java-runtime-decompiler
%{_mandir}/man1/java-runtime-decompiler.1*

# wrappers for decompilers
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/plugins
%config %{_sysconfdir}/%{name}/plugins/FernflowerDecompilerWrapper.java
%config(noreplace) %{_sysconfdir}/%{name}/plugins/FernflowerDecompilerWrapper.json
%config %{_sysconfdir}/%{name}/plugins/ProcyonDecompilerWrapper.java
%config(noreplace) %{_sysconfdir}/%{name}/plugins/ProcyonDecompilerWrapper.json
%license LICENSE

%dir %{_datadir}/applications
%{_datadir}/applications/fedora-jrd.desktop

%files javadoc -f .mfiles-javadoc
%license LICENSE

%changelog
* Wed Nov 14 2018 Petra Mikova <petra.alice.mikova@gmail.com> - 2.0-1
- fixed issues listed in review (rhbz#1636019)
- added installation of desktop file

* Wed Jun 06 2018 Petra Mikova <petra.alice.mikova@gmail.com> 1.1-1
- initial commit
