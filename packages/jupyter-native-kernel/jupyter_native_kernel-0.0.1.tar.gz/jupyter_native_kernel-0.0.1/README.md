# Minimal Native kernel for Jupyter

The goal of this kernel is to provide a unified frontend for working with native languages from jupyter.

It was started from the [jupyter C kernel][jupyter-c-kernel].

   [jupyter-c-kernel]: https://github.com/brendan-rius/jupyter-c-kernel

## Usage:
* %load <local file or URL> to load a file to the cell
   
```
//%load https://passlab.github.io/CSCE569/resources/axpy.c
//%compiler: gcc
//%cflags: -fopenmp
//%ldflags: -lm
//%args: 1024

```

## Setup

Works only on Linux and OS X.
Windows is not supported yet.
If you want to use this project on Windows, please use Docker.

Make sure you have the following requirements installed:

  * gcc
  * jupyter
  * python 3
  * pip


### Install (system)

This installs the kernel at the system level. (Not tested yet.)

 1. `git clone <this repo>`
 1. `sudo pip3 install -e jupyter-native-kernel`
 1. `sudo install_native_kernel`
 
 To install on system folder, do `sudo install_native_kernel --sys-prefix`



### Install (virtualenv)

This installs the kernel within the current virtualenv.

 1. `git clone <this repo>`
 1. `virtualenv -p python3 venv`
 1. `source venv/bin/activate`
 1. `pip3 install -e jupyter-native-kernel`
 1. `install_native_kernel --user`


## License

This project is released under the [MIT License](LICENSE.txt).
