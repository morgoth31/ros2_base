# Utiliser l'image de base ROS 2 Humble
FROM osrf/ros:humble-ros-base

# Définir l'environnement de shell
SHELL ["/bin/bash", "-c"]

# Créer un répertoire de travail pour nos scripts
WORKDIR /app

# Copier les scripts Python dans le conteneur
COPY ./publisher_node.py .
COPY ./calculator_node.py .

# Rendre les scripts exécutables (bonne pratique)
RUN chmod +x ./publisher_node.py ./calculator_node.py