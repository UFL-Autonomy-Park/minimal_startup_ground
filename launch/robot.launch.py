from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.substitutions import FindPackageShare

from launch import LaunchDescription


def generate_launch_description():

    # get parameters
    platform = LaunchConfiguration("platform")
    model = LaunchConfiguration("model")
    robot_namespace = LaunchConfiguration("robot_namespace")
    launch_microstrain = LaunchConfiguration("launch_microstrain")
    launch_emlid = LaunchConfiguration("launch_emlid")
    launch_zed = LaunchConfiguration("launch_zed")
    zed_model = LaunchConfiguration("zed_model")
    zed_camera_name = LaunchConfiguration("zed_camera_name")
    zed_namespace = LaunchConfiguration("zed_namespace")
    launch_velodyne = LaunchConfiguration("launch_velodyne")

    # launch platform
    platform_launch_path = PathJoinSubstitution(
        [FindPackageShare("minimal_startup_ground"), "launch", "platform.launch.py"]
    )
    platform_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([platform_launch_path]),
        launch_arguments={
            "platform": platform,
            "robot_namespace": robot_namespace,
        }.items(),
    )

    # launch sensors
    sensors_launch_path = PathJoinSubstitution(
        [FindPackageShare("minimal_startup_ground"), "launch", "sensors.launch.py"]
    )
    sensors_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [sensors_launch_path],
        ),
        launch_arguments={
            "robot_namespace": robot_namespace,
            "launch_microstrain": launch_microstrain,
            "launch_emlid": launch_emlid,
            "launch_zed": launch_zed,
            "zed_model": zed_model,
            "zed_camera_name": zed_camera_name,
            "zed_namespace": zed_namespace,
            "launch_velodyne": launch_velodyne,
        }.items(),
    )

    # launch transforms
    transforms_launch_path = PathJoinSubstitution(
        [FindPackageShare("minimal_startup_ground"), "launch", "transforms.launch.py"]
    )
    transforms_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [transforms_launch_path],
        ),
        launch_arguments={
            "platform": platform,
            "model": model,
            "robot_namespace": robot_namespace,
        }.items(),
    )

    # launch localization
    localization_launch_path = PathJoinSubstitution(
        [FindPackageShare("minimal_startup_ground"), "launch", "localization.launch.py"]
    )
    localization_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [localization_launch_path],
        ),
        launch_arguments={
            "robot_namespace": robot_namespace,
        }.items(),
    )

    # launch holonomic interpreter
    holonomic_interpreter_launch_path = PathJoinSubstitution(
        [
            FindPackageShare("minimal_startup_ground"),
            "launch",
            "holonomic_interpreter.launch.py",
        ]
    )
    holonomic_interpreter_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [holonomic_interpreter_launch_path],
        ),
        launch_arguments={
            "robot_namespace": robot_namespace,
        }.items(),
    )

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
                default_value="homebrew",
                description="Optional ZED namespace",
            ),
            DeclareLaunchArgument(
                "launch_velodyne",
                default_value="true",
                description="Launch Velodyne LiDAR",
            ),
            platform_launch,
            sensors_launch,
            transforms_launch,
            localization_launch,
            holonomic_interpreter_launch,
        ]
    )
