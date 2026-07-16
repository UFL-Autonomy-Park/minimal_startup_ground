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
            frame_prefix = data_loaded['robot_namespace']
            base_link_id = frame_prefix + '/base_link'
            odom_frame_id = frame_prefix + '/odom'
            navsat_link_id = frame_prefix + '/navsat_link'
            robot_namespace = '/'+ data_loaded['robot_namespace']
        except yaml.YAMLError as exc:
            print(exc)

    setup_path = LaunchConfiguration('setup_path')

    arg_setup_path = DeclareLaunchArgument('setup_path', default_value='/home/autonomypark/platform_ws/src/common/minimal_startup/')

    arg_output_final_position = DeclareLaunchArgument(
        'output_final_position',
        default_value='false')

    arg_output_file = DeclareLaunchArgument(
        'output_location',
    default_value='~/dual_ekf_navsat_debug.txt')

    dir_params = PathJoinSubstitution([
        setup_path, 'params'])

    config_localization = [
        dir_params,
        '/dual_ekf_navsat.yaml'
    ]

    return LaunchDescription([
    arg_output_file,
    arg_output_final_position,
    arg_setup_path,
    launch_ros.actions.Node(
            package='robot_localization',
            namespace=robot_namespace,
            executable='ekf_node',
            name='ekf_local',
            output='screen',
            parameters=[{"frequency": 30.0},
                        {"sensor_timeout": 0.5},
                        {"two_d_mode": True},
                        {"transform_time_offset": 0.0},
                        {"transform_timeout": 0.0},
                        {"print_diagnostics": True},
                        #{"debug": False},
                        {"map_frame": 'autonomy_park'},
                        {"odom_frame": odom_frame_id},
                        {"base_link_frame": base_link_id},
                        {"world_frame": odom_frame_id},
                        {"publish_tf" : True},
                        {"odom0": 'platform/odometry'},
                        {"odom0_config": [False, False, False,
                                          False, False, False,
                                          True,  True,  False,
                                          False, False, True,
                                          False, False, False]},
                        {"odom0_differential": False},
                        {"odom0_relative": False},
                        {"odom0_queue_size": 10},
                        {"imu0": 'sensors/imu_0/data'},
                        {"imu0_config": [False, False, False,
                                         True,  True,  True,
                                         False, False, False,
                                         True,  True,  True,
                                         True,  True,  True]},
                        {"imu0_differential": False},
                        {"imu0_relative": False},
                        {"imu0_queue_size": 10},
                        {"imu0_remove_gravitational_acceleration": True},
                        {"use_control": False},
                        #{"process_noise_covariance": [1e-3, 1e-3, 1e-3, 0.3, 0.3, 0.01, 0.5, 0.5, 0.1, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]},
                        #{"initial_estimate_covariance": [1e-9, 1e-9, 1e-9, 1.0, 1.0, 1e-9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]},
                        ],
            remappings=[
                        #('/tf', 'tf'),
                        #('/tf_static', 'tf_static'),
                        #('/diagnostics', 'diagnostics'),
                        #('imu', 'sensors/imu_0/data'),
                        #('odom', ''),
                        ('odometry/filtered', 'odometry/local'),
                        ]
           ),
])
