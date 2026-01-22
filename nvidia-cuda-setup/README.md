To install the latest nvidia driver, run `./nvidia-driver.sh`. 

After the reboot, to install the cuda toolkit, run `./cuda-12_9.sh`. This will
download the runfile from nvidia, place it in your current working directory
and run it as well. When the runfile runs, its going to ask you whether or not
you want to continue or abort. Hit continue. Then after that it is going to
have you type the word accept. Type accept. After that there will be
several options. MAKE SURE THAT YOU UNSELECT THE DRIVER OPTION. We do not want
to install this driver. The other options, which include the cuda tool kit are
the ones we want. Then hit install and this will install.  After install you
will need to add these to your bash profile
```
PATH="${PATH}:/usr/local/cuda-12.9/bin"
LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/local/cuda-12.9/lib64"
```

After installing cuda, run `./nvidia-container-toolkit.sh` to install the
nvidia container toolkit.
