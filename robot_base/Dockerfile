# Utiliser l'image de base de ROS 2 Humble
FROM ros:humble-ros-base

# Définir l'environnement de shell
SHELL ["/bin/bash", "-c"]

# Mettre à jour les paquets et installer les dépendances
RUN apt-get update && apt-get install -y \
    python3-colcon-common-extensions \
    ros-humble-tf2-ros \
    # Nettoyage
    && rm -rf /var/lib/apt/lists/*

# Créer le workspace
WORKDIR /ros2_ws

# Copier notre code source du package
COPY src/ /ros2_ws/src/

# Builder le workspace
RUN . /opt/ros/humble/setup.bash && \
    colcon build --symlink-install

# Script d'entrée pour sourcer automatiquement l'overlay
COPY <<EOF /ros_entrypoint.sh
#!/bin/bash
set -e
source "/opt/ros/humble/setup.bash"
source "/ros2_ws/install/setup.bash"
exec "\$@"
EOF
RUN chmod +x /ros_entrypoint.sh

# Définir le point d'entrée
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]