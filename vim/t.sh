sudo dnf install -y python3.12 python3.12-devel
sudo dnf builddep -y vim

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
