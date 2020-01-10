%global oname jaxb-api
Name:          glassfish-jaxb-api
Version:       2.2.7
Release:       3%{?dist}
Summary:       Java Architecture for XML Binding
Group:         Development/Libraries
License:       CDDL or GPLv2 with exception
URL:           http://jaxb.java.net/
# jaxb api and impl have different version
# svn export https://svn.java.net/svn/jaxb~version2/tags/jaxb-2_2_6/tools/lib/redist/jaxb-api-src.zip

Source0:       http://repo1.maven.org/maven2/javax/xml/bind/%{oname}/%{version}/%{oname}-%{version}-sources.jar
Source1:       http://repo1.maven.org/maven2/javax/xml/bind/%{oname}/%{version}/%{oname}-%{version}.pom

Patch0:        %{name}-2.2.6-osgi-support.patch

BuildRequires: java-devel >= 1:1.6.0
BuildRequires: jpackage-utils

BuildRequires: java-javadoc
BuildRequires: jvnet-parent

BuildRequires: maven-local
BuildRequires: maven-compiler-plugin
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-plugin-bundle
BuildRequires: maven-resources-plugin
BuildRequires: maven-shared-osgi
BuildRequires: maven-surefire-plugin

Requires:      java >= 1:1.6.0
Requires:      jpackage-utils
BuildArch:     noarch

%description
Glassfish - JAXB (JSR 222) API.

%package javadoc
Group:         Documentation
Summary:       Javadoc for %{oname}
Requires:      %{name} = %{version}-%{release} 
Requires:      jpackage-utils

%description javadoc
Glassfish - JAXB (JSR 222) API.

This package contains javadoc for %{name}.

%prep
%setup -T -q -c

# fixing incomplete source directory structure
mkdir -p src/main/java

(
  cd src/main/java
  unzip -qq %{SOURCE0}
  rm -rf META-INF
)

cp -p %{SOURCE1} pom.xml
%patch0 -p0

sed -i 's|<location>${basedir}/offline-javadoc</location>|<location>%{_javadocdir}/java</location>|' pom.xml

%build

mvn-rpmbuild install javadoc:javadoc

%install

mkdir -p %{buildroot}%{_javadir}
install -m 644 target/%{oname}-%{version}.jar %{buildroot}%{_javadir}/%{oname}.jar

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{oname}.pom
%add_maven_depmap JPP-%{oname}.pom %{oname}.jar

mkdir -p %{buildroot}%{_javadocdir}/%{oname}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{oname}

%files
%{_javadir}/%{oname}.jar
%{_mavenpomdir}/JPP-%{oname}.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%{_javadocdir}/%{oname}

%changelog
* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.2.7-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Aug 04 2012 gil cattaneo <puntogil@libero.it> 2.2.7-1
- update to 2.2.7

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 27 2012 gil cattaneo <puntogil@libero.it> 2.2.6-1
- update to 2.2.6
- remove Build/Requires: bea-stax-api

* Tue Jan 24 2012 gil cattaneo <puntogil@libero.it> 2.2.3-2
- revert to 2.2.3 (stable release)
- fix License field

* Fri Jul 22 2011 gil cattaneo <puntogil@libero.it> 2.2.3-1
- initial rpm