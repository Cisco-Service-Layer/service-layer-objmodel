#!/bin/bash

# Help                                                     #
############################################################
Help()
{
   # Display Help
   echo "This script packages inner rpms inside another rpm to be installed via Giso to sandbox."
   echo
   echo "Syntax: ./create_sandbox_outer_rpm.sh [-d|h|n|v|r]"
   echo "options:"
   echo "-d     specify directory of inner rpms to be packaged"
   echo "-h     Print this Help."
   echo "-n     specify rpm name (owner- is appended by default)"
   echo "-v     specify rpm version"
   echo "-r     specify XR release version"
   echo
}
############################################################

dflag=false
PKG_NAME=sandbox
PKG_DIR=/tmp/${PKG_NAME}
RPM_ROOT_DIR=~/rpm-factory
RPM_NAME=owner-sandbox

Version="3.14"
Release="7.11.1"


############################################################
# Process the input options.                               #
############################################################
# Get the options
while getopts ":hd:n:v:r:" option; do
   case $option in
      h) # display Help
         Help
         exit;;
      d) # Enter the inner rpm directory
         Dir=$OPTARG; dflag=true;;
      n) # Enter rpm name
         RPM_NAME=owner-$OPTARG;;
      v) # Enter rpm version
         Version=$OPTARG;;
      r) # Enter XR version
         Release=$OPTARG;;
     \?) # Invalid option
         echo "Error: Invalid option, use -h option for help"
         exit;;
   esac
done
############################################################

if ! $dflag
then
    echo "-d <path to rpms> must be specified, use -h option for help" >&2
    exit 1
fi

if [ ! -d $Dir ]
then
   echo "path "$Dir" is not a directory" >&2
   exit 1
fi

rm -rf $RPM_ROOT_DIR
rm -rf $PKG_DIR

# Create below files to be added to rpm:
mkdir -p ${PKG_DIR}
cp $Dir/* ${PKG_DIR}

pushd ${PKG_DIR}/..
tar czvf ${PKG_NAME}.tar.gz ${PKG_NAME}
popd

#PKG_TAR=/tmp/${PKG_NAME}.tar.gz
# Recreate the root directory and its structure if necessary
mkdir -p ${RPM_ROOT_DIR}/{SOURCES,BUILD,RPMS,SPECS,SRPMS,tmp}
pushd  $RPM_ROOT_DIR
cp /tmp/sandbox.tar.gz ${RPM_ROOT_DIR}/SOURCES/

# Creating a rpm spec file
cat << __EOF__ > ${RPM_ROOT_DIR}/SPECS/${PKG_NAME}.spec
Summary: This package is a sample for quickly build dummy RPM package.
Name: $RPM_NAME
Version: $Version
Release: $Release
License: GPL
Packager: $USER
Group: Development/Tools
Source: sandbox.tar.gz
BuildRoot: ${RPM_ROOT_DIR}/tmp/sandbox-%{version}
Provides: /bin/sh
Prefix: /
%description
%{summary}

%global debug_package %{nil}
%prep
%setup -n ${PKG_NAME}
%build

%install
mkdir -p "%{buildroot}/opt/owner/"
cp -r ${PKG_DIR} "%{buildroot}/opt/owner/"

%files
%defattr(-,root,root)
/opt/owner/sandbox

%clean
%if "%{clean}" != ""
  rm -rf %{_topdir}/BUILD/%{name}
  rm -rf %{buildroot}
%endif

%post

%postun
__EOF__

rpmbuild -v -bb --target x86_64 --define "_topdir ${RPM_ROOT_DIR}" SPECS/${PKG_NAME}.spec
popd

