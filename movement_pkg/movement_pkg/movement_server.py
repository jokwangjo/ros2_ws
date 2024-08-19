from geometry_msgs.msg import Twist
from custom_interface.srv import MyCustomServiceMessage
import rclpy
from rclpy.node import Node

class Service(Node):
    def __init__(self):
        super().__init__('movement_server')
        self.srv=self.create_service(MyCustomServiceMessage, 'movement',self.custom_service_callback)
        self.publisher_=self.create_publisher(Twist, 'cmd_vel', 10)

    def custom_service_callback(self,request, response):#server개념으로 만든 메서드라서 request, response필요
        msg= Twist()

        if request.move == "Turn Right":
            msg.linear.x=0.1
            msg.angular.z=-0.5
            self.publisher_.publish(msg)
            self.get_logger().info('Turning to right direction!!')
            response.success = True

        elif request.move == "Turn Left":
            msg.linear.x=0.1
            msg.angular.z=0.5
            self.publisher_.publish(msg)
            self.get_logger().info('Turning to left direction!!')
            response.success = True

        elif request.move == "Stop":
            msg.linear.x=0.0
            msg.angular.z=0.0
            self.publisher_.publish(msg)
            self.get_logger().info('Stop There!!')
            response.success = True

        else:
            response.success= False

        return response
    
def main(args=None):
    rclpy.init(args=args)
    service= Service()
    rclpy.spin(service)
    rclpy.shutdown()

if __name__=='__main__':
    main()






