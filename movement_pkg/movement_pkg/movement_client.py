from custom_interface.srv import MyCustomServiceMessage
import rclpy
from rclpy.node import Node
import sys

class ClientAsync(Node):
    def __init__(self):
        super().__init__('movement_client')
        self.client= self.create_client(MyCustomServiceMessage,'movement')

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service note available, waiting again...')

        self.req = MyCustomServiceMessage.Request()

    def send_request(self):
        self.req.move= sys.argv[1]
        self.future = self.client.call_async(self.req)

def main(args=None):
    rclpy.init(args=args)
    client=ClientAsync()
    client.send_request()

    while rclpy.ok():
        rclpy.spin_once(client)
        if client.future.done():
            try:
                response=client.future.result()
            except Exception as e:
                client.get_logger().info(f'Response state {response.success}')

            else:
                client.get_logger().info(
                    f'Response state {response.success}'
                )
            break

    client.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()