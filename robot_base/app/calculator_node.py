import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException # <-- Importez ceci
from geometry_msgs.msg import Point
from std_msgs.msg import Float64
import time

# --- Importations QoS nécessaires ---
from rclpy.qos import QoSProfile, ReliabilityPolicy

class CalculatorNode(Node):
    def __init__(self):
        super().__init__('calculator_node')

        # --- Définir un profil QoS fiable ---
        # Doit correspondre à la fiabilité du publisher
        reliable_qos_profile = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE
        )
        
        # --- Utiliser le profil QoS dans la souscription ---
        self.subscription = self.create_subscription(
            Point,
            'coordinates',
            self.listener_callback,
            reliable_qos_profile  # <-- Remplacer '10' par le profil
        )
        
        self.publisher_ = self.create_publisher(Float64, 'dot_product', 10)
        self.get_logger().info('Calculator node started (ROS_DOMAIN_ID=99). Ready.')

    def listener_callback(self, msg):
        self.get_logger().info(f'Received: [x: {msg.x}, y: {msg.y}]')
        
        # Calculer le produit scalaire (norme au carré)
        dot_product_value = (msg.x * msg.x) + (msg.y * msg.y)
        
        # Préparer et publier le message de résultat
        dot_product_msg = Float64()
        dot_product_msg.data = dot_product_value
        self.publisher_.publish(dot_product_msg)
        
        self.get_logger().info(f'Publishing dot product: {dot_product_value}')

def main(args=None):
    rclpy.init(args=args)
    
    node = CalculatorNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except ExternalShutdownException:
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()

if __name__ == '__main__':
    main()