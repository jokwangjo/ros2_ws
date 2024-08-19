import rclpy
from rclpy.node import Node
from rclpy.qos import ReliabilityPolicy, QoSProfile
from service_quiz_interfaces.srv import Turn
from geometry_msgs.msg import Twist
import time
import sys

class ServiceClient(Node):
    def __init__(self):
        super().__init__('service_quiz_client')
        self.client= self.create_client(Turn,'turn')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again..')

        self.req= Turn.Request()

    def send_request(self):#디폴트가 문자 인듯 각각에 대한 인스턴스에 대해서 자료형식 지정 필요.
        self.req.direction = sys.argv[1]
        self.req.angular_velocity= float(sys.argv[2])
        self.req.time = int(sys.argv[3])
        self.future = self.client.call_async(self.req)


def main(args= None):
    rclpy.init(args=args)
    client= ServiceClient()
    client.send_request()

    while rclpy.ok():
        rclpy.spin_once(client)
        if client.future.done():
            try:
                response = client.future.result()
            except Exception as e:
                client.get_logger().info(
                    f'Service call fail: {e}'
                )
            else:
                client.get_logger().info(
                    f'Response State: {response.success}'
                )
            break

    client.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
