import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class ActuatorSubscriber(Node):
    """
    A ROS2 node that subscribes to Twist messages on the /cmd_vel topic and
    prints the received velocity commands to the console.
    """
    def __init__(self):
        super().__init__('actuator_subscriber')
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.listener_callback,
            10)
        self.get_logger().info("Actuator Subscriber node has been started.")

    def listener_callback(self, msg):
        """
        Callback for the /cmd_vel topic. Logs the received linear and angular velocities.
        """
        self.get_logger().info(f'Received Twist message: Linear=[{msg.linear.x}, {msg.linear.y}, {msg.linear.z}], Angular=[{msg.angular.x}, {msg.angular.y}, {msg.angular.z}]')

def main(args=None):
    rclpy.init(args=args)
    actuator_subscriber = ActuatorSubscriber()
    rclpy.spin(actuator_subscriber)
    actuator_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
