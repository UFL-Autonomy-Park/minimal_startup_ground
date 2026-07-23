# minimal_startup_ground
This is a meta-package which launches necessary localization and control packages for the ground robots at the UF Autonomy Park

## Launch Files
### robot.launch.py
Main launch file which accepts all arguments. Propagates namespace throughout child launch files 
```
minimal_startup_ground
└──robot.launch.py
	├── platform.launch.py
	├── sensors.launch.py
	├── transforms.launch.py
	├── localization.launch.py
	└── holonomic_interpreter.launch.py
```

Valid platforms: `unitree,clearpath`
Valid models: `go1,b1,husky,jackal`

### platform.launch.py
Launches platform-specific nodes. 
- For `unitree`, launches `unitree_velocity_interface` and `unitree_legged_real`
- For `clearpath`, does nothing

### sensors.launch.py
In charge of the Microstrain IMU, Emlid RS+ GPS unit, Zed 2i, and Velodyne VLP16 LiDAR. Launches:
- [`microstrain_inertial_driver`](https://github.com/LORD-MicroStrain/microstrain_inertial)
- [`emlid_interface`](https://github.com/UFL-Autonomy-Park/emlid_interface)
- [`zed_wrapper`](https://github.com/stereolabs/zed-ros2-wrapper)
- [`velodyne`](https://github.com/ros-drivers/velodyne)

### transforms.launch.py
Publishes static transforms `base_link->navsat_link` and `base_link->imu_link`

### localization.launch.py
Launches [`robot_localization`](https://github.com/cra-ros-pkg/robot_localization)

### holonomic_interpreter.launch.py
Launches [`holonomic_interpreter`](https://github.com/UFL-Autonomy-Park/holonomic_interpreter)

## Launch Arguments
| Argument | Description | Default |
|---|---|---|
| `platform` | Robot platform: `unitree` or `clearpath` | Required |
| `model` | Robot model: `go1`, `b1`, `husky`, or `jackal` | Required |
| `robot_namespace` | Robot namespace without leading slash | Required |
| `launch_microstrain` | Launch the MicroStrain driver | `true` |
| `launch_emlid` | Launch the Emlid interface | `true` |
| `launch_zed` | Launch the ZED camera wrapper | `false` |
| `zed_model` | ZED camera model | `zed2i` |
| `zed_camera_name` | ZED camera node name | `zed` |
| `zed_namespace` | Namespace used by the ZED wrapper | `go1` |
| `launch_velodyne` | Launch the Velodyne LiDAR driver | `true` |

## Sample Usage
```
ros2 launch minimal_startup_ground robot.launch.py \ 
	platform:=unitree \
	model:=go1 \
	robot_namespace:=go1_158 \
	launch_microstrain:=true \
	launch_emlid:=true \
	launch_zed:=false \
	zed_model:=zed2i \
	zed_camera_name:=zed \
	zed_namespace:=go1_158 \
	launch_velodyne:=true
```

## Notes
The static transforms for each robotic platform are hard-coded into `transforms.launch.py`. Edit this file if you move sensors around, or if you are using this repo for a different robot. 

## TO-DO:
- Add static transform for LiDAR