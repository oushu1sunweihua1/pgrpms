#version=RHEL7

##########################################################################
#    Kickstart file for CentOS PostgreSQL Spin, with PGDG packages.	 #
#            Devrim GUNDUZ <devrim@gunduz.org>				 #
#									 #
##########################################################################

#platform=x86, AMD64, or Intel EM64T
# Network information
network  --bootproto=dhcp --device=eth0 --onboot=on
# Root password
rootpw --iscrypted $1$1QGU.fEd$ZVmp27WLFAyAGjpBZ4JNk0
# System authorization information
auth  --useshadow  --enablemd5
# Use graphical install
graphical
# Firewall configuration
firewall --disabled
firstboot --disable
# System keyboard
keyboard us
# System language
lang en_US.UTF-8
# SELinux configuration
selinux --disabled
# Install OS instead of upgrade
install
# Use CDROM installation media
cdrom
# System timezone
timezone  America/New_York
# X Window System configuration information
xconfig  --defaultdesktop=GNOME --startxonboot 
# System bootloader configuration
bootloader --location=mbr
# Partition clearing information
clearpart --all  
part / --size 4096

# List of repositories.

# These are the public repositories
repo --name=a-base    --baseurl=http://mirror.centos.org/centos/7/os/$basearch/
repo --name=a-updates --baseurl=http://mirror.centos.org/centos/7/updates/$basearch/
repo --name=a-extras  --baseurl=http://mirror.centos.org/centos/7/extras/$basearch/
repo --name=a-live    --baseurl=http://www.nanotechnologies.qc.ca/propos/linux/centos-live/$basearch/live
repo --name=a-epel    --baseurl=http://download.fedoraproject.org/pub/epel/7/$basearch

# PGDG RPM Repository
repo --name=pgdg95  --baseurl=https://download.postgresql.org/pub/repos/yum/9.5/redhat/rhel-7-x86_64

%packages
@base
@core
@Desktop
kernel
@base
#@sql-server
check_postgres
esc
evolution
evolution-webcal
firefox
httpd
ip4r95
boxinfo
check_postgres
pagila95
phpPgAdmin
pgadmin3_95
pgbouncer
pgdg-centos95
pgbadger
plr95
postgis2_95
postgis2_95-utils
postgresql95
postgresql95-docs
postgresql95-contrib
#postgresql95-jdbc
postgresql95-odbc
postgresql95-plperl
postgresql95-plpython
postgresql95-pltcl
postgresql95-server
postgresql95-test
pyliblzma
python-psycopg2
# Exclude postgresql RPMs from CentOS repo.
-postgresql
-postgresql-docs
-postgresql-contrib
-postgresql-jdbc
-postgresql-odbc
-postgresql-server
-postgresql-test

# Save some space
-a2ps
-alacarte
-at-spi
-cadaver
-ekiga
-esc
-evolution-help
-festival
-fetchmail
-firstboot
-foomatic
-gnome-bluetooth
-gnome-vfs2-smb
-gstreamer-plugins-base 
-gstreamer-plugins-good
-gstreamer
-gucharmap
-hpijs
-hplip
-isdn4k-utils
-mpage
-mtr
-mutt
-nautilus-sendto
-orca
-redhat-lsb
-rsh
-samba-client
-sane-backends
-sendmail
-slrn
-sox
-system-config-printer 
-system-config-printer-libs
-vino
-xsane
-xsane-gimp
-zenity
# smartcards won't really work on the livecd.
-coolkey
# duplicate functionality
-pinfo
-vorbis-tools
# lose the compat stuff
-compat*
# livecd bits to set up the livecd and be able to install
anaconda
rootfiles
authconfig
xkeyboard-config
chkconfig
syslinux
bash
passwd
policycoreutils

# Need to prevent conflicts
-rhdb-utils

# make sure debuginfo doesn't end up on the live image
-*debuginfo
%end

%post
cat > /etc/rc.d/init.d/centos-live << EOF
#!/bin/bash
#
# live: Init script for live image
#
# chkconfig: 345 00 99
# description: Init script for live image.

. /etc/init.d/functions

if ! strstr "\`cat /proc/cmdline\`" liveimg || [ "\$1" != "start" ] || [ -e /.liveimg-configured ] ; then
    exit 0
fi

