import os
import pathlib

import launch.actions
import launch_ros.actions
import yaml
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node

from launch import LaunchDescription


def generate_launch_description():
    file_path = os.path.expanduser("~/robot_param.yaml")
    with open(file_path, "r") as stream:
        try:
            data_loaded = yaml.safe_load(stream)
            frame_prefix = data_loaded["robot_namespace"]
            base_link_id = frame_prefix + "/base_link"
            odom_frame_id = frame_prefix + "/odom"
            navsat_link_id = frame_prefix + "/navsat_link"
            map_frame_id = frame_prefix + "/map"
            robot_namespace = "/" + data_loaded["robot_namespace"]
        except yaml.YAMLError as exc:
            print(exc)

    setup_path = LaunchConfiguration("setup_path")

    arg_setup_path = DeclareLaunchArgument(
        "setup_path",
        default_value="/home/autonomypark/platform_ws/src/common/minimal_startup_ground/",
    )

    arg_output_final_position = DeclareLaunchArgument(
        "output_final_position", default_value="false"
    )

    arg_output_file = DeclareLaunchArgument(
        "output_location", default_value="~/dual_ekf_navsat_debug.txt"
    )

    dir_params = PathJoinSubstitution([setup_path, "params"])

    config_localization = [dir_params, "/dual_ekf_navsat_test.yaml"]

    return LaunchDescription(
        [
            arg_output_file,
            arg_output_final_position,
            arg_setup_path,
            launch_ros.actions.Node(
                package="robot_localization",
                namespace=robot_namespace,
                executable="ekf_node",
                name="ekf_local",
                output="screen",
                parameters=[
                    {"frequency": 30.0},
                    {"sensor_timeout": 0.1},
                    {"two_d_mode": True},
                    {"transform_time_offset": 0.0},
                    {"transform_timeout": 0.0},
                    {"print_diagnostics": True},
                    # {"debug": False},
                    {"map_frame": map_frame_id},
                    {"odom_frame": odom_frame_id},
                    {"base_link_frame": base_link_id},
                    {"world_frame": odom_frame_id},
                    {"publish_tf": True},
                    {"odom0": "platform/odometry"},
                    {
                        "odom0_config": [
                            True,
                            True,
                            True,
                            False,
                            False,
                            False,
                            True,
                            True,
                            True,
                            False,
                            False,
                            True,
                            False,
                            False,
                            False,
                        ]
                    },
                    {"odom0_differential": False},
                    {"odom0_relative": True},
                    {"odom0_queue_size": 10},
                    {"nodelay": False},
                    {"imu0": "sensors/imu_0/data"},
                    {
                        "imu0_config": [
                            False,
                            False,
                            False,
                            False,
                            False,
                            True,
                            False,
                            False,
                            False,
                            False,
                            False,
                            True,
                            False,
                            False,
                            False,
                        ]
                    },
                    {"imu0_differential": False},
                    {"imu0_relative": True},
                    {"imu0_queue_size": 10},
                    {"imu0_pose_rejection_threshold": 0.8},
                    {"imu0_twist_rejection_threshold": 5.0},
                    {"imu0_linear_acceleration_rejection_threshold": 0.8},
                    {"imu0_remove_gravitational_acceleration": True},
                    {"use_control": False},
                    {"control_config": [True, True, False, False, False, True]},
                    # {"process_noise_covariance": [1e-3, 1e-3, 1e-3, 0.3, 0.3, 0.01, 0.5, 0.5, 0.1, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]},
                    # {"initial_estimate_covariance": [1e-9, 1e-9, 1e-9, 1.0, 1.0, 1e-9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]},
                ],
                remappings=[
                    # ('/tf', 'tf'),
                    # ('/tf_static', 'tf_static'),
                    # ('/diagnostics', 'diagnostics'),
                    # ('imu', 'sensors/imu_0/data'),
                    # ('odom', ''),
                    ("odometry/filtered", "odometry/local"),
                ],
            ),
            launch_ros.actions.Node(
                package="robot_localization",
                namespace=robot_namespace,
                executable="ekf_node",
                name="ekf_global",
                output="screen",
                parameters=[
                    {"frequency": 50.0},
                    {"sensor_timeout": 0.5},
                    {"two_d_mode": True},
                    {"transform_time_offset": 0.0},
                    {"transform_timeout": 0.0},
                    {"print_diagnostics": True},
                    {"debug": False},
                    {"map_frame": map_frame_id},
                    {"odom_frame": odom_frame_id},
                    {"base_link_frame": base_link_id},
                    {"world_frame": map_frame_id},
                    {"publish_tf": True},
                    {"reset_on_time_jump": True},
                    {"odom0": "platform/odometry"},
                    {
                        "odom0_config": [
                            False,
                            False,
                            True,
                            False,
                            False,
                            False,
                            True,
                            True,
                            False,
                            False,
                            False,
                            False,
                            False,
                            False,
                            False,
                        ]
                    },
                    {"odom0_differential": False},
                    {"odom0_relative": True},
                    {"odom0_nodelay": False},
                    {"odom0_queue_size": 2},
                    {"odom1": "odometry/gps"},
                    {
                        "odom1_config": [
                            True,
                            True,
                            False,
                            False,
                            False,
                            False,
                            False,
                            False,
                            False,
                            False,
                            False,
                            False,
                            False,
                            False,
                            False,
                        ]
                    },
                    {"odom1_differential": False},
                    {"odom1_relative": False},
                    {"odom1_queue_size": 2},
                    {"imu0": "sensors/imu_0/data"},
                    {
                        "imu0_config": [
                            False,
                            False,
                            False,
                            False,
                            False,
                            True,
                            False,
                            False,
                            False,
                            False,
                            False,
                            True,
                            False,
                            False,
                            False,
                        ]
                    },
                    {"imu0_differential": False},
                    {"imu0_relative": False},
                    {"imu0_queue_size": 10},
                    {"imu0_pose_rejection_threshold": 0.8},
                    {"imu0_twist_rejection_threshold": 5.0},
                    {"imu0_linear_acceleration_rejection_threshold": 0.8},
                    {"imu0_remove_gravitational_acceleration": True},
                    {"use_control": False},
                    # {"control_config": [True,True,False,False,False,True]},
                    # {"process_noise_covariance": [1.0, 1.0, 1.0, 0.01, 0.1, 0.1, 0.1, 0.1, 0.1, 0.01, 0.01, 0.01, 0.1, 0.1, 0.1]},
                    # {"initial_estimate_covariance": [1.0, 1.0, 1e-9, 1.0, 1.0, 1e-9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]},
                ],
                remappings=[
                    # ('/tf', 'tf'),
                    # ('/tf_static', 'tf_static'),
                    # ('/diagnostics', 'diagnostics'),
                    # ('imu', 'sensors/imu_0/data'),
                    # ('odom', 'platform/odom'),
                    ("odometry/filtered", "odometry/global"),
                ],
            ),
            launch_ros.actions.Node(
                package="robot_localization",
                namespace=robot_namespace,
                executable="navsat_transform_node",
                name="navsat_transform",
                output="screen",
                parameters=[
                    {"frequency": 10.0},
                    {"delay": 3.0},
                    {"map_frame": map_frame_id},
                    {"odom_frame": odom_frame_id},
                    {"world_frame": map_frame_id},
                    {"base_link_frame": base_link_id},
                    {"gps_frame": navsat_link_id},
                    {
                        "magnetic_declination_radians": 0.1117
                    },  # For lat/long 29.628164, -82.360346
                    {
                        "yaw_offset": 0.0
                    },  # 1.570796327 IMU reads 0 facing magnetic north, not east
                    {"zero_altitude": False},
                    {"broadcast_utm_transform": True},
                    {"broadcast_utm_transform_as_parent_frame": True},
                    {"broadcast_cartesian_transform": False},
                    {"publish_filtered_gps": True},
                    {"use_odometry_yaw": False},
                    {"wait_for_datum": True},
                    {"datum": [29.628164, -82.360346, -0.602196554855]},
                ],
                remappings=[
                    # ('/tf', 'tf'),
                    # ('/tf_static', 'tf_static'),
                    # ('/diagnostics', 'diagnostics'),
                    ("imu", "sensors/imu_0/data"),
                    ("gps/fix", "sensors/gps/fix"),
                    ("gps/filtered", "gps/filtered"),
                    ("odometry/gps", "odometry/gps"),
                    ("odometry/filtered", "odometry/global"),
                ],
            ),
        ]
    )
