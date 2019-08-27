# Instructions for installing Docker on your local machine
When working on the cloud, you should already have a working Docker installation, as long as you set up a compute instance as outlined in the instructions for using Google Cloud. For working on your local machine, you do however need to install Docker as outlined below.

## Dependencies
For working locally with your CPU:
* Linux / Mac, or Windows 10 host environment
* Docker
On Windows, Powershell is advised as a convenient CLI environment:
https://docs.microsoft.com/en-us/powershell/

For working locally with your GPU:
* Linux host environment (Mac / Windows not supported)
* CUDA-enabled GPU with compute capability >= 3.0 (required for CUDA 9, which is used for the course) https://developer.nvidia.com/cuda-gpus
* Proprietary Nvidia driver (CUDA will not work with open-source alternatives such as Nouveau)
* Docker >= 19.03
* NVIDIA Container Runtime https://nvidia.github.io/nvidia-container-runtime/

## Installation
We advice to install the "Docker Engine - Community" edition since we have verified that it is working fine. Other editions might work just as fine.
The following page provides links to a number of ways of obtaining Docker:
https://docs.docker.com/install/

On the menu on the left-hand-side there are links to installation instructions for different host environments (Windows / Mac / Linux). Some of these links will bring you to Docker Hub, where a Docker Hub account is needed for access.

There are however other ways to download Docker, e.g. by following the link provided in the instructions under the "Releases" section at https://docs.docker.com/install/

<!-- Windows 10
Install: https://docs.docker.com/docker-for-windows/install/
Test & get started: https://docs.docker.com/docker-for-windows/
During installation - if asked - do not check the option "Use Windows containers instead of Linux containers"
When using docker for the first time, it might ask you to enable "Hyper-V and Container features", which you will have to do. Here is how to manually enable these features (run as administrator):
https://success.docker.com/article/manually-enable-docker-for-windows-prerequisites

Legacy Windows - will run through Linux VM, introduces performance limitations
https://docs.docker.com/toolbox/toolbox_install_windows/
Do Chalmers lab computers have docker installed?
Final solution: work on cloud with CPU instance -->

## (Linux) Allow your own user to run Docker
On Linux, you need to add your user to the `docker` group before you can use Docker. On the cloud, this already setup for the `dml-host` user.
```
sudo usermod -a -G docker $(whoami)
```
After you have done this, **log out** or reboot is needed to make it effective. When logging back in, verify that you see `docker` listed when running the `groups` command.

## Test Docker Installation
To test your docker installation, make sure that the following commands run without any problems:
```
docker info
docker run hello-world
```
