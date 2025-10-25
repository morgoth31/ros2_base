#!/bin/bash
# Permet aux conteneurs Docker d'accéder au serveur X de l'hôte
xhost +local:docker

# Fichier: .env
# Récupère automatiquement l'UID et le GID de l'utilisateur qui lance la commande
UID=$(id -u)
GID=$(id -g)

docker container kill ros_humble_desktop

docker compose up -d

docker exec -it ros_humble_desktop bash -c "source /opt/ros/humble/setup.bash && rviz2"

#source /opt/ros/humble/setup.bash

#rviz2