# Instructions for using Google Cloud

For assignments HA1, HA2, and your final project, we have set up a Google Cloud machine with a K80 GPU and (almost) all the necessary programs and packages you will need. This guide explains how to connect to this instance.

You will always be interacting with your virtual machine in Google Cloud's servers via a terminal, or terminal emulator. Hence, it's important to know [a few commands](http://www.informit.com/blogs/blog.aspx?uk=The-10-Most-Important-Linux-Commands) to be able to perform simple tasks (like changing directories, copying files, moving files, etc).



#### 1. Login to Google Cloud and see your instance

- When it's time to start using Google Cloud, you will get an e-mail from us saying that you have been invited to a Google Cloud project. Accept the invitation.
- Go to https://console.cloud.google.com. This is the web page you will always use to access Google Cloud.

- Click on the "Navigation Menu" button, on the top left corner of the Google Cloud console (three parallel horizontal bars). This brings up all the options you have in Google Cloud.

- Hover your mouse over "Compute Engine", and then click "VM instances" in the new menu that pops up. This brings you to the VM instances web page. Here you can see the instance (the computer in Google Cloud's servers) that you have access for our course, called `gpu-instance`.
- Eventually you will be a member of more than one project in Google Cloud (one for HA1 and the project, and another one for HA2). Each project has a different `gpu-instance` in it. The current active project's name is shown in the top blue bar in Google Cloud's console, to the right of "Google Cloud Platform". Click on it to change the current active project.



#### 2. Connecting to your instance

- Click on the check box to the left of the instance's name to select it. After selecting it, click on "START" in the top menu (below the blue bar). This starts the instance booting procedure. When the instance is ready to be used its icon will change to a green circle.s

- When the instance is ready, you can click on the "SSH" button. This button is located in the same line where you can see the name of your instance. That will pop-up a new browser window with a terminal emulator connected to your instance.

- One of the first messages that you will see in this terminal is the amount of hours you already used in this instance. You can check this again whenever you want by typing the following command in the terminal:

  ```bash
  check_quota
  ```



#### 3. Changing to the `student` user and using the instance

- You always login as an user with the same name as your Gmail account. However, all the configurations we created are are for the `student` user. To change to the `student` user, input the following in the terminal:

  ```bash
  su - student
  ```

  You will then be prompted for the `student`'s password, which is also `student`. Once you input the password and press enter, you will log in as the `student` user, and be changed to its home directory.

- All the required packages are installed in a conda environment called `dml_gpu`. To activate it, run:

  ```bash
  source activate dml_gpu
  ```

- Now you are ready to use the instance for the assignments. If this is the first time you connect to the instance, you might also want to clone the GitHub repository. You can do so with the command:

  ```bash
  git clone https://github.com/JulianoLagana/deep-machine-learning.git
  ```

  This creates the course folder in the current directory you are in.



#### 4. Disconnect and stop the instance

- When you are done using the instance, you can close the browser window with the terminal emulator to disconnect from it. **HOWEVER**: the instance will still be running, and therefore still consuming your hour quota. Hence, it's extremely important to also stop your instance.
- To stop the instance, simply click on the check box to the left of its name, and then click on "STOP". Wait until the instance's icon changes to a gray circle with a white square inside it. It's good practice to wait until that happens, since if any errors occur after you click "STOP", and you close the browser's window right after, you might still have the instance running without knowing.