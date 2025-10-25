import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Quaternion
import math

class MarkerPublisherNode(Node):
    def __init__(self):
        super().__init__('marker_publisher')
        self.publisher_ = self.create_publisher(Marker, 'hello_marker', 10)
        self.timer = self.create_timer(1.0, self.timer_callback) # 1 Hz
        self.get_logger().info('Marker Publisher Node started.')

    def timer_callback(self):
        marker = Marker()
        
        # --- Entête ---
        marker.header.frame_id = "base_link" # Le repère de référence
        marker.header.stamp = self.get_clock().now().to_msg()
        
        # --- Identification ---
        marker.ns = "hello_world"
        marker.id = 0 # ID unique pour ce marqueur
        
        # --- Type et Action ---
        marker.type = Marker.CUBE
        marker.action = Marker.ADD # Ajouter ou modifier le marqueur
        
        # --- Position et Orientation ---
        marker.pose.position.x = 0.5
        marker.pose.position.y = 0.0
        marker.pose.position.z = 0.0
        marker.pose.orientation = self.euler_to_quaternion(0.0, 0.0, 0.785) # Rotation 45 deg Z

        # --- Échelle (1m x 1m x 1m) ---
        marker.scale.x = 0.5
        marker.scale.y = 0.5
        marker.scale.z = 0.5
        
        # --- Couleur (Vert, non-transparent) ---
        marker.color.a = 1.0 # Alpha (opacité)
        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        
        # --- Durée de vie (0 = infini) ---
        marker.lifetime = rclpy.duration.Duration(seconds=2).to_msg()

        # Publication
        self.publisher_.publish(marker)
        self.get_logger().info('Publishing a green cube...')

    def euler_to_quaternion(self, roll, pitch, yaw):
        """ Convertit les angles d'Euler en Quaternion. """
        q = Quaternion()
        q.x = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        q.y = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
        q.z = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        q.w = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        return q


def main(args=None):
    rclpy.init(args=args)
    node = MarkerPublisherNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()