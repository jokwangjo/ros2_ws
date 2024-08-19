import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class SimplePublisher(Node):
    def __init__(self):
        super().__init__('simple_publisher')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)#10은 메세지의 최대 갯수구나
        time_period= 0.5
        self.timer= self.create_timer(time_period,self.timer_callback)

    def timer_callback(self):
        msg= Twist()
        msg.linear.x=0.0
        msg.angular.z=0.0
        
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg)

def main(args=None):
    rclpy.init(args=args)
    simple_publisher = SimplePublisher()
    rclpy.spin(simple_publisher)
    simple_publisher.destroy_node()
    rclpy.shutdown()

if __name__== '__main__':
    main()

