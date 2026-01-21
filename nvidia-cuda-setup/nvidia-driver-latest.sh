arch=x86_64
distro=rhel9

subscription-manager repos --enable=rhel-9-for-$arch-appstream-rpms
subscription-manager repos --enable=rhel-9-for-$arch-baseos-rpms
subscription-manager repos --enable=codeready-builder-for-rhel-9-$arch-rpms

dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm

sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm

sudo dnf config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/$distro/$arch/cuda-$distro.repo

sudo dnf clean expire-cache

sudo dnf module enable nvidia-driver:latest
sudo dnf install nvidia-driver
sudo dnf install nvidia-driver-cuda

