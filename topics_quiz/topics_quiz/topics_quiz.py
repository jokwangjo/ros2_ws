import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from rclpy.qos import ReliabilityPolicy, QoSProfile
from nav_msgs.msg import Odometry
import numpy as np


class Exercise(Node):
    def __init__(self):
        super().__init__('topic_exercise_node')
        self.publisher_=self.create_publisher(Twist, 'cmd_vel',10)
        self.subscriber = self.create_subscription(LaserScan, '/scan',self.laser_callback,QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE))
        self.odom_subscriber = self.create_subscription(Odometry, '/odom',self.odom_callback,QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE))
        self.timer_period= 0.5
        self.laser_forward =0 
        self.laser_right=0
        self.laser_left=0
        self.current_roll=0.0
        self.current_pitch=0.0
        self.current_yaw =0.0
        self.postive_current_yaw= 0.0
        self.target_yaw= self.current_yaw
        self.cmd = Twist()
        self.timer= self.create_timer(self.timer_period, self.motion)

        #cmd cycle
        self.turn_cmd_cycle_req=False
        self.sequence_no=0


    def laser_callback(self, msg):
        self.laser_forward= msg.ranges[0]
        self.laser_left=msg.ranges[90]
        self.laser_right=msg.ranges[270]

    def odom_callback(self, msg):
        orientation_q= msg.pose.pose.orientation
        quaternion=[orientation_q.x,orientation_q.y,orientation_q.z,orientation_q.w]
        self.current_roll,self.current_pitch, self.current_yaw = self.euler_from_quaternion(quaternion)

    def msg_cmd_forward(self):
        self.cmd.linear.x=0.5
        self.cmd.angular.z=0.0
    def msg_cmd_turn(self):
        self.cmd.linear.x=0.0
        self.cmd.angular.z=0.2
        self.turn_cmd_cycle_req=True
    def msg_cmd_stop(self):
        self.cmd.linear.x=0.0
        self.cmd.angular.z=0.0

    def turn_req_check(self,yaw_error):
        if abs(yaw_error) >0.1:
            result= True
            self.get_logger().info('turn req!!!!!!!!!!!!!!!!!!!')
        else:
            result= False

        return result

    def forward_req_check(self, range):
        if self.laser_forward > range:
            result= True
        else:
            result= False

        return result
    
    def left_inf_check(self):
        if self.laser_left==float('inf'):
            result= True
            self.get_logger().info('left inf!!!!!!!!!!!!!!!!!!!')
        else:
            result= False
        return result



    def update_target_yaw(self):
        # 현재 yaw 값에 90도 (π/2 라디안) 추가
        self.target_yaw = (self.current_yaw + np.pi / 4) % (2*np.pi)
        
        self.get_logger().info(f'New Target Yaw: {self.target_yaw}')

    def postive_current_yau_calc(self):
        if self.current_yaw<0:
            postive_current_yaw=(np.pi+self.current_yaw)+np.pi
        if self.current_yaw>=0:
            postive_current_yaw=self.current_yaw
        return postive_current_yaw

    def motion(self):
        self.postive_current_yaw= self.postive_current_yau_calc()
        self.get_logger().info(f'laser forward: {self.laser_forward}, laser left:{self.laser_left},laser right: {self.laser_right}')
        self.get_logger().info('I receive turn req: "%s"' % str(self.turn_cmd_cycle_req))
        self.get_logger().info(f'Postive_Current Yaw:{self.postive_current_yaw},Target yaw:{self.target_yaw}') 
        self.get_logger().info(f'Current Yaw:{self.current_yaw}') 
        yaw_error= self.target_yaw-self.postive_current_yaw

        if self.sequence_no==0:
            self.get_logger().info(f"step no:{self.sequence_no}")
            #self.msg_cmd_stop()
            if self.turn_req_check(yaw_error) :
                self.sequence_no=10
            else:
                if self.forward_req_check(3):
                    self.sequence_no=5
                else:
                    self.sequence_no=10

        elif self.sequence_no==5:
            self.get_logger().info(f"step no:{self.sequence_no}")
            self.msg_cmd_forward()
            if not self.forward_req_check(3):
                self.sequence_no=0

        elif self.sequence_no==10:
            self.get_logger().info(f"step no:{self.sequence_no}")
            if not self.turn_cmd_cycle_req:
                self.update_target_yaw()
            self.msg_cmd_turn()
            if not self.turn_req_check(yaw_error):
                self.sequence_no=0
                self.turn_cmd_cycle_req=False

        self.publisher_.publish(self.cmd)
        self.get_logger().info(f'yaw_error:{yaw_error}')


    def euler_from_quaternion(self, quaternion):
        x= quaternion[0]
        y= quaternion[1]
        z= quaternion[2]
        w= quaternion[3]

        sinr_cosp= 2*(w*x+ y*z)
        cosr_cosp= 1- 2*(x*x+y*y)
        roll = np.arctan2(sinr_cosp, cosr_cosp)

        sinp= 2*(w*y-z*x)
        pitch = np.arcsin(sinp)

        siny_cosp= 2*(w*z+x*y)
        cosy_cosp= 1-2*(y*y+z*z)
        yaw= np.arctan2(siny_cosp, cosy_cosp)

        return roll,pitch,yaw
    
    def quanternion(self, target_axis, target_angle):
        axis= target_axis
        angle= np.pi/(180/target_angle)

        w= np.cos(angle/2)
        x= axis[0]*np.sin(angle/2)
        y= axis[1]*np.sin(angle/2)
        z= axis[2]*np.sin(angle/2)

        quanternion=[x,y,z,w]

        return self.euler_from_quaternion(quanternion)




def main(args=None):
    rclpy.init(args=args)
    exercise_node= Exercise()
    rclpy.spin(exercise_node)
    exercise_node.destroy_node()
    rclpy.shutdown()

if __name__== '__main__':
    main()