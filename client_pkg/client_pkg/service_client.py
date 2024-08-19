from std_srvs.srv import Empty
import rclpy
from rclpy.node import Node

class ClientAsync(Node):
    def __init__(self):
        super().__init__('service_client')
        self.client= self.create_client(Empty, 'moving')
        while not self.client.wait_for_service(timeout_sec=1.0):#클라이언트 서비스 대기 시간 1초주기로 시도
            self.get_logger().info('service not availabe, waiting again...')

        self.req= Empty.Request()#채울게 없더라도 뚫어 놓는 역할.

    def send_request(self):
        self.future = self.client.call_async(self.req)#응답을 접근하기 위한 변수.

def main(args=None):
    rclpy.init(args=args)
    client=ClientAsync()
    client.send_request()

    while rclpy.ok():
        rclpy.spin_once(client)#콜백을 하면서 동시동작을 하기위해선 spin_once쓰면됨.
        if client.future.done():#service request 받았는지 확인.
            try:
                response = client.future.result()#결과 확인.Type자체가 Empty라서 암것도 없음.

            except Exception as e:
                client.get_logger().info(
                    'the robot is moving'
                )
            else:
                client.get_logger().info(
                    'the robot is moving'
                )
            break
        #do something async시 동시 동작 추가 가능.

    client.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()

