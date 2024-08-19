import rclpy
# import the Node module from ROS2 Python library
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('Miller')
        self.create_timer(0.2, self.timer_callback)

    def timer_callback(self):
        self.get_logger().info("Hello World")


def main(args=None):
    # initialize the ROS communication
    rclpy.init(args=args)# initialize the ROS communication
    node= MyNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main() # call the main function