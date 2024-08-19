import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from rclpy.qos import ReliabilityPolicy, QoSProfile

class Exercise(Node):
    def __init__(self):
        super().__init__('topic_exercise_node')
        self.publisher_=self.create_publisher(Twist, 'cmd_vel',10)
        self.subscriber = self.create_subscription(LaserScan, '/scan',self.laser_callback,QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE))
        self.timer_period= 0.5
        self.laser_forward =0 #?
        self.cmd = Twist()
        self.timer= self.create_timer(self.timer_period, self.motion)


    def laser_callback(self, msg):
        self.laser_forward= msg.ranges[0]

    def motion(self):
        self.get_logger().info('I receive: "%s"' % str(self.laser_forward))
        if self.laser_forward>5:
            self.cmd.linear.x = 0.5
            self.cmd.angular.z = 0.5
        elif self.laser_forward < 5 and self.laser_forward>=0.5:
            self.cmd.linear.x = 0.2
            self.cmd.angular.z= 0.0
        else:
            self.cmd.linear.x= 0.0
            self.cmd.linear.z= 0.0

        self.publisher_.publish(self.cmd)

def main(args=None):
    rclpy.init(args=args)
    exercise_node= Exercise()
    rclpy.spin(exercise_node)
    exercise_node.destroy_node()
    rclpy.shutdown()

if __name__== '__main__':
    main()