sudo dnf install -y python3.12 python3.12-devel

#--------------------------------------------------
sudo dnf builddep -y vim

# this installs the following:
#
# make-1:4.3-8.el9.x86_64
# gcc-11.5.0-11.el9.x86_64
# python3-devel-3.9.25-3.el9_7.3.x86_64
# autoconf-2.69-41.el9.noarch
# gettext-0.21-8.el9.x86_64
# ncurses-devel-6.2-12.20210508.el9.x86_64
# libselinux-devel-3.6-3.el9.x86_64
# perl-generators-1.13-1.el9.noarch
# perl-devel-4:5.32.1-481.1.el9_6.x86_64
# libacl-devel-2.3.1-4.el9.x86_64
# perl-ExtUtils-Embed-1.35-481.1.el9_6.noarch
# libX11-devel-1.7.0-11.el9.x86_64
# libappstream-glib-0.7.18-5.el9_4.x86_64
# file-5.39-16.el9.x86_64
# ruby-devel-3.0.7-165.el9_5.x86_64
# lua-devel-5.4.4-4.el9.x86_64
# gtk3-devel-3.24.31-8.el9.x86_64
# ruby-3.0.7-165.el9_5.x86_64
# gpm-devel-1.20.7-29.el9.x86_64
# libSM-devel-1.2.3-10.el9.x86_64
# libICE-devel-1.0.10-8.el9.x86_64
# libXpm-devel-3.5.13-10.el9.x86_64
# libXt-devel-1.2.0-6.el9.x86_64
# libcanberra-devel-0.30-27.el9.x86_64
# perl-ExtUtils-ParseXS-1:3.40-460.el9.noarch
# desktop-file-utils-0.26-6.el9.x86_64
#--------------------------------------------------



mkdir -p ${HOME}/software
git clone https://github.com/vim/vim.git ${HOME}/software/vim

cd ~/software/vim
PREFIX="${HOME}/.local"
./configure \
	--with-features=huge \
	--with-x \
	--enable-python3interp \
	--enable-fail-if-missing \
	--with-python3-command=$(which python3.12) \
	--with-python3-config-dir=$(python3.12-config --configdir) \
	--prefix="${PREFIX}"

make
make install
