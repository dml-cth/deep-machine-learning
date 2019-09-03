# Instructions for installing Docker on your local machine
When working on the cloud, you should already have a working Docker installation, as long as you set up a compute instance as outlined in the instructions for using Google Cloud. For working on your local machine, you do however need to install Docker as outlined below.

## Developement without your own computer
If you don't have one or don't want to use your local machine, you can use the computers at Chalmers' computer labs.
Unfortunately we lack the priviliges to install Docker on these machines. The solution is to always work via Google Cloud.
Simply keep following the instructions but only follow the ones concerning cloud development.

**Note:** Pay extra attention at [this](https://github.com/JulianoLagana/deep-machine-learning/blob/master/Instructions/03_using_google_cloud.md#5-if-needed-create-a-cpu-only-instance)
section and make sure that you set up both the GPU and CPU version of the Docker image.
Using the much cheaper CPU version will reduce the toll that the extra cloud development will have on your credits.

## Dependencies
For working locally with your CPU:
* Linux / Mac, or Windows 10 Pro host environment (Note: Windows 10 Home is not supported, see workaround below)
* Docker
On Windows, Powershell (but not Powershell ISE!) is advised as a convenient CLI environment:
https://docs.microsoft.com/en-us/powershell/

For working locally with your GPU:
* Linux host environment (Mac / Windows not supported)
* CUDA-enabled GPU with compute capability >= 3.0 (required for CUDA 9, which is used for the course) https://developer.nvidia.com/cuda-gpus
* Proprietary NVIDIA driver (CUDA will not work with open-source alternatives such as Nouveau)
* Docker >= 19.03
* NVIDIA Container Runtime https://nvidia.github.io/nvidia-container-runtime/

## Installing Docker
We advice to install the "Docker Engine - Community" edition since we have verified that it is working fine. Other editions might work just as fine.
The following page provides links to a number of ways of obtaining Docker:
https://docs.docker.com/install/

On the menu on the left-hand-side there are links to installation instructions for different host environments (Windows / Mac / Linux). Some of these links will bring you to Docker Hub, where a Docker Hub account is needed for access.

There are however other ways to download Docker, e.g. by following the link provided in the instructions under the "Releases" section at https://docs.docker.com/install/

If you want to work locally in your GPU-enabled Linux environment, remember to install all dependencies listed above, i.e. not only Docker (>= 19.03), but also NVIDIA drivers & NVIDIA Container Runtime.

### Docker on Windows 10 Pro
Docker Desktop is advised. Follow the installation instructions here: https://docs.docker.com/docker-for-windows/install/

If asked, do not check the option "Use Windows containers instead of Linux containers".

As explained in the instructions, the "Hyper-V" and "Containers" Windows features must be enabled. Docker might ask to do this for you, otherwise go to the Control Panel -> Programs and Features -> Turn Windows features on and off, and enable both features there, after which you will need to reboot.

#### Enable virtualisation
Furthermore, virtualization has to be enabled in BIOS.

See here for how to verify whether virtualization is enabled: https://docs.docker.com/docker-for-windows/troubleshoot/#virtualization-must-be-enabled

If not, this means that you should change a setting in your BIOS, which is accessible during the booting of your computer.
Usually you can enter the BIOS settings by pressing `F2` during boot.
However this might vary between computer manufacturers.

In the BIOS settings, you should look for an option to enable virtualisation.
It will be named something along the lines of VT-x, Intel VT-x, Virtualization Extensions, Intel Virtualization Technology,
and there should be an option to enable it.
Then exit the BIOS menu and let your computer resume booting.

#### Docker on Windows troubleshooting
If you face any issues with your Windows installation of Docker, refer to this page: https://docs.docker.com/docker-for-windows/troubleshoot

### Workaround for Windows 10 Home, or older Windows systems
If you are running any Windows OS other than Windows 10 Pro, there is no fast and convenient way to run Docker. Instead we advise you to following these instructions to setup a Python environment on your local computer using Anaconda: [XX_anaconda_workaround.md](XX_anaconda_workaround.md)

Note however, that you will still need to use Docker when working on the cloud.

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
