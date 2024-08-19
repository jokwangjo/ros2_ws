import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from rclpy.qos import ReliabilityPolicy, QoSProfile

class SimpleSubscriber(Node):
    def __init__(self):
        super().__init__('simple_subscriber')
        self.subscriber= self.create_subscription(
            LaserScan, #메세지 타입
            '/scan', #토픽 이름
            self.listener_callback, #콜백함수
            QoSProfile(depth=10, reliability= ReliabilityPolicy.RELIABLE)#TCP방식
            #depth는 메세지 축적 가능 갯수, 설정 갯수 초과시 먼저 쌓인 메세지가 지워지게 됨.
            #출력되는 메세지는 쌓여있는 메세지중 먼저 쌓인 메세지가 우선순위 선입선출.
            #BEST_EFFORT 즉, UDP방식이 있지만 이 방식은 메시지가 큐에 도달하기전에 손실이 발생할수 있음.
            #하지만 속도는 빠르다.
            # 이런 것을 QOS(Quality of Service)정책 또는 설정이라 한다. 
        )

    def listener_callback(self, msg):
        self.get_logger().info('I receive: "%s"' % str(msg))

def main(args=None):
    rclpy.init(args=args)
    simple_subscriber= SimpleSubscriber()
    rclpy.spin(simple_subscriber)
    simple_subscriber.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()