from launch.actions import (
    DeclareLaunchArgument,
    LogInfo,
    OpaqueFunction,
)
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node

from launch import LaunchDescription


def platform_transform(context):

    platform = LaunchConfiguration("platform").perform(context).lower()
    model = LaunchConfiguration("model").perform(context).lower()
    robot_namespace = LaunchConfiguration("robot_namespace").perform(context).strip("/")

    if not robot_namespace:
        raise RuntimeError("robot_namespace cannot be empty")

    if not model:
        raise RuntimeError("model cannot be empty")

    base_link_frame = f"{robot_namespace}/base_link"
    navsat_link_frame = f"{robot_namespace}/navsat_link"
    imu_link_frame = f"{robot_namespace}/imu_link"

    return LaunchDescription(
        [
            launch_ros.actions.Node(
                package="tf2_ros",
                namespace=robot_namespace,
                executable="static_transform_publisher",
                name="static_navsat_tf_publisher",
                arguments=[
                    "0.0",
                    "0.0",
                    "0.2",
                    "0.0",
                    "0.0",
                    "0.0",
                    base_link,
                    navsat_link,
                ],
                parameters=[],
                #            remappings=[('/tf', 'tf'),
                #                        ('/tf_static', 'tf_static'),
                #                        ('/diagnostics', 'diagnostics'),
                #                        ],
            ),
            launch_ros.actions.Node(
                package="tf2_ros",
                namespace=robot_namespace,
                executable="static_transform_publisher",
                name="static_imu_tf_publisher",
                arguments=[
                    "0.1",
                    "0.0",
                    "0.2",
                    "0.0",
                    "0.0",
                    "0.0",
                    base_link,
                    imu_link,
                ],
                # arguments=["0.0","0.0","0.0","0.602196554855","0.0","0.0", base_link, imu_link],
                parameters=[],
                #        remappings=[('/tf', 'tf'),
                #                    ('/tf_static', 'tf_static'),
                #                    ('/diagnostics', 'diagnostics'),
                #                    ],
            ),
            launch_ros.actions.Node(
                package="tf2_ros",
                namespace=robot_namespace,
                executable="static_transform_publisher",
                name="static_park_tf_publisher",
                # arguments=["-368305.0700699703","-3278357.100811787","-0.6021965548550632","0.0","0.0", "utm", "autonomy_park"],
                arguments=[
                    "368305.0700699703",
                    "3278357.100811787",
                    "0.0",
                    "0.0",
                    "0.0",
                    "0.0",
                    "utm",
                    "autonomy_park",
                ],
                parameters=[],
                #        remappings=[('/tf', 'tf'),
                #                    ('/tf_static', 'tf_static'),
                #                    ('/diagnostics', 'diagnostics'),],
            ),
        ]
    )


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "platform",
                description="Platform name: `unitree` or `clearpath`",
            ),
            DeclareLaunchArgument(
                "model",
                description="Model name: `go1`, `b1`, `husky`, or `jackal`",
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
