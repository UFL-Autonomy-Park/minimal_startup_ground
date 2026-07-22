from typing import Tuple

from launch.actions import (
    DeclareLaunchArgument,
    OpaqueFunction,
)
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

from launch import LaunchDescription

# Sensor mounting transforms for each robot platform and model
#
# xyz:
#   Position of sensor frame origin expressed in base_link; in meters
#
# rpy:
#   Orientation of sensor frame relative to base_link; in radians
MODEL_TRANSFORMS = {
    ("unitree", "go1"): {
        "gps": {"xyz": (0.0, 0.0, 0.2), "rpy": (0.0, 0.0, 0.0)},
        "imu": {"xyz": (0.1, 0.0, 0.2), "rpy": (0.0, 0.0, 0.0)},
    },
    ("unitree", "b1"): {
        "gps": {"xyz": (0.0, 0.0, 0.64), "rpy": (0.0, 0.0, 0.0)},
        "imu": {"xyz": (0.0, 0.0, 0.0), "rpy": (0.0, 0.0, 0.0)},
    },
    # CLEARPATH VALUES ARE OUTDATED
    ("clearpath", "husky"): {
        "gps": {"xyz": (0.0, 0.0, 0.64), "rpy": (0.0, 0.0, 0.0)},
        "imu": {"xyz": (0.0, 0.0, 0.0), "rpy": (0.0, 0.0, 0.0)},
    },
    ("clearpath", "jackal"): {
        "gps": {"xyz": (0.0, 0.0, 0.64), "rpy": (0.0, 0.0, 0.0)},
        "imu": {"xyz": (0.0, 0.0, 0.0), "rpy": (0.0, 0.0, 0.0)},
    },
}

VALID_PLATFORM_MODELS = {"unitree": {"go1", "b1"}, "clearpath": {"husky", "jackal"}}


def make_static_transform_node(
    *,
    node_name: str,
    namespace: str,
    parent_frame: str,
    child_frame: str,
    xyz: Tuple[float, float, float],
    rpy: Tuple[float, float, float],
) -> Node:

    x, y, z = xyz
    roll, pitch, yaw = rpy

    return Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        namespace=namespace,
        name=node_name,
        arguments=[
            "--x",
            str(x),
            "--y",
            str(y),
            "--z",
            str(z),
            "--roll",
            str(roll),
            "--pitch",
            str(pitch),
            "--yaw",
            str(yaw),
            "--frame-id",
            parent_frame,
            "--child-frame-id",
            child_frame,
        ],
    )


# CURRENTLY UNUSED, STORING FOR LATER
def autonomy_park_transform():
    return Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="static_park_tf_publisher",
        arguments=[
            "--x",
            "368305.0700699703",
            "--y",
            "3278357.100811787",
            "--z",
            "0.0",
            "--roll",
            "0.0",
            "--pitch",
            "0.0",
            "--yaw",
            "0.0",
            "--frame-id",
            "utm",
            "--child-frame-id",
            "autonomy_park",
        ],
    )


def platform_transforms(context):

    platform = LaunchConfiguration("platform").perform(context).strip().lower()
    model = LaunchConfiguration("model").perform(context).strip().lower()
    robot_namespace = LaunchConfiguration("robot_namespace").perform(context).strip("/")

    if not robot_namespace:
        raise RuntimeError("robot_namespace cannot be empty")

    if platform not in VALID_PLATFORM_MODELS:
        raise RuntimeError(
            f"Unsupported platform: `{platform}` "
            f"Expected one of: {sorted(VALID_PLATFORM_MODELS)}"
        )

    if model not in VALID_PLATFORM_MODELS[platform]:
        raise RuntimeError(
            f"Unsupported model `{model}` for platform `{platform}` "
            f"Expected one of: {sorted(VALID_PLATFORM_MODELS[platform])}"
        )

    platform_model = (platform, model)

    if platform_model not in MODEL_TRANSFORMS:
        raise RuntimeError(f"Transforms not defined for: ({platform},{model})")

    transforms = MODEL_TRANSFORMS[platform_model]

    base_link_frame = f"{robot_namespace}/base_link"
    navsat_link_frame = f"{robot_namespace}/navsat_link"
    imu_link_frame = f"{robot_namespace}/imu_link"

    return [
        make_static_transform_node(
            node_name="static_navsat_tf_publisher",
            namespace=robot_namespace,
            parent_frame=base_link_frame,
            child_frame=navsat_link_frame,
            xyz=transforms["gps"]["xyz"],
            rpy=transforms["gps"]["rpy"],
        ),
        make_static_transform_node(
            node_name="static_imu_tf_publisher",
            namespace=robot_namespace,
            parent_frame=base_link_frame,
            child_frame=imu_link_frame,
            xyz=transforms["imu"]["xyz"],
            rpy=transforms["imu"]["rpy"],
        ),
    ]


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
            OpaqueFunction(function=platform_transforms),
        ]
    )
