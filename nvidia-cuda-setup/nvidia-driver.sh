# See https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/red-hat-enterprise-linux.html
# for more detail.

arch=x86_64
distro=rhel9
driver_version=580-open

subscription-manager repos --enable=rhel-9-for-$arch-appstream-rpms
subscription-manager repos --enable=rhel-9-for-$arch-baseos-rpms
subscription-manager repos --enable=codeready-builder-for-rhel-9-$arch-rpms
sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm
sudo dnf config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/$distro/$arch/cuda-$distro.repo

sudo dnf module enable nvidia-driver:${driver_version}

sudo dnf install nvidia-open

sudo reboot
