from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare

from launch import LaunchDescription


def generate_launch_description():
    robot_namespace = LaunchConfiguration("robot_namespace")

    localization_params = PathJoinSubstitution(
        [FindPackageShare("minimal_startup_ground"), "param", "localization.yaml"]
    )

    odom_frame = ParameterValue([robot_namespace, "/odom"], value_type=str)
    base_link_frame = ParameterValue([robot_namespace, "/base_link"], value_type=str)

    ekf_local_node = Node(
        package="robot_localization",
        executable="ekf_node",
        name="ekf_local",
        namespace=robot_namespace,
        output="screen",
        parameters=[
            localization_params,
            {"map_frame": "autonomy_park"},
            {"odom_frame": odom_frame},
            {"base_link_frame": base_link_frame},
            {"world_frame": odom_frame},
        ],
        remappings=[("odometry/filtered", "odometry/local")],
    )
    ekf_global_node = Node(
        package="robot_localization",
        executable="ekf_node",
        name="ekf_global",
        namespace=robot_namespace,
        output="screen",
        parameters=[
            localization_params,
            {"map_frame": "autonomy_park"},
            {"odom_frame": odom_frame},
            {"base_link_frame": base_link_frame},
            {"world_frame": "autonomy_park"},
        ],
        remappings=[("odometry/filtered", "odometry/global")],
    )
    navsat_transform_node = Node(
        package="robot_localization",
        executable="navsat_transform_node",
        name="navsat_transform",
        namespace=robot_namespace,
        output="screen",
        parameters=[
            localization_params,
        ],
        remappings=[
            ("imu", "sensors/imu/data"),
            ("gps/fix", "sensors/gps/fix"),
            ("gps/filtered", "sensors/gps/filtered"),
            ("odometry/filtered", "odometry/global"),
        ],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "robot_namespace",
                description="Namespace for platform, TF prefix",
            ),
            ekf_local_node,
            ekf_global_node,
            navsat_transform_node,
        ]
    )
