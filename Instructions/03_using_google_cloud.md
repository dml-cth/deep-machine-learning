# Instructions for using Google Cloud

For assignments HA1, HA2, and your final project, you will need a GPU enabled machine. This guide will show you how to set up and connect to a Google Cloud machine with a K80 GPU, referred to as a compute instance.

You will always be interacting with your virtual machine in Google Cloud's servers via a terminal, or terminal emulator. Hence, it's important to know [a few commands](http://www.informit.com/blogs/blog.aspx?uk=The-10-Most-Important-Linux-Commands) to be able to perform simple tasks (like changing directories, copying files, moving files, etc).

You are advised to perform steps 1-3 early on in the course, as they involve redeeming Google Cloud coupons & requesting GPU resources on the cloud, both of which may take some time to sort out, should any issues occur. Step 3 could potentially take up to 48h, but more commonly just a few minutes.


#### 1. Confirm your redeemed coupon and login to Google Cloud

- We will redeem a $50 Google Cloud coupon for each of you, upon which you will get an e-mail from Google Cloud to confirm that the personal details we have provided are correct.
- When you have confirmed this, login to https://console.cloud.google.com. This is the web page you will always use to access Google Cloud.
- Again: the $50 coupon should last for the entirety of the course, provided that you handle your Google cloud machine with care.


#### 2. Create & configure a Google Cloud project

Essentially all operations on Google Cloud can be performed either via a web GUI, referred to as the [Cloud Console](https://console.cloud.google.com), or via a command-line interpreter using the `gcloud` CLI tool. The `gcloud` CLI tool can either be installed on your own computer, or may be used on the cloud via the "Cloud Shell".

Access the Cloud Shell, by clicking the [**>\_**] icon on the top right, and then clicking "Start Cloud Shell". Multiple "Cloud Shell" sessions can be used simultaneously, and accessed via different tabs.

Create a Google Cloud project (you will have to be a bit creative with the project id, since you are not alone on the cloud)
```
gcloud projects create <PROJECT_ID>
```
Verify access to billing account. You are expected to see an account `Deep machine learning` with an `ACCOUNT_ID`.
```
gcloud alpha billing accounts list
```
Link project to billing account (this allows the project to use the cloud credits)
```
gcloud alpha billing projects link <PROJECT_ID> --billing-account <ACCOUNT_ID>
```
Set the default project & zone (so they need not be specified in the following commands). Alternatively, most commands accept --project & --zone arguments, which override the defaults.
```
gcloud config set core/project <PROJECT_ID>
gcloud config set compute/zone europe-west1-b
```
Verify default project & zone
```
gcloud config get-value core/project
gcloud config get-value compute/zone
```
Activate Compute Engine for the project (this allows you to create compute instances within it)
```
gcloud services enable compute.googleapis.com
```
Configure project firewall, to allow remote connections to the cloud
```
gcloud compute firewall-rules create open-port-jupyter --allow tcp:9090 --direction INGRESS
```

#### 3. Request GPU quota increase
**Instructions on this will be provided later**
<!-- Link to find where to apply for increased GPU quota:
https://console.cloud.google.com/iam-admin/quotas?_ga=2.233391134.-1027612475.1543580804&project=YOURPROJECTNAME&folder&organizationId&metric=GPUs%20(all%20regions) -->

#### 4. Create a compute instance
Upon creation, a cloud instance is **automatically started**, which also means it starts to consume credits. Therefore, make sure you know how to stop it before proceeding (see instructions down below).

Create a Google Cloud compute instance called `gpu-instance`.
```
gcloud compute instances create gpu-instance \
     --custom-cpu=8 \
     --custom-memory=16 \
     --accelerator type=nvidia-tesla-k80,count=1 \
     --maintenance-policy TERMINATE \
     --restart-on-failure \
     --boot-disk-size=20GB \
     --boot-disk-type=pd-standard \
     --image-project ssy340dml-image-project \
     --image ssy340dml-host-image
```
<!-- ```
gcloud compute instances create-with-container gpu-instance \
     --accelerator type=nvidia-tesla-k80,count=1 \
     --maintenance-policy TERMINATE \
     --restart-on-failure \
     --custom-cpu=8 \
     --custom-memory=16 \
     --container-image registry.hub.docker.com/ssy340dml/gcloud-host-image
```
```
gcloud compute instances create-with-container gpu-instance \
     --accelerator type=nvidia-tesla-k80,count=1 \
     --maintenance-policy TERMINATE \
     --restart-on-failure \
     --custom-cpu=8 \
     --custom-memory=16 \
     --boot-disk-size=20GB \
     --boot-disk-type=pd-standard \
     --container-image registry.hub.docker.com/ssy340dml/gcloud-host-image
``` -->
**Stop** the instance if you do not plan on using it directly.
```
gcloud compute instances stop gpu-instance
```

#### 5. (If needed) Create a CPU-only instance
If you for some reason cannot work locally, you could also create a (much cheaper) CPU instance, and do most of your work on that one. Replace the command above with the following.
```
gcloud compute instances create cpu-instance \
     --machine-type n1-standard-4 \
     --maintenance-policy TERMINATE \
     --restart-on-failure \
     --boot-disk-size=20GB \
     --boot-disk-type=pd-standard \
     --image-project ssy340dml-image-project \
     --image ssy340dml-host-image
```
**Note**, that you are still supposed to use the GPU docker image when working on the cloud, since it will be synced by default if updated. The GPU image has no limitations, the only advantage with the CPU version is its reduced disk consumption.

#### 6. Visualizing your compute instance (optional)
You may now move away from the `gcloud`  CLI tool, and visualize the results using the Cloud Console instead.

- The current active project's name is shown in the top blue bar in Google Cloud's console, to the right of "Google Cloud Platform". Make sure that the project you created is selected here.

- Click on the "Navigation Menu" button, on the top left corner of the Google Cloud console (three parallel horizontal bars). This brings up all the options you have in Google Cloud.

- Hover your mouse over "Compute Engine", and then click "VM instances" in the new menu that pops up. This brings you to the VM instances web page. Here you can see the instance (the computer in Google Cloud's servers) that you have access to for our course, called `gpu-instance`.

- You can quite intuitively see whether the instance is running or not, start/stop it, as well as connecting to it via SSH. Below we will go through the command-line way instead, but feel free to do the same steps in graphically in the Cloud Console if you prefer.


#### 7. Connecting to your compute instance
Start the compute instance. Make sure you know how to stop it before proceeding (see instructions down below).
```
gcloud compute instances start gpu-instance
```
Assess the **external** IP of the instance, and note it down. This will be necessary later, when connecting to the instance from your own computer.
```
gcloud compute instances list gpu-instance
```
Connect to the compute instance via SSH. When asked to generate SSH keys, just comply. Leave the password empty and press ENTER.
```
gcloud compute ssh gpu-instance
```
Note that after starting up the instance, it may take a little while before it is ready to receive SSH connections (a few seconds up to a minute at most). If the above command is failing but the instance is running, simply try again.


#### 8. Changing to the `dml-host` user and run the docker container
Change to the `dml-host` user, which has permission to use Docker (it is part of the `docker` group).
```
sudo su - dml-host
```
You will notice that every time the `dml-host` user is logged in, the course Docker image will be automatically synced, to ensure you are up-to-date with any changes we may push to it.

You can now run Docker just like on your local computer, as explained in the separate Instructions for using Docker.

Start with cloning the course git repository, like explained in [01_getting_started_with_docker.md](01_getting_started_with_docker.md):
```
docker run -it -e HOST_USER_ID=$(id -u) -e HOST_GROUP_ID=$(id -g) -v "$PWD":/workspace ssy340dml/dml-image:gpu git clone https://github.com/JulianoLagana/deep-machine-learning.git
```

This creates the course folder in the current directory you are in.

**DO NOT FORK THIS REPOSITORY**\
You might be tempted to use git for syncing your work within your groups or between your local computer and the cloud. This is fine as long as you know what you are doing, but you are under no circumstances allowed to make your assignments publicly available. Be aware that GitHub forks of public repositories (such as this one) will always be public.



#### 9. Disconnect and stop the compute instance
Exit the SSH session. **Note** that even after you disconnect, the instance will still be running, and consuming your credits!
```
exit
```
Stop the compute instance.
```
gcloud compute instances stop gpu-instance
```
You can verify that the instance has stopped, by checking its status, either using the graphical Cloud Console (as explained above), or by the following command. Note that in both these cases, only the instances in the currently selected project will be listed.
```
gcloud compute instances list
```

<!-- - When you are done using the instance, you can close the browser window with the terminal emulator to disconnect from it. **HOWEVER**: the instance will still be running, and therefore still consuming your hour quota. Hence, it's extremely important to also stop your instance.
- To stop the instance, simply click on the check box to the left of its name, and then click on "STOP". Wait until the instance's icon changes to a gray circle with a white square inside it. It's good practice to wait until that happens, since if any errors occur after you click "STOP", and you close the browser's window right after, you might still have the instance running without knowing. -->


#### 10. Monitor your credit balance and past consumption
Go to http://console.cloud.google.com

- Click on the "Navigation Menu" button, on the top left corner of the Google Cloud console (three parallel horizontal bars). Then click "Billing".

- You should now see the billing overview. Make sure that the billing account of the course (named "Deep machine learning") is selected at the top of the page.

- On the right of the page, under "Promotional credits", you should see your current balance of credits.

- To see your past consumption, click on "Reports" in the left-hand sidebar. Here there are various options for filtering, selecting time period, etc. By default, the checkbox "One time credits" on the right is checked, meaning that all you see is actual money spent, which will always be zero, since the cost is compensated for by the promotional credits we have received. Uncheck the box, and your consumed credits will be taken into account, which is what you want.

- Here are some (rough) estimates for the total amount of credits (per group) you should use for each part of the course
  - HA1: $6;
  - HA2: $6;
  - Project: $30 (can vary a lot depending on your project).
  
  That is, each person in the group should spend around $3 + $3 + $15 in total.
