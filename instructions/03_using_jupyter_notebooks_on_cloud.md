# Instructions for using Jupyter Notebooks in the cloud
In the [01_environment_setup.md](01_environment_setup.md) instructions, you learned how to access Jupyter notebooks when working on your own computer. When working on a virtual machine in the cloud, the process is similar, but requires some extra manual steps. Be sure to have completed the Google Cloud guide [02_google_cloud_instructions.md](02_google_cloud_instructions.md) before proceeding.

- Select the correct "project" and start your virtual machine instance.

- Once it has started, determine the IP address of the virtual machine, which will be needed later.
  - The **External IP** should be clearly displayed in the list of virtual machine instances. In the example below, it is 34.123.45.90.
![Running instance](figs/gcp-running-vm-instance.png)

- Connect to your virtual machine instance by clicking **SSH** from the instance overview page, then activate the `dml` environment:
  ```bash
  conda activate dml
  ```

- If this is the first time you use Jupyter on this virtual machine, you should configure a password.

  **Note**: The security here is quite weak. The browser may (rightfully) warn for security issues. The realistic risk of a hacker attack is quite low, but nevertheless, **you should not upload sensitive data to your VM**. Also, **you should not use a password for the jupyter notebook that use use elsewhere**, as the security around the password transmission/storage is weak.

  Configure a password by running the following command:
  ```bash
  jupyter notebook password
  ```

- Now you can start a Jupyter server with the command:

  ```bash
  jupyter notebook
  ```

- The browser will not pop up automatically, like when you worked on your own computer. Instead, you need to navigate to the appropriate page automatically, for which you first need the external IP address of the virtual machine that you determined earlier.

- Open up your browser and navigate to e.g. `
http://52.183.118.98:8888`, but replace the IP address with the appropriate one.

- If all of the steps above have been followed correctly (and you set up your virtual machine correctly), you will now see a web page asking you to provide the password you created before starting the Jupyter server.
  - If the page is broken or is displayed incorrectly, make sure that you disable all your browser extensions and that the security settings for the webpage allows content to be viewed.

- You are now connected to your Jupyter server running in the Google Cloud's instance.

- When you are done working with it, go back to `SSH-in-browser`, stop Jupyter server with `ctrl`+`C`, and type `exit`. **Remember to stop the VM instance once you're done with training**. 

### Misc advice

- You can use the Jupyter web interface to upload files to your instance (for example, Python notebooks you have developed when working in your local computer or datasets that you'll use to train on the Cloud). To do so, simply click the button `Upload` on the top of the Jupyter web interface.

- You can also download data (e.g. trained network weights, images, etc) by right-clicking on a file in the file explorer view and select `Download`. This is one way to make back-ups of your work.

- If your `SSH-in-browser` is inactive for some time, it will ask you to authorize again. If it fails to re-authorize for some reason, you can just try it again. It should not interrupt your work in the Jupyter notebooks. 
