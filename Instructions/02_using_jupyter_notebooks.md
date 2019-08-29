# Instructions for using Jupyter Notebooks
**Note:** Before starting out, walk through [01_getting_started_with_docker.md](01_getting_started_with_docker.md) and make sure you are familiar with running Docker.

## How to run Jupyter Notebooks on your local computer

- Open up a terminal (or Windows prompt / Powershell), and `cd` into the git repository you have previously cloned.

- Start a Jupyter server with one of the following commands:
  - Mac / Linux without GPU access
    ```
    ./rundocker-mapuid.sh -it -v "$PWD":/workspace -p 9090:8888 ssy340dml/dml-image:gpu
    ```
  - Linux with GPU access (the `--gpus all` argument is essential in order to let the container access the host GPU)
    ```
    ./rundocker-mapuid.sh -it -v "$PWD":/workspace -p 9090:8888 --gpus all ssy340dml/dml-image:gpu
    ```
  - Windows
    ```
    docker run -it -v %cd%:/workspace -p 9090:8888 ssy340dml/dml-image:gpu
    ```

- Note that the above command will run the course Docker image, with no explicit command to be run, in which case it defaults to start a Jupyter Notebook server on port 9090. (actually it is port 8888 inside the Docker container, which is mapped to port 9090 outside of it)

- The first time you run the command, you will be prompted to set up a password. **Choose this with care**, since anybody in the world could potentially connect to your computer, login with the password, and run python scripts or even terminal commands. They could however only access resources provided to the isolated Docker container (such as the current directory contents).

- A hash of your password will be stored in a file named PASSWD_HASH.txt in the current directory. Next time you start a Jupyter Notebook server from this directory, this file will be detected and you will not need to type in the password again. In order to change your password, just remove the file and run the server once again.

- Open a new browser window in your local machine and navigate to the address `http://localhost:9090`.

- You will now see a web page asking you for a password. Provide the password you set up when starting the Jupyter server, and log in.

- You will now see the contents of the `/workspace` directory of the Docker container, which should be mapped to the current directory of your host environment, where you issued the command to start the server.


## How to run Jupyter Notebooks in the Cloud

- Connect to your instance, change to the `dml-host` user, and `cd` into the git repository you have previously cloned.

- Start a Jupyter server with the following command. (The `--gpus all` argument is essential in order to let the container access the host GPU)
  ```
  ./rundocker-mapuid.sh -it -v "$PWD":/workspace -p 9090:8888 --gpus all ssy340dml/dml-image:gpu
  ```
  It may prompt you for a password, just as explained above in the case on your local computer.

- Now take a look at the VM instances web page in the Google Cloud's console. There, in the same line where you see the name of your instance, you will also see its external IP. For instance, something like 35.255.15.79. (Alternatively, you can obtain this information with the `gcloud compute instances list` command, but note that this should not be run on the compute instance itself.)

- Open a new browser window in your local machine and navigate to the address `http://<external_ip>:9090`, where `<external_ip>` is the IP address you obtained in the previous step. For instance, in my case I would connect to `http://35.255.15.79:9090`.

- If all of the steps above have been followed correctly, you will now see the web page asking you for a password. Provide the password you set up when starting the Jupyter server, and log in.

- You are now connected to your Jupyter server running in the Google Cloud's instance.

- You can use the Jupyter web interface to upload files to your instance (for example, Python notebooks you have developed when working in your local computer, or datasets that you'll use to train on the Cloud). To do so, simply click the button "Upload" on the top of the Jupyter web interface (to the right of the text "Select items to perform actions on them.", and to the left of the "New" button).
