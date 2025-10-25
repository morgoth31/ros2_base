from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    """
    Generates a LaunchDescription to start the sensor_publisher and actuator_subscriber nodes.
    """
    return LaunchDescription([
        Node(
            package='robot_simulator',
            executable='sensor_publisher',
            name='sensor_publisher',
            output='screen'
        ),
        Node(
            package='robot_simulator',
            executable='actuator_subscriber',
            name='actuator_subscriber',
            output='screen'
        ),
    ])
