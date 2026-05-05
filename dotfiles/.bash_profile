setxkbmap -option ctrl:nocaps

PATH=~/.local/bin:${PATH}

PATH="${PATH}:/usr/local/cuda-12.9/bin"
LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/local/cuda-12.9/lib64"
