# Instructions for using Jupyter Notebooks in the cloud
In the [01_environment_setup.md](01_environment_setup.md) instructions, you learned how to access Jupyter notebooks when working on your own computer. When working on a virtual machine in the cloud, the process is similar, but requires some extra manual steps. Be sure to have completed the guide [02_setting_up_azure.md](02_setting_up_azure.md) before proceeding.

- Start your virtual machine instance.

- Once it has started, determine the IP address of the virtual machine, which will be needed later. In the [Azure Portal](http://portal.azure.com/) click on the virtual machine you just started, and navigate to "Overview". Under "Networking" identify the Public IP address (e.g. 
52.183.118.98). Note that the IP might change every time you start up the instance.

- Connect to your virtual machine instance, and activate the `dml` environment.

- If this is the first time you use Jupyter on this virtual machine, configure a password by running the following command:

```bash
jupyter notebook password
```

- Now you can start a Jupyter server with the command:

  ```bash
  jupyter notebook
  ```

- The browser will not pop up automatically, like when you worked on your own computer. Instead, you need to navigate to the appropriate page automatically, for which you first need the IP address of the virtual machine that you determined earlier.

- Open up your browser and navigate to e.g. `
http://52.183.118.98:8888`, but replace the IP with the appropriate one.

- If all of the steps above have been followed correctly (and you set up your Azure machine correctly), you will now see a web page asking you to provide the password you created before starting the Jupyter server.

- You are now connected to your Jupyter server running in the Google Cloud's instance.

### Tips

- You can use the Jupyter web interface to upload files to your instance (for example, Python notebooks you have developed when working in your local computer, or datasets that you'll use to train on the Cloud). To do so, simply click the button "Upload" on the top of the Jupyter web interface (to the right of the text "Select items to perform actions on them.", and to the left of the "New" button).
