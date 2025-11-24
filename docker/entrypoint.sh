#!/bin/sh
set -e

echo "Starting RPM Tracker"

# Execute the main Python script
exec python3 main.py

# DEBUG
#ls -la /etc/yum.repos.d/
#dnf repolist enabled
#dnf list available