exists() {
    which \$1 >/dev/null 2>&1 || return
    \$*
}

touch /.liveimg-configured

# mount live image
if [ -b /dev/live ]; then
   mkdir -p /mnt/live
   mount -o ro /dev/live /mnt/live
fi

# read some variables out of /proc/cmdline
for o in \`cat /proc/cmdline\` ; do
    case \$o in
    ks=*)
        ks="\${o#ks=}"
        ;;
    xdriver=*)
        xdriver="--set-driver=\${o#xdriver=}"
        ;;
    esac
done


# if liveinst or textinst is given, start anaconda
if strstr "\`cat /proc/cmdline\`" liveinst ; then
   /usr/sbin/liveinst \$ks
fi
if strstr "\`cat /proc/cmdline\`" textinst ; then
   /usr/sbin/liveinst --text \$ks
fi

# enable swaps unless requested otherwise
swaps=\`blkid -t TYPE=swap -o device\`
if ! strstr "\`cat /proc/cmdline\`" noswap -a [ -n "\$swaps" ] ; then
  for s in \$swaps ; do
    action "Enabling swap partition \$s" swapon \$s
  done
fi

# configure X, allowing user to override xdriver
if [ -n "\$xdriver" ]; then
   exists system-config-display --noui --reconfig --set-depth=24 \$xdriver
fi

# add set no password for postgres user. It is already created with postgresql95-server RPM.
passwd -d postgres > /dev/null

# turn off firstboot for livecd boots
echo "RUN_FIRSTBOOT=NO" > /etc/sysconfig/firstboot

# don't start yum-updatesd for livecd boots
chkconfig --level 345 yum-updatesd off 2>/dev/null

# don't do packagekit checking by default
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults -s -t string /apps/gnome-packagekit/frequency_get_updates never >/dev/null
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults -s -t string /apps/gnome-packagekit/frequency_refresh_cache never >/dev/null
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults -s -t bool /apps/gnome-packagekit/notify_available false >/dev/null

# apparently, the gconf keys aren't enough
mkdir -p /var/lib/pgsql/.config/autostart
echo "X-GNOME-Autostart-enabled=false" >> /var/lib/pgsql/.config/autostart/gpk-update-icon.desktop
chown -R postgres:postgres /var/lib/pgsql/.config


# don't start cron/at as they tend to spawn things which are
# disk intensive that are painful on a live image
chkconfig --level 345 crond off 2>/dev/null
chkconfig --level 345 atd off 2>/dev/null
chkconfig --level 345 anacron off 2>/dev/null
chkconfig --level 345 readahead_early off 2>/dev/null
chkconfig --level 345 readahead_later off 2>/dev/null

# Disable cups,rpcbind and sshd for this spin
chkconfig cups off 2>/dev/null
chkconfig sshd off 2>/dev/null
chkconfig rpcbind off 2>/dev/null

# Enable NetworkManager for this spin
chkconfig NetworkManager on

# Start PostgreSQL and Apache for this spin.
# We need Apache for phpPgAdmin
chkconfig postgresql-9.4 on 2>/dev/null
chkconfig httpd on 2>/dev/null
service httpd start
# PostgreSQL needs some additional interest on it
# Let's run our initdb. RPM runs initdb's with --auth='ident sameuser', 
# but we don't need/want it in the live CD.
su -l postgres -c "/usr/pgsql-9.4/bin/initdb -D /var/lib/pgsql/9.4/data"
service postgresql-9.4 start

# Create pagila database and load pagila data into it:
su -l postgres -c "createdb pagila"
su -l postgres -c "psql pagila -f /usr/share/pagila95/pagila-schema.sql"
su -l postgres -c "psql pagila -f /usr/share/pagila95/pagila-data.sql"

# Stopgap fix for RH #217966; should be fixed in HAL instead
touch /media/.hal-mtab

# workaround clock syncing on shutdown that we don't want (#297421)
sed -i -e 's/hwclock/no-such-hwclock/g' /etc/rc.d/init.d/halt

#Create Desktop directory for postgres user:
su -l postgres -c "mkdir /var/lib/pgsql/Desktop"

EOF

# workaround avahi segfault (#279301)
touch /etc/resolv.conf
/sbin/restorecon /etc/resolv.conf

chmod 755 /etc/rc.d/init.d/centos-live
/sbin/restorecon /etc/rc.d/init.d/centos-live
/sbin/chkconfig --add centos-live

# save a little bit of space at least...
rm -f /boot/initrd*
# make sure there aren't core files lying around
rm -f /core*

# disable screensaver locking
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults -s -t bool /apps/gnome-screensaver/lock_enabled false >/dev/null
# set up timed auto-login with no delay. 
cat >> /etc/gdm/custom.conf << EOF
[daemon]
TimedLoginEnable=true
TimedLogin=postgres
TimedLoginDelay=0
EOF

# Create Desktop directory
mkdir /var/lib/pgsql/Desktop

# Create a desktop conf file for psql
cat > /var/lib/pgsql/Desktop/psql <<EOF

[Desktop Entry]
Encoding=UTF-8
Version=1.0
Type=Application
Terminal=true
Name[en_US]=Command-line interface to PostgreSQL
Exec=/usr/bin/psql postgres -U postgres
Comment[en_US]=Command-line interface to PostgreSQL
Name=psql
Comment=Command-line interface to PostgreSQL
Icon=utilities-terminal
EOF

# Create a desktop conf file for pgadmin3
cat > /var/lib/pgsql/Desktop/pgadmin3 <<EOF

#!/usr/bin/env xdg-open

[Desktop Entry]
Encoding=UTF-8
Name=pgAdmin III
Exec=/usr/bin/pgadmin3
Icon=/usr/share/pgadmin3_95/pgadmin3_95.xpm
Type=Application
Categories=Application;Development;
MimeType=text/html;
DocPath=/usr/share/pgadmin3/docs/en_US/index.html
Comment=PostgreSQL Tools
X-Desktop-File-Install-Version=0.15
EOF

# Create a conf file for pgadmin3. 
cat > /var/lib/pgsql/.pgadmin3 << EOF
ShowTipOfTheDay=false
[Updates]
pgsql-Versions=9.4
[Servers]
Count=1
[Servers/1]
Server=localhost
Description=postgresql-livecd
ServiceID=
Port=5432
StorePwd=true
Restore=true
Database=postgres
Username=postgres
LastDatabase=
LastSchema=
DbRestriction=
SSL=-1
[Properties]
[Properties/Server]
Left=238
Top=160
[frmMain]
Perspective-6930=layout2|name=objectBrowser;caption=Object browser;state=16779560;dir=4;layer=1;row=0;pos=0;prop=100000;bestw=200;besth=450;minw=100;minh=200;maxw=-1;maxh=-1;floatx=236;floaty=222;floatw=-1;floath=-1|name=listViews;caption=Info pane;state=1020;dir=5;layer=0;row=0;pos=0;prop=100000;bestw=400;besth=200;minw=200;minh=100;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1|name=sqlPane;caption=SQL pane;state=16779560;dir=3;layer=0;row=0;pos=0;prop=100000;bestw=400;besth=200;minw=200;minh=100;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1|name=toolBar;caption=Tool bar;state=16788208;dir=1;layer=10;row=0;pos=0;prop=100000;bestw=525;besth=44;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1|dock_size(5,0,0)=202|dock_size(3,0,0)=228|dock_size(1,10,0)=46|dock_size(4,1,0)=233|
[frmQuery]
MaxRows=100
MaxColSize=256
ExplainVerbose=false
ExplainAnalyze=false
Font=monospace 12
[Export]
Unicode=false
QuoteChar="\""
ColSeparator=;
RowSeparator=LF
Quote=Strings
[Copy]
QuoteChar="\""
ColSeparator=;
Quote=Strings
EOF

chown postgres: /var/lib/pgsql/.pgadmin3

%end

%post --nochroot
cp $INSTALL_ROOT/usr/share/doc/*-release-*/GPL $LIVE_ROOT/GPL
cp $INSTALL_ROOT/usr/share/doc/HTML/readme-live-image/en_US/readme-live-image-en_US.txt $LIVE_ROOT/README

# only works on x86, x86_64
if [ "$(uname -i)" = "i386" -o "$(uname -i)" = "x86_64" ]; then
  if [ ! -d $LIVE_ROOT/LiveOS ]; then mkdir -p $LIVE_ROOT/LiveOS ; fi
  cp /usr/bin/livecd-iso-to-disk $LIVE_ROOT/LiveOS
fi
%end

