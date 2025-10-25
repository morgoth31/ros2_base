import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException 
from geometry_msgs.msg import Point
import time

class CoordinatePublisher(Node):
    def __init__(self):
        super().__init__('coordinate_publisher')
        self.publisher_ = self.create_publisher(Point, 'coordinates', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.x = 1.0
        self.y = 2.0
        self.get_logger().info('Publisher node started (ROS_DOMAIN_ID=99). Publishing to "coordinates"...')

    def timer_callback(self):
        msg = Point()
        msg.x = self.x
        msg.y = self.y
        msg.z = 0.0  # Non utilisé
        
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: [x: {msg.x}, y: {msg.y}]')
        
        # Mettre à jour les valeurs pour la prochaine publication
        self.x += 0.5
        self.y -= 0.5
        if self.x > 10.0:
            self.x = 1.0
        if self.y < -10.0:
            self.y = 2.0

def main(args=None):
    rclpy.init(args=args)
    
    # Créez votre nœud
    node = CoordinatePublisher() 

    try:
        # Fait tourner le nœud jusqu'à ce qu'il soit arrêté
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass  # L'utilisateur a pressé Ctrl+C
    except ExternalShutdownException:
        pass  # Docker/Compose a envoyé un signal d'arrêt (SIGTERM)
    finally:
        # Nettoie *seulement si* rclpy est toujours actif
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()
if __name__ == '__main__':
    main()