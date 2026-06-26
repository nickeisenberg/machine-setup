set -e

# sudo dnf builddep -y vim is the following
sudo dnf install -y \
	python3.12 \
	python3.12-devel \
	ncurses-devel \
	libX11-devel \
	libXt-devel \
	libXpm-devel \
	make \
	gcc \
	autoconf \
	gettext \
	libselinux-devel \
	perl-devel \
	libacl-devel \
	perl-ExtUtils-Embed \
	libappstream-glib \
	file \
	ruby-devel \
	lua-devel \
	gtk3-devel \
	ruby \
	gpm-devel \
	libSM-devel \
	libICE-devel \
	libcanberra-devel \
	perl-ExtUtils-ParseXS \
	desktop-file-utils


cd ./vim
mkdir -p /opt/data/eisenbnt_la/.local

make distclean

./configure \
	--with-features=huge \
	--with-x \
	--enable-python3interp \
	--enable-fail-if-missing \
	--with-python3-command=$(which python3.12) \
	--with-python3-config-dir=$(python3.12-config --configdir) \
	--prefix="/opt/data/eisenbnt_la/.local"

make -j 16
make install
