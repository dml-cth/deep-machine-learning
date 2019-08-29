# Instructions for using Docker, and getting started with the course Docker environment

## Why use Docker?
The main reason we are using Docker in this course is for scalability and predictability. When all of you are working in the same Docker environment, we expect to eliminate most of the issues related to your unique computer environments, that may otherwise have needed (sometimes urgent) attention from our side.

You are by no means prohibited to set up and work in another environment, but in this case we cannot promise any guidance, should issues arise.

## What is Docker?
Docker is the industry-standard software used for *containerization*, i.e. running applications inside of so called "containers". The easiest way to grasp what a container is, is to relate it to virtual machines.

There are many similarities between a container and a virtual machine:
- They both provide a way to seemingly run software inside of a virtual guest operating system
- The guest environment is completely isolated from the host environment

But there are also some differences:
- Virtual machines suffer from degraded performance, while containers are essentially just as fast as running software on the host.
- A virtual machine is a virtual emulation of a physical computer, on which a guest OS is installed. The virtual machine runs as a single process on the host. On the contrary, containers are not emulated. Containerized processes are run as actual processes on the host, but all their resources are isolated from the host.
- A virtual machine needs to boot up before processes you can run processes inside of it. A containerized process can be started

### Docker glossary
- **Docker image:** A package with all the dependencies and information needed to create a container. An image includes all the dependencies (such as frameworks) plus deployment and execution configuration to be used by a container runtime.
- **Docker container:** An instance of a Docker image. A container represents the execution of a single application, process, or service.

## Install Docker
If you haven't already, install Docker as explained in [00_installing_docker.md](00_installing_docker.md), before proceeding.

## Clone course git repository
The course git repository is used to distribute all the assignments.

Now clone the course git repository into a local repository. If you have git installed you could use that, but otherwise, you can make use of the course Docker image, which has git installed inside of it.

Cloning with Docker on Windows:
```
docker run -v %cd%:/workspace ssy340dml/dml-image:gpu git clone https://github.com/JulianoLagana/deep-machine-learning.git
```
Cloning with Docker on Mac / Linux:
```
docker run -e HOST_USER_ID=$(id -u) -e HOST_GROUP_ID=$(id -g) -v "$PWD":/workspace ssy340dml/dml-image:gpu git clone https://github.com/JulianoLagana/deep-machine-learning.git
```
If you receive the error `docker: invalid reference format`, see the note below.

`cd` into the local repository:
```
cd deep-machine-learning
```

When you are inside of it you can run git commands like `git status`, `git pull` etc. You do not need to know git for the purpose of this course, but it might be useful to you.
Here is a small [cheat sheet](https://github.github.com/training-kit/downloads/github-git-cheat-sheet.pdf) to get you started.

**DO NOT FORK THIS REPOSITORY**\
You might be tempted to use git for syncing your work within your groups or between your local computer and the cloud. This is fine as long as you know what you are doing, but you are under no circumstances allowed to make your assignments publicly available. Be aware that GitHub forks of public repositories (such as this one) will always be public.

## Running Docker
A Docker container is completely isolated from its host environment, without any access to or knowledge about it, unless explicitly provided. As you probably noticed when cloning the repository above, `docker run` commands tend to get quite long. This is because of a number of arguments, with the purpose of providing access to the container for whatever resources it may need on the host.

We will now illustrate the usage of `docker run` commands, and walk through the most important arguments, starting with some simple commands.

First, pull (download) the course Docker image:
```
docker pull ssy340dml/dml-image:gpu
```

Note: the previous `git clone` command needed the image so it was already downloaded behind the scenes.

Run the `pwd` command inside the container:
```
docker run ssy340dml/dml-image:gpu pwd
```
You will see `/workspace` printed out. This is the default path where all processes will start, as configured in the course Docker image.

Run the `ls -l` command to list the contents of `/workspace` (it should be empty).
```
docker run ssy340dml/dml-image:gpu ls -l
```

Run the `ls -l` command once again, but now mounting (mapping) your current directory on the host (`%cd%` or `"$PWD"`), to the `/workspace` directory inside the container. You should now see the contents of the current directory instead.\
Windows:
```
docker run -v %cd%:/workspace ssy340dml/dml-image:gpu ls -l
```
Mac / Linux:
```
docker run -v "$PWD":/workspace ssy340dml/dml-image:gpu ls -l
```
**Note:** On some systems there is a (really annoying) issue with mounting a host directory, if the path to it contains any spaces. If you receive the error `docker: invalid reference format`, you might be suffering from this. The only workaround we know of, is to move to a path without spaces, and do all your work from there. The issue is mentioned [here](https://www.reddit.com/r/docker/comments/3p3in6/how_do_you_mount_host_directories_with_spaces_in/) as well.

Next, read through the list of arguments below, and make sure you understand their behavior and purpose.
- `-it` (always use if unsure)\
    This argument (the `-i` and `-t` arguments combined) lets you interact with the container while its process is running. Your keyboard strokes will only be received by the process if this argument is proved. If no input to the process is required, this argument is actually redundant (i.e. for `cd`, `ls`, `pwd` commands etc.), but it will never cause any harm for you.
- `-v "$PWD":/workspace` (UNIX) / `-v %cd%:/workspace` (Windows)\
    Mount (map) the current directory on the host to `/workspace` inside the container.
- `-e HOST_USER_ID=$(id -u) -e HOST_GROUP_ID=$(id -g)` (UNIX only)\
    This will ensure that the user inside the container shares user ID and group ID with the user on the host. Whenever you are using the `-v` argument to mount directories, these arguments should be provided as well to ensure proper file permissions, both on read/write.
- `-p <HOST_PORT>:<CONTAINER_PORT>`\
    Publish a port. Make port <CONTAINER_PORT> visible outside of the container, mapping it to <HOST_PORT>. For example, we will use the `-p 9090:8888` argument to make Jupyter Notebooks visible outside of the container.
- `--gpus all`\
    Provide the container access to the host GPU(s). Can only be used if certain requirements are met on the host (Docker >= 19.03, Linux, etc.)

If you are using Mac / Linux, you will suffer from the particularly cumbersome arguments `-e HOST_USER_ID=$(id -u) -e HOST_GROUP_ID=$(id -g)`, so we have provided a wrapper script called `rundocker-mapuid.sh`, which provides you with a shorthand
```
./rundocker-mapuid.sh ARG1 ARG2 ARG3...
```
instead of
```
docker run -e HOST_USER_ID=$(id -u) -e HOST_GROUP_ID=$(id -g) ARG1 ARG2 ARG3...
```
`./rundocker-mapuid.sh` above assumes that you are currently at the root of the git repository. Otherwise you need to specify the path to the script.

If you find it useful, you are encouraged to create your own wrapper scripts.


## Keeping the Docker image up to date
When you use `docker run` (or the `rundocker-mapuid.sh` wrapper script), Docker will first search for the Docker image locally on your computer, but if there is no image, it will conveniently download it from Docker Hub (this is where we host the course Docker image).
**However**, if we make changes to the Docker image and push a new version to Docker Hub, your `docker run` calls will still use the local image.
Therefore remember to run the below command, to make sure you have the latest course Docker image. This may be run from any directory.

```
docker pull ssy340dml/dml-image:gpu
```
Note: On Google Cloud, this is done automatically each time you login.

## Lightweight alternative image
If you have limited resources on your system, there is a version of the docker image without GPU support, which might consume less disk space. Just replace `ssy340dml/dml-image:gpu` with `ssy340dml/dml-image:cpu` in every command involving the image.
