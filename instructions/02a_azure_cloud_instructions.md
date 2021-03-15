# Instructions for setting up Azure

For assignments HA1, HA2, and your final project, you will need a GPU-enabled machine. This guide will show you how to set up and connect to an Azure cloud machine with GPU, referred to as a virtual machine.

You will always be interacting with your virtual machine in Azure's servers via a terminal, or terminal emulator. Hence, it's important to know [a few commands](http://www.informit.com/blogs/blog.aspx?uk=The-10-Most-Important-Linux-Commands) to be able to perform simple tasks (like changing directories, copying files, moving files, etc).

## 1. Registering for Azure Students

- Navigate to https://azure.microsoft.com/en-us/free/students/ and click the green _Activate now_ button.
- Create a Microsoft account and follow the steps for activating your free credits. Use your institutional e-mail (@net.chalmers.se, @student.chalmers.se, @chalmers.se or @student.gu.se) for the registration.
- Once everything is approved you'll get an e-mail confirmation. Now you're ready to follow the next steps in this guide.

## 2. Creating an instance

- **Note**: As soon as the instance is created it will be started, already consuming your credits. Make sure you follow this step until the end to stop it after creation.
- Navigate to https://portal.azure.com/ and login.
- Under _Azure Services_, click on _Virtual machines_, you'll be redirected to a new page.
- Click on Add > Virtual Machine.
- Don't change anything in this page except for the following:
  - In **Resource group**, click on _Create new_. Name it `MyRG` and click on _ok_.
  - In **Virtual machine name** give your instance an appropriate name, e.g. "`dml-instance`".
  - In **Region** choose one of the recommended regions.
    - **Note** Some regions might not have GPUs available, if that's the case try another region. Here's a list of all the regions that (at the time of writing this) have the GPU we'll use: East US; South Central US; Australia East; Southeast Asia; North Europe; UK South.
  - In **Image**, click on _See all images_. Search for `ngc` in the search box, and click on the result with the name `NVIDIA GPU-optimized Image for AI & HPC - v20.06.3`.
  - In **Size**, click on _Select all sizes_. Then, search for `NC6`, and choose the result with the name `NC6`, then click the blue button on the bottom named _Select_. (There are other GPU-enabled machines to choose from, but we have only tested running the assignments for NC6 and NV6. You can find all GPU options by filtering on Family: GPU.)
  - In **Username**, select a username for logging in to your instance.
    - **Note**: Write this down, we'll use it later for connecting to the instance. If you forget it you won't be able to login to your instance.
- Click on the blue button on the bottom of the page named _Review + Create_, and wait for the final validation to pass.
- Fill in the required fields (name, e-mail, phone number) and accept the terms associated with the Marketplace offerings.
- Click on the blue button on the bottom of the page named _Create_.
- A pop-up will appear requesting you to generate new key pairs. Click on _Download private key and create resource_. A `*.pem` file will be downloaded, keep it stored in a safe place, we'll use it to connect to the instance later (if you misplace this file you won't be able to connect to your instance anymore).
- You will be taken to a webpage that says _Deployment is in progress_. Wait for it to finish, when it will then exhibit the message _Your deployment is complete_
- Click on the blue button _Go to resource_.
- Click on the button with a square on its left, named _Stop_. A message will show up regarding IP addresses, click on _ok_.
- Now click on _Networking_ in your instance's Properties tab. Then, click on _Add inbound port rule_. Under _Destination port ranges_, type `8888`. Under _Name_, type `JUPYTER_PORT`. Finally, click on _Add_.
- Congratulations, you have now created your instance! You also stopped it, so that it doesn't consume credits while you're not using it. Now keep following the next steps, in order to connect to it, and set up all the required software.

## 3. Connecting to the instance

- Navigate to https://portal.azure.com/ and login.

- Under _Azure Services_, click on _Virtual machines_, you'll be redirected to a new page.

- If you followed step 1 of this guide correctly, you should now see your newly-created instance in this page. Click on its name.

- Click on _Start_ and wait until the instance has started; the _Start_ button will be greyed out when this happens, and the _Status_ of the instance will be shown as _Running_.

  - **Note**: As soon as the instance starts it will be consuming credits. This only halts when you stop it. Take this into account when following the next steps.

- In the _Properties_ part of the webpage you're currently in, you'll find your instance's _Public IP address_, under _Networking_. Write it down somewhere, we'll use it in the next steps.

  - **Note**: Sometimes it takes a few seconds for the IP of a recently-started machine to show up in the webpage. If that's the case, refresh your webpage after starting the instance.

