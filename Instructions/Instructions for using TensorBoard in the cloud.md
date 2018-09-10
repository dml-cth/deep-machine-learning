# Instructions for using TensorBoard in the cloud

- When running a Keras method for training your model, make sure to supply TensorBoard as one of the callbacks (CL2 has an example).

- Once your network is being trained, a folder (usually called `logs`) will be created in the same directory.

- Open a new terminal in the instance (for instance, by clicking again in the SSH button for your instance, then changing user, etc) , `cd` to the directory that has the notebook you're running (and contains the `logs` folder), and run:

  ```bash
  tensorboard --logdir=logs
  ```

  where `logs` is the name of the directory created by the TensorBoard callback.

- Now open a new browser window in your local machine and go to `http://<instance_ip>:6006`, where `<instance_ip>` is your instance's external IP address (which you can find in the same line that shows the instance's name).



Tip: for discerning between different runs of the same network, you can create TensorBoard callbacks that save the log files to different subfolders of the `logs` folder. This way TensorBoard will know that each one is a different run, and display all of them with different colors (CL2 has an example of this).