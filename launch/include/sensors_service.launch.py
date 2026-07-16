import os

from ament_index_python import get_package_share_directory
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

    # Include Packages
    minimal_startup_ground = FindPackageShare("minimal_startup_ground")

    launch_file_imu_0 = PathJoinSubstitution(
        [minimal_startup_ground, "launch/include", "imu_0.launch.py"]
    )

    # Include launch files
    launch_imu_0 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([launch_file_imu_0]),
    )

    launch_imu_0 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory("minimal_startup_ground")),
                "/imu_0.launch.py",
            ]
        )
    )

    emlid_interface = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory("emlid_interface"), "launch"),
                "/emlid_interface_launch.py",
            ]
        )
    )

    # Create LaunchDescription
    ld = LaunchDescription()
    ld.add_action(launch_imu_0)
    ld.add_action(emlid_interface)
    return ld
