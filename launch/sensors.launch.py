from ament_index_python.packages import get_package_share_directory
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    GroupAction,
    IncludeLaunchDescription,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    EnvironmentVariable,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.actions import Node, SetRemap
from launch_ros.substitutions import FindPackageShare

from launch import LaunchDescription


def generate_launch_description():

    microstrain_launch_path = PathJoinSubstitution(
        [
            FindPackageShare("microstrain_inertial_driver"),
            "launch",
            "microstrain_launch.py",
        ]
    )
    microstrain_param = PathJoinSubstitution(
        [FindPackageShare("minimal_startup_ground"), "param", "microstrain.yaml"]
    )

    microstrain_imu = GroupAction(
        [
            SetRemap("imu/data", "data"),
            SetRemap("/moving_ang", "moving_ang"),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([microstrain_launch_path]),
                launch_arguments={
                    "namespace": "sensors/imu",
                    "params_file": microstrain_param,
                    "configure": "true",
                    "activate": "true",
                }.items(),
            ),
        ]
    )

    # emlid = Node(
    #     package="emlid_interface",
    #     executable="emlid_interface_node",
    #     name="emlid_interface",
    #     parameters=
    # )

    return LaunchDescription([microstrain_imu])
