# FROM nvidia/cuda:10.0-cudnn7-runtime-ubuntu16.04
FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu16.04

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN apt-get update && \
    apt-get install -y --no-install-recommends apt-utils && \
    apt-get install -y --no-install-recommends \
        curl \
        unzip \
        git

# Install gosu, in order to switch to a particular user, matching the host UID, during runtime
# From: https://denibertovic.com/posts/handling-permissions-with-docker-volumes/
RUN gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4
RUN curl -o /usr/local/bin/gosu -SL "https://github.com/tianon/gosu/releases/download/1.4/gosu-$(dpkg --print-architecture)" \
    && curl -o /usr/local/bin/gosu.asc -SL "https://github.com/tianon/gosu/releases/download/1.4/gosu-$(dpkg --print-architecture).asc" \
    && gpg --verify /usr/local/bin/gosu.asc \
    && rm /usr/local/bin/gosu.asc \
    && chmod +x /usr/local/bin/gosu


# Install CLoud SDK. Command from https://cloud.google.com/sdk/docs/quickstart-debian-ubuntu
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-sdk -y


# Clean up apt - less bloated container
RUN rm -rf /var/lib/apt/lists/*


WORKDIR /workspace


# ==============================================================================
# CONDA
# https://pytorch.org/get-started/locally/#anaconda-1
# ==============================================================================
RUN curl -o ~/miniconda.sh -O  https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh  && \
     chmod +x ~/miniconda.sh && \
     ~/miniconda.sh -b -p /opt/conda && \
     rm ~/miniconda.sh
ENV PATH /opt/conda/bin:$PATH
RUN conda update -n base -c defaults conda

# ARG GPU_SUPPORT=1
# RUN if [ "$GPU_SUPPORT" = "1" ] ; then conda install -y -c pytorch pytorch-cpu torchvision-cpu; else conda install -y -c pytorch pytorch torchvision cudatoolkit=9.0; fi
# # RUN conda install -y -c pytorch pytorch-cpu torchvision-cpu
# # RUN conda install -y -c pytorch pytorch torchvision cudatoolkit=9.0

# Determine environment of choice, and select corresponding environment file
ARG CONDA_ENV_SUFFIX=gpu
COPY conda-environment-"$CONDA_ENV_SUFFIX".yml /tmp/environment.yml

# Proxy user "condauser" installs conda environment, but provides access to actual user "dml-guest" (which will be added later)
# HACK: ID 7892 assumed not to collide with the IDs to be copied from host later
RUN groupadd -g 7892 -o condauser
RUN useradd --shell /bin/bash -u 7892 -g condauser -o -m condauser
WORKDIR /home/condauser
USER condauser
RUN conda env create -f /tmp/environment.yml
# Optionally provide write permissions to conda packages: (but read permissions should be enough, and running recursive chmod takes a lot of time) 
#RUN chmod -R 777 /home/condauser/.conda
USER root
WORKDIR /workspace
# Refrain from removing /tmp/environment.yml - might be of use for hacky students, wanting to work outside Docker
RUN conda clean -ya
# ==============================================================================


# Entrypoint script for adding a new user, matching the host UID
# From: https://denibertovic.com/posts/handling-permissions-with-docker-volumes/
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]


# Configure jupyter
COPY gen_passwd.py /gen_passwd.py
COPY config-password-and-start-jupyter-server.sh /config-password-and-start-jupyter-server.sh
RUN chmod +x /config-password-and-start-jupyter-server.sh

CMD ["/config-password-and-start-jupyter-server.sh"]
