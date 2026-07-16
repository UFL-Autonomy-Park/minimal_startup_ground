import launch_ros.actions
import os
import yaml
import pathlib
import launch.actions
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

def generate_launch_description():
    file_path = os.path.expanduser("~/robot_param.yaml")
    with open(file_path, "r") as stream:
        try:
            data_loaded = yaml.safe_load(stream)
            robot_namespace = '/'+ data_loaded['robot_namespace']
            robot_prefix = data_loaded['robot_namespace']
            base_link = robot_prefix + '/base_link'
            navsat_link = robot_prefix + '/navsat_link'
            imu_link = robot_prefix + '/imu_0_link'
        except yaml.YAMLError as exc:
            print(exc)

    return LaunchDescription([
    launch_ros.actions.Node(
            package='tf2_ros',
            namespace=robot_namespace,
            executable='static_transform_publisher',
            name='static_navsat_tf_publisher',
            arguments=["0.0","0.0","0.2","0.0","0.0","0.0", base_link, navsat_link],
            parameters=[],
#            remappings=[('/tf', 'tf'),
#                        ('/tf_static', 'tf_static'),
#                        ('/diagnostics', 'diagnostics'),
#                        ],
           ),
    launch_ros.actions.Node(
        package='tf2_ros',
        namespace=robot_namespace,
        executable='static_transform_publisher',
        name='static_imu_tf_publisher',
        arguments=["0.1","0.0","0.2","0.0","0.0","0.0", base_link, imu_link],
        #arguments=["0.0","0.0","0.0","0.602196554855","0.0","0.0", base_link, imu_link],
        parameters=[],
#        remappings=[('/tf', 'tf'),
#                    ('/tf_static', 'tf_static'),
#                    ('/diagnostics', 'diagnostics'),
#                    ],
       ),
    launch_ros.actions.Node(
        package='tf2_ros',
        namespace=robot_namespace,
        executable='static_transform_publisher',
        name='static_park_tf_publisher',
        #arguments=["-368305.0700699703","-3278357.100811787","-0.6021965548550632","0.0","0.0", "utm", "autonomy_park"],
        arguments=["368305.0700699703","3278357.100811787","0.0", "0.0","0.0","0.0", "utm", "autonomy_park"],
        parameters=[],
#        remappings=[('/tf', 'tf'),
#                    ('/tf_static', 'tf_static'),
#                    ('/diagnostics', 'diagnostics'),],
        ),
])
