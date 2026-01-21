On a fresh install of RHEL9, start with the following:

```bash
sudo dnf update -y
sudo reboot
```

On boot, there may be a couple RHEL options to choose at the GRUB menu. Pick
the one with the latest kernal. Again, before continuing. Make sure everything
is updated.

Next to install
* The latest nvidia driver
* The cuda-toolkit
* The nvidia container toolkit
follow the readme at ./nvidia-cuda-setup/README.md
