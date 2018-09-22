# Instructions for using Jupyter Notebooks in the cloud

- Connect to your instance, change to the `student` user, and activate the `dml_gpu` environment.

- Start a Jupyter server with the command:

  ```bash
  jupyter notebook
  ```

  This will print some information to the terminal, including a string looking something like this: `        http://(gpu-instance or 127.0.0.1):7000/?token=6d0810daf275a4a15c1237f8f44657ace6036d68de27609e`. The part after `token=` is the authentication token you will need to connect to your Jupyter server from you local machine (in this case it's `6d0810daf275a4a15c1237f8f44657ace6036d68de27609e`).

- Now take a look at the VM instances web page in the Google Cloud's console. There, in the same line where you see the name of your instance, you will also see its external IP. For instance, something like 35.255.15.79.

- Open a new browser window in your local machine and navigate to the address `http://<external_ip>:7000`, where `external_ip` is the IP address you obtained in the previous step. For instance, in my case I would connect to `http://35.255.15.79:7000`.

- If all of the steps above have been followed correctly, you will now see a web page asking you for the authentication token you obtained when starting the Jupyter server. In my case, that was `6d0810daf275a4a15c1237f8f44657ace6036d68de27609e`, so I input that and press "Log in".

- You are now connected to your Jupyter server running in the Google Cloud's instance.



### Tips

- You can use the Jupyter web interface to upload files to your instance (for example, Python notebooks you have developed when working in your local computer, or datasets that you'll use to train on the Cloud). To do so, simply click the button "Upload" on the top of the Jupyter web interface (to the right of the text "Select items to perform actions on them.", and to the left of the "New" button).

- Instead of using an authentication token, you can specify a password for logging in more easily with the command:

  ```bash
  jupyter notebook password		
  ```
