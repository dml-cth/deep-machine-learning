# Prompts user for password, and prints a hash of it

from notebook.auth import passwd

hash = passwd()
print(hash)
