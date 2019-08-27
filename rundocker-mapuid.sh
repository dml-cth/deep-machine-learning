#!/bin/sh
set -o errexit

# ==============================================================================
# Wrapper script for running the course Docker image in a UNIX host environment,
# such that the user ID inside container matches the one on the host, avoiding
# file permission issues.

# USAGE
# Just replace "docker run" with the path of this script
# ==============================================================================

docker run -e HOST_USER_ID=$(id -u) -e HOST_GROUP_ID=$(id -g) $@
