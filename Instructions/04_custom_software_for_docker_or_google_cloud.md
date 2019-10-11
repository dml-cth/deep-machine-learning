# Install custom software for Docker and/or Google Cloud
During the project, you might very well need to install some software that is specific to your project and was not already provided by us.

## Install custom software for Docker (locally or on cloud)
To install custom software in the Docker environment, follow the steps below. Do however first make sure you have pulled the latest Docker image.

### Temporarily install software in container
1. Startup a terminal inside the Docker container. There are a few ways you can do this:
  - Run Docker (`docker run -it ...` / `./rundocker-mapuid.sh ...`) with the `bash` argument at the end of the whole command. This will start a new container, and bring you into a bash terminal inside of it.
  - Start a Jupyter server. Connect to it from a browser as usual, and navigate to "New -> Terminal".
  - Alternatively, you can refrain from starting a terminal, and instead use a notebook to run terminal commands (see [here](https://support.anaconda.com/hc/en-us/articles/360023858254-Executing-Terminal-Commands-in-Jupyter-Notebooks)).
1. Run whatever commands you need in order to install additional software. You (the `dml-guest` user) has `sudo` privileges inside the container.
  - To install Ubuntu packages, run `sudo apt-get install ...`
  - To install Python packages, you need to switch to the user `condauser`:
    1. Switch users with `sudo su condauser`
    1. Run `conda install ...` / `pip install ...` to install the Anaconda or pip packages you need.
    1. Run `exit` to go back to the `dml-guest` user.
1. You should now have your software installed for as long as the container will be running (i.e. until you exit the bash terminal, or until you stop the Jupyter server, depending on what you did in the first step. When the container stops however, the software you installed will be lost. You basically have two options here:
  - Repeat the installatiojn procedure every time you start a container.
  - Before the container stops, make the changes permanent - according to the next section.

### Make the installed software permanent
You can use the `docker commit` command while the container is still running, in order to create a new image based on the container. If you then start a new container (with the `docker run` command) with the image you just created, instead of an image we provided (e.g. `ssy340dml/dml-image:gpu`), the software you installed will be preserved.

The documentation for this command can be found here: [https://docs.docker.com/engine/reference/commandline/commit/](https://docs.docker.com/engine/reference/commandline/commit/).

The gist of it is: install software in your container, according to instructions above, then run in a terminal, *outside of the container*

```bash
# Check what images already exist
docker image ls

REPOSITORY            TAG                             IMAGE ID            CREATED             SIZE
ssy340dml/dml-image   gpu                             2d6011daf7a1        18 hours ago        9.15GB

docker ps

CONTAINER ID        IMAGE               			COMMAND             CREATED   	...
c3f279d17e0a        ssy340dml/dml-image:gpu   /bin/bash           7 days ago  ...

# docker commit CONTAINER [REPOSITORY[:TAG]]
docker commit c3f279d17e0a my_own/image:tag_name

sha256:<some_hash>

# Check images again
docker image ls

REPOSITORY            TAG                             IMAGE ID            CREATED             SIZE
my_own/image          tag_name                        d64ab5954617        7 seconds ago       9.18GB
ssy340dml/dml-image   gpu                             2d6011daf7a1        18 hours ago        9.15GB
```

## Build you own docker file

**Note:** You should know your way around your computer if you want to try this

We have published the Dockerfiles we use to build the images from scratch.
You can find the in the public repo at `Tools/Docker`
If you are feeling adventurous you can build your very own docker image from a Dockerfile.

The documentation for this command can be found here: [https://docs.docker.com/engine/reference/commandline/build/](https://docs.docker.com/engine/reference/commandline/build/)

### Change the Dockerfile

Edit `Tools/Docker/dml-image/context/Dockerfile` to make your changes.
To install packages, add them to the `RUN apt-get` command:

```bash
RUN apt-get update && \
    apt-get install -y --no-install-recommends apt-utils && \
    apt-get install -y --no-install-recommends \
        curl \
		<name_of_your_package> \
        unzip \
        git
```

To add python packages via conda: edit `Tools/Docker/dml-image/context/conda-environment-<cpu/gpu>.yml`,
by adding packages in the `pip` section.

### Build the image

These commands will build the CPU/GPU course Docker images, respectively.

```bash
docker build --build-arg CONDA_ENV_SUFFIX=cpu -t ssy340dml/dml-image:cpu Tools/Docker/dml-image/context
docker build --build-arg CONDA_ENV_SUFFIX=gpu -t ssy340dml/dml-image:gpu Tools/Docker/dml-image/context
```

### Important with failed builds
Even though a build of a docker image fails, it still produces a quasi-image with `<none>` repo and tag:

```bash
docker image ls # After a failed build
REPOSITORY          TAG                             IMAGE ID            CREATED                  SIZE
<none>              <none>                          68bcd71e6d92        Less than a second ago   9.13GB
nvidia/cuda         10.0-cudnn7-devel-ubuntu16.04   b739d7317c55        4 weeks ago              3.12GB
```

Failure to remove these artefacts may have something to do with strange computer issues (e.g. computer not booting).
By forcing the removal of the artefacts, the issues seem to go away:

```bash
docker image rm --forced <IMAGE ID>
```
*Note:* This is a working hypotheses, but it does not hurt to be careful.


## Install custom software on cloud without Docker
If you find it more convenient to scrap the Docker environment altogether - feel free to install all of your software from scratch, but note that we do not have the time to support you in this endeavor.

Simply put, instead of creating a compute instance based on the image we provided for you (`ssy340dml-host-image` from the project `ssy340dml-image-project`), you can use any of the publicly available Google Cloud images.
Note that "image" in this context, does not refer to a Docker image.

You can find the available images on [this page](https://console.cloud.google.com/compute/images).
For instance, there are Ubuntu images with CUDA+Pytorch already installed.
