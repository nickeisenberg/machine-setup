arch=x86_64
distro=rhel9

# Enable required RHEL repos
subscription-manager repos --enable=rhel-9-for-$arch-appstream-rpms
subscription-manager repos --enable=rhel-9-for-$arch-baseos-rpms
subscription-manager repos --enable=codeready-builder-for-rhel-9-$arch-rpms

# EPEL (optional but fine)
sudo dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm

# Add NVIDIA CUDA repo
sudo dnf config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/$distro/$arch/cuda-$distro.repo

# IMPORTANT: disable the RHEL nvidia module (prevents modular filtering)
sudo dnf module reset nvidia-driver -y
sudo dnf module disable nvidia-driver -y

# Clean metadata
sudo dnf clean all
sudo dnf makecache

# Install driver + CUDA support
sudo dnf install -y nvidia-driver nvidia-driver-cuda

# Reboot to load kernel module
sudo reboot
