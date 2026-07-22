from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

from launch import LaunchDescription


def generate_launch_description():
    robot_namespace = LaunchConfiguration("robot_namespace")
    params_file = LaunchConfiguration("params_file")

    default_param_file = PathJoinSubstitution(
        [
            FindPackageShare("minimal_startup_ground"),
            "param",
            "holonomic_interpreter.yaml",
        ]
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "robot_namespace",
                description=(
                    "Namespace for the specific robot, without a leading slash"
                ),
            ),
            DeclareLaunchArgument("params_file", default_value=default_param_file),
            Node(
                package="holonomic_interpreter",
                executable="holonomic_interpreter_node",
                name="holonomic_interpreter",
                parameters=[params_file],
                remappings=[
                    ("holo_cmd_vel", "cmd_vel_filtered"),
                    ("odom", "odometry/global"),
                    ("nonholo_cmd_vel", "cmd_vel"),
                ],
            ),
        ]
    )
