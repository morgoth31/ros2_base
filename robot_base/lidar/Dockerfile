FROM ros:humble-ros-core

# Mettre à jour les paquets et installer le pilote YDLIDAR pour ROS 2 Humble
RUN apt-get update && apt-get install -y \
    ros-humble-ydlidar-ros-driver \
    && rm -rf /var/lib/apt/lists/*

# Copier le script entrypoint qui sourcera l'environnement ROS
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Définir l'entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Commande par défaut (peut être surchargée par docker-compose)
CMD ["ros2", "launch", "ydlidar_ros_driver", "ydlidar_launch.py"]