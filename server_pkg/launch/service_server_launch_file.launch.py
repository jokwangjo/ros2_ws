from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='server_pkg',
            executable='service_server',
            output='screen'
        ),
    ])