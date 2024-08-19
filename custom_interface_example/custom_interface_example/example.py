import rclpy
from rclpy.node import Node
from rclpy.qos import ReliabilityPolicy, QoSProfile
from custom_interface.msg import Age

class Example(Node):
    def __init__(self):
        super().__init__('custom_interface_example_node')
        self.publisher_=self.create_publisher(Age, 'age',10)
        self.age=Age()
        self.time_period=0.5
        self.timer= self.create_timer(self.time_period, self.timer_callback)

    def timer_callback(self):
        self.age.year=2031
        self.age.month=5
        self.age.day=21
        self.publisher_.publish(self.age)

def main(args=None):
    rclpy.init(args=args)
    example_node= Example()
    rclpy.spin(example_node)
    example_node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
