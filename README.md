# ROS2 Robot Simulator with Docker Compose

This project provides a complete, self-contained, and runnable example of a ROS2 architecture using Docker Compose. It simulates a robot and a control station, demonstrating a common robotics development setup.

## Architecture

The project consists of two services defined in `docker-compose.yml`:

-   `robot_simulator`: This service runs a ROS2 package that simulates a robot's sensors and actuators. It includes two Python nodes:
    -   `sensor_publisher`: Publishes `sensor_msgs/msg/LaserScan` messages to the `/scan` topic, `nav_msgs/msg/Odometry` messages to the `/odom` topic, and the `odom` to `base_link` transform.
    -   `actuator_subscriber`: Subscribes to `geometry_msgs/msg/Twist` messages on the `/cmd_vel` topic and prints the received velocity commands to the service log.
-   `station_control`: This service runs RViz2, a 3D visualization tool for ROS. It is configured to connect to the `robot_simulator` service and display the sensor data.

## File Structure

```
.
├── docker-compose.yml
├── robot_simulator
│   ├── Dockerfile
│   ├── launch
│   │   └── robot.launch.py
│   ├── package.xml
│   ├── robot_simulator
│   │   ├── actuator_subscriber.py
│   │   ├── __init__.py
│   │   └── sensor_publisher.py
│   ├── resource
│   │   └── robot_simulator
│   └── setup.py
├── station_control
│   └── config.rviz
└── README.md
```

## Prerequisites

-   Docker
-   Docker Compose
-   An X11 server running on your host machine (e.g., XQuartz on macOS, VcXsrv on Windows, or a standard X.Org server on Linux).

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Allow local connections to the X11 server:**
    This step is necessary to allow the Docker container to display the RViz GUI on your host machine.
    ```bash
    xhost +local:docker
    ```
    If you get `docker: unable to open display`, you might need to find your machine's IP address and run `xhost +<ip-address>`.

## Running the Application

1.  **Build and run the services:**
    ```bash
    docker-compose up --build
    ```
    This command will build the `robot_simulator` image and then start both the `robot_simulator` and `station_control` services.

2.  **Verify the output:**
    -   You should see the RViz2 GUI appear on your host machine.
    -   In RViz2, you should see:
        -   A laser scan visualization from the `/scan` topic.
        -   The robot's pose (as an arrow) from the `/odom` topic.
        -   The `odom` and `base_link` frames in the TF display.
    -   In the terminal where you ran `docker-compose up`, you will see the logs from both services. The `actuator_subscriber` will print any messages it receives on the `/cmd_vel` topic.

3.  **Send a command to the robot (optional):**
    Open a new terminal and run the following command to send a velocity command to the robot:
    ```bash
    docker-compose exec robot_simulator bash -c "source /ros2_ws/install/setup.bash && ros2 topic pub /cmd_vel geometry_msgs/msg/Twist '{linear: {x: 0.5, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.5}}' -1"
    ```
    You should see the `actuator_subscriber` log the received message, and the robot's pose will update in RViz.

## Stopping the Application

To stop the services, press `Ctrl+C` in the terminal where you ran `docker-compose up`. To remove the containers and network, run:
```bash
docker-compose down
```
