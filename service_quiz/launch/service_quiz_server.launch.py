from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='service_quiz',
            executable='service_quiz_server',
            output='screen',

        ),
    ])