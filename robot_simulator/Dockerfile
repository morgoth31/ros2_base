# Use the ROS2 Humble base image
FROM ros:humble-ros-base

# Set the working directory
WORKDIR /ros2_ws

# Copy the robot_simulator package into the workspace
COPY ./robot_simulator /ros2_ws/src/robot_simulator

# Install dependencies and build the workspace
RUN . /opt/ros/humble/setup.sh && \
    apt-get update && \
    rosdep install -i --from-path src --rosdistro humble -y && \
    colcon build --packages-select robot_simulator

# Set up the entrypoint to source the workspace and run the launch file
CMD ["/bin/bash", "-c", "source /ros2_ws/install/setup.bash && ros2 launch robot_simulator robot.launch.py"]
