## Instructions for using TensorBoard
**Note:** Before starting out, walk through the Docker instructions and make sure you are familiar with running Docker.

If you make use of TensorBoard in your assignments, you will let experiment files will be written to a directory of your choice (assumed to be called `logs`) in the following. This guide will show you how to start up a TensorBoard server, in order to visualize the results of your experiments.

### On your local computer
Start up the server by running:
```
docker run --rm -p 6006:6006 tensorflow/tensorflow tensorboard --logdir logs
```
- TensorBoard will search through the `logs` directory for any experiment files produced by your training.

- Open a new browser window and go to `http://localhost:6006`.

Tip: for discerning between different runs of the same network, you can create TensorBoard callbacks that save the log files to different subfolders of the `logs` folder. This way TensorBoard will know that each one is a different run, and display all of them with different colors (CL2 has an example of this).

### On the cloud
- Connect to the compute instance with a new SSH session (for instance, by opening a new tab in the Cloud Shell), and change to the `dml-host` user. `cd` to the directory that has the notebook you're running (and contains the `logs` folder)

- Run the same command as above to start up a TensorBoard server:
```
docker run --rm -p 6006:6006 tensorflow/tensorflow tensorboard --logdir logs
```

- Now open a new browser window on your local machine and go to `http://<instance_ip>:6006`, where `<instance_ip>` is your instance's external IP address (which you should know how to assess by now).
