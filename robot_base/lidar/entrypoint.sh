#!/bin/bash
set -e

# Sourcer l'environnement ROS 2 Humble
source /opt/ros/humble/setup.bash

# Exécuter la commande passée en argument (CMD du Dockerfile ou command: du docker-compose)
exec "$@"