#!/bin/sh
set -e

HASH_PATH=PASSWD_HASH.txt

# Search for existing password hash, or request new password
if [ -f $HASH_PATH ]; then
    # Note: grep command will fail if there are no matches, which will (intentionallly) also make the truth statement fail.
    if [ $(cat "$HASH_PATH" | grep -c sha1:) -eq "1" ]; then
        echo "Reusing password, hash found in $HASH_PATH"
    else
        echo "$HASH_PATH found, but could not parse contents. Please provide your desired password for accessing Jupyter Notebook server."
        hash=$(python /gen_passwd.py)
        # Will only write hash to file if above command succeeded:
        echo $hash > $HASH_PATH
    fi
else
    echo "No password hash found in $HASH_PATH. Please provide your desired password for accessing Jupyter Notebook server."
    hash=$(python /gen_passwd.py)
    # Will only write hash to file if above command succeeded:
    echo $hash > $HASH_PATH
fi

# Create temporary config file
echo "c.NotebookApp.password = u'"$(cat $HASH_PATH)"'" > /tmp/jupyter_notebook_config.py

# Start server
jupyter notebook --config /tmp/jupyter_notebook_config.py --ip 0.0.0.0 --no-browser
