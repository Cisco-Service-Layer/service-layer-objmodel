#!/bin/bash

usage="
$(basename "$0") [-h] [-p/--path_to_destination -b/--path_to_binary -v/--version_of_rpm
-n/--name_of_rpm specify,  -x/--xr_release_version, -i/--prod_image_path, -s/--sandbox_rpms_path] 
-- Script Does three things: 
1) Builds rpm from binary (Uses -b -v -n)  
2) Converts rpm into xr-rpm (Uses -v -n -x)
3) Builds Giso with xr-rpm, base imgae(-i), and sandbox rpms(-s)
where:
    -h  show this help text
    -p/--path_to_destination specify the full destination path where you want to store GISO (mandatory argument) 
    -b/--path_to_binary specify the full path to the binary file (mandatory argument) 
    -v/--version_of_rpm specify the version number you want to give the rpm (mandatory argument) 
    -n/--name_of_rpm specify the name you want to give the rpm (mandatory arguement) 
    -x/--xr_release_version specify the release version you want to give (mandatory arguement)
    -i/--prod_image_path specify full path to production image iso usually in /auto/prod_weekly_archive2/bin/ (mandatory argument)
    -s/--sandbox_rpms_path specify full path to folder where your sandbox optional rpms are located
    (usually in /auto/prod_weekly_archive2/bin/<some_image_build>/8000/optional-rpms/sandbox) (mandatory argument)
"

while true; do
  case "$1" in
    -h | --help )        echo "$usage"; exit 0 ;;
    -p | --path_to_destination )   PATH_DEST=$2; shift; shift;;
    -b | --path_to_binary )   PATH_BIN=$2; shift; shift;;
    -v | --version_of_rpm )   VERSION_RPM=$2; shift; shift;;
    -n | --name_of_rpm ) NAME_RPM=$2; shift; shift;;
    -x | --xr_release_version ) XR_VERSION=$2; shift; shift;;
    -i | --prod_image_path ) PROD_IMG_PATH=$2; shift; shift;;
    -s | --sandbox_rpms_path ) SB_RPMS_PATH=$2; shift; shift;;
    -- ) shift; break ;;
    * ) break ;;
  esac
done

if ! [[ $PATH_DEST ]] || ! [[ $PATH_BIN ]] || ! [[ $VERSION_RPM ]] || ! [[ $NAME_RPM ]] || ! [[ $XR_VERSION ]] || ! [[ $PROD_IMG_PATH ]] || ! [[ $SB_RPMS_PATH ]]; then
   echo "Must specify -p/--path_to_destination -b/--path_to_binary  -v/--version_of_rpm 
   -n/--name_of_rpm -x/--xr_release_version -i/--prod_image_path -s/--sandbox_rpms_path, see usage below"
   echo "$usage"
   exit 0
fi 

CURR_DIRECTORY=$(pwd)

cd $PATH_DEST || exit

cd $CURR_DIRECTORY

# Creating a rpmbuild directory structure
mkdir rpmbuild
mkdir rpmbuild/{BUILD,BUILDROOT,SOURCES,SPECS,SRPMS,RPMS,TMPRPMS}
cd rpmbuild || exit


# Creating a dummy rpm spec file
cat << __EOF__ > SPECS/${NAME_RPM}.spec
Summary: This package is a sample for quickly build dummy RPM package.
Name:           $NAME_RPM
Version:        $VERSION_RPM
Release:        1%{?dist}
Summary:        A simple C++ Client for SL-API
BuildArch:      x86_64

License:        GPL
Source0:        %{name}-%{version}.tar.gz

Requires:       bash

%description
A demo RPM build for C++ client


%prep
%setup -q

%install
rm -rf \$RPM_BUILD_ROOT
mkdir -p \$RPM_BUILD_ROOT/%{_bindir}
cp %{name} \$RPM_BUILD_ROOT/%{_bindir}

%clean
rm -rf \$RPM_BUILD_ROOT

%files
%{_bindir}/%{name}
__EOF__

SPEC_FILE=$(find SPECS/ -name "*.spec" -print -quit)
echo $SPEC_FILE

# creating the tar file from given binary
PACKAGE_DIR=$NAME_RPM-$VERSION_RPM
mkdir SOURCES/$PACKAGE_DIR
cp $PATH_BIN SOURCES/$PACKAGE_DIR
cd SOURCES || exit
tar --create --file $PACKAGE_DIR.tar.gz $PACKAGE_DIR
rm -rf $PACKAGE_DIR
cd .. || exit


rpmbuild --define "_topdir $(pwd)" -bb $SPEC_FILE

mv RPMS/*/*.rpm TMPRPMS/

# Calling the script to convert this rpm into a giso image
cd $CURR_DIRECTORY || exit
./create_sandbox_rpm.sh -d $CURR_DIRECTORY/rpmbuild/TMPRPMS/ -n $NAME_RPM -v $VERSION_RPM -r $XR_VERSION

# cp ~/rpm-factory/RPMS/x86_64/* $CURR_DIRECTORY || exit


cd $PATH_DEST || exit
/auto/ioxprojects13/lindt-giso/gisobuild_cisco.sh --iso $PROD_IMG_PATH \
--repo $SB_RPMS_PATH  ~/rpm-factory/RPMS/x86_64/ \
--pkglist xr-sandbox owner --clean --use-container --label sandbox

# Clean Up of rpmbuild directory and rpm-factory
rm -rf ~/rpm-factory 
rm -rf $CURR_DIRECTORY/rpmbuild

