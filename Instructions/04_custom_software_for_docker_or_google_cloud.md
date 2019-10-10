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
You can use the `docker commit` command while the container is still running, in order to create a new image based on the container. If you then start a new container (with the `docker run` command) with the image you just created, instead of an image we provided (e.g. `ssy340dml/dml-image:gpu`), the software you installed should be preserved.

More specific instructions on this might follow later. If not refer to [https://docs.docker.com/engine/reference/commandline/commit/](https://docs.docker.com/engine/reference/commandline/commit/).


## Install custom software on cloud without Docker
If you find it more convenient to scrap the Docker environment altogether - feel free to install all of your software from scratch, but note that we do not have the time to support you in this endeavor.

Simply put, instead of creating a compute instance based on the image we provided for you (`ssy340dml-host-image` from the project `ssy340dml-image-project`), you can use any of the publicly available Google Cloud images.
Note that "image" in this context, does not refer to a Docker image.

You can find the available images on [this page](https://console.cloud.google.com/compute/images).
For instance, there are Ubuntu images with CUDA+Pytorch already installed.
