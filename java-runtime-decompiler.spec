Summary: Application for extraction of bytecode from running JVM and its decompilation back to source code. 
Name: java-runtime-decompiler
Version: 1.1
Release: 1%{?dist}
License: GPL
URL: https://github.com/pmikova/java-runtime-decompiler
Source0: https://github.com/pmikova/%{name}/archive/%{name}-%{version}.tar.gz
Source1: java-runtime-decompiler
Source2: java-runtime-decompiler.1
BuildArch: noarch

BuildRequires: maven-local
BuildRequires: byteman
BuildRequires: rsyntaxtextarea
BuildRequires: java-devel >= 1:1.8.0
BuildRequires: google-gson
Requires: java-devel >= 1:1.8.0
Requires: javapackages-tools
Requires: byteman
Requires: rsyntaxtextarea
Requires: google-gson

%description
This application can access JVM memory at runtime, extract classes and their bytecode from the JVM and decompile them back to the source code. It needs an agent jar and external decompiler for targeted JVM language (e.g. Java).

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

%files -f .mfiles
%dir %{_javadir}/%{name}
%attr(755, root, -) %{_bindir}/java-runtime-decompiler
%{_mandir}/man1/java-runtime-decompiler.1*

# wrappers for decompilers
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/plugins
%config %{_sysconfdir}/%{name}/plugins/FernflowerDecompilerWrapper.java
%config(noreplace) %{_sysconfdir}/%{name}/plugins/FernflowerDecompilerWrapper.json
%config %{_sysconfdir}/%{name}/plugins/ProcyonDecompilerWrapper.java
%config(noreplace) %{_sysconfdir}/%{name}/plugins/ProcyonDecompilerWrapper.json

%files javadoc -f .mfiles-javadoc

%changelog
* Wed Jun 06 2018 Petra Mikova <petra.alice.mikova@gmail.com> 1.0-1
- initial commit
