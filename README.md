# Intro

This repo serves as the initial setup of a freshly installed RHEL9 machine.
The core installation scripts are given in the `./nvidia-cuda-setup` and
`./llm-serving` directories. The default `vim` on `RHEL9` is out of date and
the `./vim` has an install script to build the latest `vim` version from
source. This may seem unneccesarry but this machine will be headless, so having
the best possible terminal based editor is extremely important. Please follow
the following exactly. The following is the bare minimum needed for a
successful machine.

# Steps

1. `./start-here`

On a fresh install of RHEL9, start with `./start-here/README.md` On boot, there
may be a couple RHEL options to choose at the GRUB menu. Pick the one with the
latest kernal. Again, before continuing. Make sure everything is updated.

2. `./nvidia-cuda-setup`

To install

* The latest nvidia driver
* The cuda-toolkit
* The nvidia container toolkit

follow the readme at `./nvidia-cuda-setup/README.md`

3. `./llm-serving`

To do the following,
 
* pull the openwebui container
* pull vllm container
* pull ollama container
* pull gemma-3-1b-it from Huggingface
* launch all containers either separately or with podman compose

follow the readme at `./llm-serving/README.md`

4. `./vim`

To install the up to date vim with clipboard support follow the readme 
at `./vim/README.md`

