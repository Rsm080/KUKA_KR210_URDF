"""Launch the PN robot in Gazebo Classic with ros2_control."""

from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    RegisterEventHandler,
    TimerAction,
)
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import xacro


def generate_launch_description():
    package_share = Path(get_package_share_directory("robot_gazebo_sim"))
    gazebo_share = Path(get_package_share_directory("gazebo_ros"))
    xacro_file = package_share / "urdf" / "robot.gazebo.urdf.xacro"
    controllers_file = package_share / "config" / "controllers.yaml"
    world_file = package_share / "worlds" / "empty.world"

    robot_description = xacro.process_file(
        str(xacro_file),
        mappings={"controllers_file": str(controllers_file)},
    ).toxml()

    gui = LaunchConfiguration("gui")
    paused = LaunchConfiguration("paused")
    run_demo = LaunchConfiguration("demo")

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(str(gazebo_share / "launch" / "gazebo.launch.py")),
        launch_arguments={
            "world": str(world_file),
            "gui": gui,
            "pause": paused,
            "verbose": "false",
        }.items(),
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description, "use_sim_time": True}],
    )

    spawn_robot = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        name="spawn_kuka_kr210",
        output="screen",
        arguments=["-entity", "kuka_kr210", "-topic", "robot_description"],
    )

    joint_state_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
            "--controller-manager-timeout",
            "60",
        ],
        output="screen",
    )

    arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "arm_controller",
            "--controller-manager",
            "/controller_manager",
            "--controller-manager-timeout",
            "60",
        ],
        output="screen",
    )

    demo = Node(
        package="robot_gazebo_sim",
        executable="gazebo_joint_demo",
        name="gazebo_joint_demo",
        output="screen",
        condition=IfCondition(run_demo),
    )

    start_joint_state = RegisterEventHandler(
        OnProcessExit(target_action=spawn_robot, on_exit=[joint_state_spawner])
    )
    start_arm_controller = RegisterEventHandler(
        OnProcessExit(target_action=joint_state_spawner, on_exit=[arm_controller_spawner])
    )
    start_demo = RegisterEventHandler(
        OnProcessExit(
            target_action=arm_controller_spawner,
            on_exit=[TimerAction(period=1.0, actions=[demo])],
        )
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument("gui", default_value="true"),
            DeclareLaunchArgument("paused", default_value="false"),
            DeclareLaunchArgument(
                "demo",
                default_value="false",
                description="Send a small, collision-conscious joint trajectory after startup.",
            ),
            gazebo,
            robot_state_publisher,
            spawn_robot,
            start_joint_state,
            start_arm_controller,
            start_demo,
        ]
    )
