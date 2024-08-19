import rclpy
from rclpy.node import Node
from rclpy.qos import ReliabilityPolicy, QoSProfile
from service_quiz_interfaces.srv import Turn
from geometry_msgs.msg import Twist
import time

class ServiceServer(Node):
    def __init__(self):
        super().__init__('service_quiz_server')
        self.srv= self.create_service(Turn, 'turn',self.turn_callback)
        self.publisher_=self.create_publisher(Twist,'cmd_vel',10)
        self.cmd =Twist()
        self.turn_time = 10.0

    def stop_motion(self):
        self.get_logger().warn("Motion Stop!")
        self.cmd.linear.x=0.0
        self.cmd.angular.z=0.0
        self.publisher_.publish(self.cmd)

    def turn_right_motion(self,request):
        self.cmd.linear.x=0.0
        self.cmd.angular.z=-(request.angular_velocity)
        for i in range(request.time):
            self.get_logger().warn("Turn Right move move!")
            self.get_logger().info(f"time_sec=={i} seconds")
            self.publisher_.publish(self.cmd)
            time.sleep(1)

        self.stop_motion()

    def turn_left_motion(self,request):
        
        self.cmd.linear.x=0.0
        self.cmd.angular.z=(request.angular_velocity)
        for i in range(request.time):
            self.get_logger().warn("Turn Left move move!")
            self.get_logger().info(f"time_sec=={i} seconds")
            self.publisher_.publish(self.cmd)
            time.sleep(1)

        self.stop_motion()


    def turn_callback(self, request, response):
        if request.direction== 'right':
            self.turn_right_motion(request)
            response.success = True
        elif request.direction== 'left':
            self.turn_left_motion(request)
            response.success = True
        else:
            self.get_logger().error('Invalid Dierection')
            response.success = False

        return response

def main(args=None):
    rclpy.init(args=args)
    service_quiz_server = ServiceServer()
    rclpy.spin(service_quiz_server)
    rclpy.shutdown()

if __name__=='__main__':
    main()





