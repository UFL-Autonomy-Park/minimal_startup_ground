import os

import yaml
from ament_index_python.packages import get_package_share_directory
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    IncludeLaunchDescription,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    EnvironmentVariable,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

from launch import LaunchDescription


def generate_launch_description():

    file_path = os.path.expanduser("~/robot_param.yaml")
    with open(file_path, "r") as stream:
        try:
            data_loaded = yaml.safe_load(stream)
            robot_namespace = "/" + data_loaded["robot_namespace"]
            user = "/" + data_loaded["user"]
        except yaml.YAMLError as exc:
            print(exc)

    namespace = robot_namespace + "/sensors/imu_0"

    # Include Packages
    minimal_startup_ground = FindPackageShare("minimal_startup_ground")

    # Declare launch files
    # launch_file_microstrain_imu = PathJoinSubstitution([
    #    minimal_startup_ground, 'launch/include', 'microstrain_imu.launch.py'])

    # param_file_microstrain_imu = PathJoinSubstitution([
    #    minimal_startup_ground, 'config', 'imu_0.yaml'])

    param_file_microstrain_imu = (
        "/home"
        + user
        + "/platform_ws/src/Common/minimal_startup_ground/params/imu_0.yaml"
    )

    # Include launch files
    launch_microstrain_imu = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory("minimal_startup_ground")),
                "/microstrain_imu.launch.py",
            ]
        ),
        launch_arguments=[
            ("parameters", param_file_microstrain_imu),
            ("namespace", namespace),
        ],
    )

    # Create LaunchDescription
    ld = LaunchDescription()
    ld.add_action(launch_microstrain_imu)
    return ld
