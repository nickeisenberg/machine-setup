On a fresh install of RHEL9, start with the following:

```bash
sudo dnf update -y
sudo reboot
```

On boot, there may be a couple RHEL options to choose at the GRUB menu. Pick
the one with the latest kernal. Again, before continuing. Make sure everything
is updated.

# Nvidia
To install

* The latest nvidia driver
* The cuda-toolkit
* The nvidia container toolkit

follow the readme at ./nvidia-cuda-setup/README.md

# LLMs
To do the following,
 
* pull the openwebui 
* pull vllm container
* pull gemma-3-1b-it from Huggingface
* launch all containers either separately or with podman compose

follow the readme at ./llm-serving/README.md
