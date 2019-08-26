## Instructions for using TensorBoard
Before starting out, walk through the Docker instructions and make sure you are familiar with running Docker. Either locally or on the cloud, the following command starts up a TensorBoard server.

- If you make use of TensorBoard in your assignments, you will let experiment files will be written to a directory of your choice (assumed to be called `logs`) in the following.

- Connect to the compute instance with a new SSH session (for instance, by opening a new tab in the Cloud Shell), and change to the `dml-host` user. `cd` to the directory that has the notebook you're running (and contains the `logs` folder), and run:

```bash
docker run --rm -p 6006:6006 tensorflow/tensorflow tensorboard --logdir logs
```
- TensorBoard will search through the `logs` directory for any experiment files produced by your training.

- Now open a new browser window on your local machine and go to `http://<instance_ip>:6006`, where `<instance_ip>` is your instance's external IP address (which you should know how to assess by now).

Tip: for discerning between different runs of the same network, you can create TensorBoard callbacks that save the log files to different subfolders of the `logs` folder. This way TensorBoard will know that each one is a different run, and display all of them with different colors (CL2 has an example of this).
