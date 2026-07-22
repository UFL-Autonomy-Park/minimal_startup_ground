from ament_index_python.packages import get_package_share_directory
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    GroupAction,
    IncludeLaunchDescription,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    EnvironmentVariable,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.actions import Node, SetRemap
from launch_ros.substitutions import FindPackageShare

import launch
from launch import LaunchDescription


def generate_launch_description():

    robot_namespace = LaunchConfiguration("robot_namespace")

    # Microstrain
    launch_microstrain = LaunchConfiguration("launch_microstrain")
    microstrain_launch_path = PathJoinSubstitution(
        [
            FindPackageShare("microstrain_inertial_driver"),
            "launch",
            "microstrain_launch.py",
        ]
    )
    microstrain_param = PathJoinSubstitution(
        [
            FindPackageShare("minimal_startup_ground"),
            "param",
            "microstrain_inertial_driver.yaml",
        ]
    )

    microstrain_imu = GroupAction(
        [
            SetRemap("imu/data", "data"),
            SetRemap("/moving_ang", "moving_ang"),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([microstrain_launch_path]),
                launch_arguments={
                    "namespace": f"{robot_namespace}/sensors/imu",
                    "params_file": microstrain_param,
                    "configure": "true",
                    "activate": "true",
                }.items(),
                parameters=[{"imu_frame_id": f"{robot_namespace}/imu_link"}],
            ),
        ],
        condition=IfCondition(launch_microstrain),
    )

    # Emlid GPS
    launch_emlid = LaunchConfiguration("launch_emlid")
    emlid_param = PathJoinSubstitution(
        [FindPackageShare("minimal_startup_ground"), "param", "emlid_interface.yaml"]
    )
    emlid_gps = Node(
        package="emlid_interface",
        executable="emlid_interface_node",
        name="emlid_interface",
        namespace=robot_namespace,
        parameters=[emlid_param, {"navsat_link_id": f"{robot_namespace}/navsat_link"}],
        remappings=[("rtk/fix", "sensors/gps/fix")],
        condition=IfCondition(launch_emlid),
    )

    # Zed 2i
    launch_zed = LaunchConfiguration("launch_zed")
    zed_model = LaunchConfiguration("zed_model")
    zed_camera_name = LaunchConfiguration("zed_camera_name")
    zed_namespace = LaunchConfiguration("zed_namespace")
    zed_stereo_camera = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    FindPackageShare("zed_wrapper"),
                    "launch",
                    "zed_camera.launch.py",
                ]
            )
        ),
        condition=IfCondition(launch_zed),
        launch_arguments={
            "camera_model": zed_model,
            "camera_name": zed_camera_name,
            "namespace": zed_namespace,
        }.items(),
    )

    # Velodyne LiDAR
    launch_velodyne = LaunchConfiguration("launch_velodyne")
    velodyne_launch_path = PathJoinSubstitution(
        [FindPackageShare("velodyne"), "launch", "velodyne-all-nodes-VLP16-launch.py"]
    )
    velodyne_lidar = GroupAction(
        [
            SetRemap("velodyne_packets", "sensors/lidar/packets"),
            SetRemap("velodyne_points", "sensors/lidar/points"),
            SetRemap("scan", "sensors/lidar/scan"),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([velodyne_launch_path]),
            ),
        ],
        condition=IfCondition(launch_velodyne),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "robot_namespace",
                description=(
                    "Namespace for the specific robot, without a leading slash"
                ),
            ),
            DeclareLaunchArgument(
                "launch_microstrain",
                default_value="true",
                description="Launch Microstrain IMU",
            ),
            DeclareLaunchArgument(
                "launch_emlid",
                default_value="true",
                description="Launch Emlid GPS",
            ),
            DeclareLaunchArgument(
                "launch_zed",
                default_value="false",
                description="Launch the ZED camera wrapper",
            ),
            DeclareLaunchArgument(
                "zed_model",
                default_value="zed2i",
                description="ZED camera model",
            ),
            DeclareLaunchArgument(
                "zed_camera_name",
                default_value="zed",
                description="ZED camera name",
            ),
            DeclareLaunchArgument(
                "zed_namespace",
                default_value="go1",
                description="Optional ZED namespace",
            ),
            DeclareLaunchArgument(
                "launch_velodyne",
                default_value="true",
                description="Launch Velodyne LiDAR",
            ),
            microstrain_imu,
            emlid_gps,
            velodyne_lidar,
            zed_stereo_camera,
        ]
    )
