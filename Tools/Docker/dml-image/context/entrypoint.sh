#!/bin/bash

# From: https://denibertovic.com/posts/handling-permissions-with-docker-volumes/
# Add user to container matching the specified HOST_USER_ID of the host environment.
# Either use the HOST_USER_ID if passed in at runtime or fallback to 9001

USER_ID=${HOST_USER_ID:-9001}
GROUP_ID=${HOST_GROUP_ID:-9001}

echo "Starting with UID : $USER_ID, GID : $GROUP_ID"
id -u dml-guest >/dev/null 2>/dev/null && echo "User dml-guest already exists - deleting." && userdel -r dml-guest
echo "Creating user dml-guest."
groupadd -g $GROUP_ID -o dml-guest
useradd --shell /bin/bash -u $USER_ID -g dml-guest -o -m dml-guest
export HOME=/home/dml-guest

# Provide sudo rights to dml-guest, without requiring password
usermod -aG sudo dml-guest
echo 'dml-guest ALL=(ALL) NOPASSWD: ALL'>/etc/sudoers.d/dml-guest

# Setup conda environment (which is installed for the proxy "condauser")
ln -s /home/condauser/.conda /home/dml-guest/.conda
/usr/local/bin/gosu dml-guest conda init bash>/dev/null
#/usr/local/bin/gosu dml-guest conda activate dml
echo conda activate dml >> /home/dml-guest/.bashrc

# Important to start a bash shell, with the -i (interactive) argument, in order to make sure .bashrc is sourced, and hence that conda env is activated.
# Write command to file. Ugly fix for weird issue, where desired command had to be wrapped in quotes in the "docker run" command
echo $@>/tmp/cmd.sh
chmod a+x /tmp/cmd.sh
exec /usr/local/bin/gosu dml-guest bash -i /tmp/cmd.sh
