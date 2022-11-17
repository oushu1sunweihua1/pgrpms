#!/usr/bin/env bash

# postgresql spec expect this version number, hard code here
PG_MAJOR_NUMBER=14
PG_MINOR_NUMBER=5
PG_VERSION=${PG_MAJOR_NUMBER}.${PG_MINOR_NUMBER}

DEPENDENCY_PATH=/root/dependency
SRC_PATH=/root/postgres/postgres
PDF_PATH=/root/postgres/postgresql-${PG_MAJOR_NUMBER}-A4.pdf
PGRPMS_PATH=/root/postgres/pgrpms
TARGET_PATH=/root/postgres/target
BUILD_PATH=${PGRPMS_PATH}/rpm/redhat/$PG_MAJOR_NUMBER/postgresql-$PG_MAJOR_NUMBER/EL-9

DEPENDENCY=${DEPENDENCY_PATH}/postgresql-dependency.tar.xz
DEPENDENCY_DIR=/opt/postgresql-dependency

tar xvf "$DEPENDENCY" -C /opt || exit 1

cd "$BUILD_PATH"

# prepare postgresql source
ln -s "$SRC_PATH" postgresql-${PG_VERSION}
ln -s "$PDF_PATH" .
tar chjf postgresql-${PG_VERSION}.tar.bz2 postgresql-${PG_VERSION} || exit 1

# prepare environment variables
export DEPATH=$DEPENDENCY_DIR
export CFLAGS="-I${DEPATH}/include"
export CXXFLAGS="$CFLAGS"
export CPPFLAGS="$CFLAGS"
export LDFLAGS="-L${DEPATH}/lib"
export LD_LIBRARY_PATH="${DEPATH}/lib"
export PKG_CONFIG_PATH="${DEPATH}/lib/pkgconfig"
export PATH="${DEPATH}/bin":$PATH

# call build command
make build14 || exit 1

mv /root/rpm14/RPMS/x86_64/*.rpm || exit 1
