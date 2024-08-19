from std_srvs.srv import Empty
import rclpy
from rclpy.node import Node

class ClientAsync(Node):
    def __init__(self):
        super().__init__('stop_client')
        self.client= self.create_client(Empty,'stop')

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not availabe, waiting again...')

        self.req=Empty.Request()

    def send_request(self):
        self.future= self.client.call_async(self.req)


def main(args=None):
    rclpy.init(args=args)
    client= ClientAsync()
    client.send_request()

    while rclpy.ok():
        rclpy.spin_once(client)
        if client.future.done():
            try:
                response= client.future.result()
            except Exception as e:
                client.get_logger().info(f'Service call failed{e}')
            else:#try의 예외 경우가 아닐 시 발생함.
                client.get_logger().info('the robot is stopped')
            break

    client.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()