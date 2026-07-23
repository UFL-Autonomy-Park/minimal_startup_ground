from launch.actions import (
    DeclareLaunchArgument,
    LogInfo,
    OpaqueFunction,
)
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

from launch import LaunchDescription


def launch_platform(context):
    platform = LaunchConfiguration("platform").perform(context).lower()
    robot_namespace = LaunchConfiguration("robot_namespace").perform(context).strip("/")

    if not robot_namespace:
        raise RuntimeError("robot_namespace cannot be empty")

    odom_frame = f"{robot_namespace}/odom"
    base_link_frame = f"{robot_namespace}/base_link"

    if platform == "clearpath":
        return [
            LogInfo(
                msg=(
                    "Clearpath platform selected. No local platform nodes will be launched. The Clearpath SBC is expected to provide cmd_vel and platform/odom."
                )
            )
        ]

    if platform != "unitree":
        raise RuntimeError("platform must be either 'unitree' or 'clearpath'")

    unitree_velocity_interface = Node(
        package="unitree_velocity_interface",
        executable="unitree_velocity_interface_node",
        name="unitree_velocity_interface",
        namespace=robot_namespace,
        output="screen",
        parameters=[
            {
                "base_link_id": base_link_frame,
                "odom_frame_id": odom_frame,
                "command_pub_frequency": 100,
                "command_timeout": 0.25,
            }
        ],
        remappings=[
            ("platform/odometry", "platform/odom"),
        ],
    )

    unitree_legged_real = Node(
        package="unitree_legged_real",
        executable="udp",
        name="udp",
        namespace=robot_namespace,
        output="screen",
    )

    return [
        unitree_velocity_interface,
        unitree_legged_real,
    ]


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "platform",
                description="Platform name: `unitree` or `clearpath`",
            ),
            DeclareLaunchArgument(
                "robot_namespace",
                description=(
                    "Namespace for the specific robot, without a leading slash"
                ),
            ),
            OpaqueFunction(function=launch_platform),
        ]
    )
