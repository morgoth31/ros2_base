import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped, Twist
from tf2_ros import TransformBroadcaster
import numpy as np
import math

class SensorPublisher(Node):
    """
    A ROS2 node that simulates sensor data from a robot.
    It publishes LaserScan and Odometry messages, and broadcasts the odom to base_link transform.
    """
    def __init__(self):
        super().__init__('sensor_publisher')

        # Publishers for LaserScan and Odometry
        self.scan_publisher = self.create_publisher(LaserScan, 'scan', 10)
        self.odom_publisher = self.create_publisher(Odometry, 'odom', 10)

        # Transform broadcaster for odom -> base_link
        self.tf_broadcaster = TransformBroadcaster(self)

        # Timers to publish data at regular intervals
        self.scan_timer = self.create_timer(0.1, self.publish_scan)  # 10 Hz
        self.odom_timer = self.create_timer(0.05, self.publish_odom)  # 20 Hz

        # Robot state variables
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        # Subscription to velocity commands to update odometry
        self.cmd_vel_subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            10)

        self.get_logger().info("Sensor Publisher node has been started.")

    def cmd_vel_callback(self, msg):
        """
        Callback for the /cmd_vel topic. Updates the robot's pose based on velocity commands.
        """
        # Update robot's pose based on received velocity commands
        dt = 0.05  # Time step, should match the odom timer period
        self.x += (msg.linear.x * math.cos(self.theta) - msg.linear.y * math.sin(self.theta)) * dt
        self.y += (msg.linear.x * math.sin(self.theta) + msg.linear.y * math.cos(self.theta)) * dt
        self.theta += msg.angular.z * dt

    def publish_scan(self):
        """
        Publishes a simulated LaserScan message.
        """
        scan_msg = LaserScan()
        now = self.get_clock().now().to_msg()
        scan_msg.header.stamp = now
        scan_msg.header.frame_id = 'base_link'

        scan_msg.angle_min = -math.pi
        scan_msg.angle_max = math.pi
        scan_msg.angle_increment = math.pi / 180.0
        scan_msg.time_increment = (1.0 / 10.0) / 360.0
        scan_msg.range_min = 0.1
        scan_msg.range_max = 10.0

        num_readings = 360
        scan_msg.ranges = [float(i % 10) for i in range(num_readings)]

        self.scan_publisher.publish(scan_msg)

    def publish_odom(self):
        """
        Publishes a simulated Odometry message and broadcasts the odom->base_link transform.
        """
        now = self.get_clock().now().to_msg()

        # Create and publish the odometry message
        odom_msg = Odometry()
        odom_msg.header.stamp = now
        odom_msg.header.frame_id = 'odom'
        odom_msg.child_frame_id = 'base_link'

        odom_msg.pose.pose.position.x = self.x
        odom_msg.pose.pose.position.y = self.y
        odom_msg.pose.pose.position.z = 0.0

        # Convert yaw to quaternion
        q = self.get_quaternion_from_euler(0, 0, self.theta)
        odom_msg.pose.pose.orientation.x = q[0]
        odom_msg.pose.pose.orientation.y = q[1]
        odom_msg.pose.pose.orientation.z = q[2]
        odom_msg.pose.pose.orientation.w = q[3]

        self.odom_publisher.publish(odom_msg)

        # Create and broadcast the transform
        t = TransformStamped()
        t.header.stamp = now
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_link'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        self.tf_broadcaster.sendTransform(t)

    def get_quaternion_from_euler(self, roll, pitch, yaw):
        """
        Converts Euler angles to a quaternion.
        """
        cy = math.cos(yaw * 0.5)
        sy = math.sin(yaw * 0.5)
        cp = math.cos(pitch * 0.5)
        sp = math.sin(pitch * 0.5)
        cr = math.cos(roll * 0.5)
        sr = math.sin(roll * 0.5)

        q = [0.0] * 4
        q[0] = cy * cp * sr - sy * sp * cr  # x
        q[1] = sy * cp * sr + cy * sp * cr  # y
        q[2] = sy * cp * cr - cy * sp * sr  # z
        q[3] = cy * cp * cr + sy * sp * sr  # w
        return q

def main(args=None):
    rclpy.init(args=args)
    sensor_publisher = SensorPublisher()
    rclpy.spin(sensor_publisher)
    sensor_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