- Now we're going to open the browser-based Shell that Azure provides, so we can login to the instance. Click on the shell icon on the blue bar at the top of your screen. It is a square with the symbols `>_` inside it (and when you hover over it it says _Cloud Shell_).

- You'll be prompted to create some storage for the shell, accept it.

- The bottom part of the webpage will now become a terminal, where you can type commands for the next steps of this guide. The rest of this guide assumes you will use the Bash version of the terminal (by default, this is the one you start with), instead of the Powershell version.

- Drag-and-drop the `*.pem` that you downloaded when creating this instance into the terminal. A message will appear on the bottom-right telling you that the upload was successful.

- In the terminal, type the following commands:

  - ```
    chmod 400 <filename>.pem
    ```

    (substitute `<filename>` with the name of your `*.pem` file).

  - ```
    ssh -i <filename>.pem <user>@<public-ip>
    ```

    (substitute `<user>` with the username you chose when creating the instance, and `<public-ip>` with the _Public IP address_ mentioned previously in this guide).

  - **Note**: If after running the `ssh` command nothing happens for a while, make sure you typed the correct IP address for your instance. If not, use `Ctrl+c` to cancel the current command and type in the correct address. Also note that even if the instance is marked as "running" after starting up, it might take a little while before you can actually connect to it.

- You will now see a message stating that you're connected to the instance, and the green text before the cursor in the terminal will say `<username>@<instance-name>` (your values, of course), instead of `<username>@Azure`.

- Congratulations, you have now connected to your instance! Any commands you run here will be performed by your instance, and the output will be displayed in this terminal.

- When you're done using your instance, you can type `exit` in the terminal to disconnect from it. **Note that this does not stop the instance**. To do so, and stop consuming credits, you have to manually click on the _Stop_ button for your instance. Make sure the instance is stopped by waiting until the _Stop_ button is greyed out, and the _Start_ button becomes available again.

  - **Important note**: Forgetting to stop your instance is a common mistake that will cost you many (if not all) credits! Be mindful of this and always click on the stop button after using the instance, and wait for the confirmation that the instance was truly stopped
  - **Important note 2**: There are a couple of gotchas regarding stopping the instance, i.e. you might thing you have stopped it but you actually haven't. This includes running `sudo poweroff` or using the Azure CLI to stop the instance, without **deallocating** it. No matter how you choose to stop the virtual machine, make sure that its state goes to **Stopped (deallocated)**.

  - **Important note 3**: Leaving the browser based shell in a semi-active state (like training networks) for a long time can cause the shell to terminate the VM connection. We don't have a good fix for this but using a proper shell on your computer, rather than the browser one, will be more stable.

## 4. Setting up all the required software in your instance

- Connect to your instance, like described previously.

- In your instance, clone the course repository using the command:

  ```
  git clone https://github.com/JulianoLagana/deep-machine-learning.git
  ```

  This will create a folder in your home directory called `deep-machine-learning` (you can check the contents of your current directory with the command `ls`).

  - **Note**: This command must be run from your `home` directory (which is the one you start on after connecting to the instance).

- Now run the command:

  ```
  ./deep-machine-learning/instructions/configure_cloud_machine.sh
  ```

  When prompted whether to proceed, simply press enter. This will install all the required software for the course, and will create a conda environment for you. It may take a few minutes, specially the part where conda is installing pip dependencies.

  - **Note**: If you just created your instance, you might run into the error `Unable to acquire dpkg frontend lock`. If that's the case, just wait a few minutes and try the same command again, the instance is still updating some packages in the background.

  - **Note** 2: Another possible error states that `dpkg was interrupted`. If you run into that, execute the command

    ```
    sudo dpkg --configure -a
    ```

    and re-run the previous command.

- Once everything is installed, disconnect from the instance with the command

  ```
  exit
  ```

  and then connect to it again like described previously. **Note**: This is important for the setup, so that the terminal is reinitialized; don't skip this step. **Note 2**: This command _does not_ stop your instance, it just disconnects you from it while leaving it running in the background.

- You are now ready to start a Jupyter notebook in the instance and connect to it by following the instructions [here](https://github.com/JulianoLagana/deep-machine-learning/blob/master/instructions/03_using_jupyter_notebooks_on_cloud.md).
