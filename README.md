# KUKA KR210 Gazebo 仿真

这是 KUKA KR210 的 ROS 2 Humble + Gazebo Classic 11 工作区。机器人模型、控制器、启动文件和运动演示均位于 `src/robot_gazebo_sim/`。

## 构建

```bash
cd /home/jsm/robot_gazebo_sim
source /opt/ros/humble/setup.bash
colcon build --packages-select robot_gazebo_sim
source install/setup.bash
```

## 启动

启动 Gazebo 和控制器：

```bash
ros2 launch robot_gazebo_sim gazebo.launch.py
```

启动后自动执行四点关节轨迹：

```bash
ros2 launch robot_gazebo_sim gazebo.launch.py demo:=true
```

也可以在仿真启动后单独发送轨迹：

```bash
ros2 run robot_gazebo_sim gazebo_joint_demo
```

无图形界面运行时追加 `gui:=false`。压缩包没有提供真实质量和惯量，当前参数是根据 STL 几何做的稳定仿真估算；Link_4 和 Link_7 未提供网格，因此在仿真中作为轻量运动框架。

`Joint_0` 将机器人底座固定在世界坐标系中。`Joint_1` 到 `Joint_6` 是六个可控运动关节，分别带动 `Link_1` 到 `Link_6`；`Link_6_to_Link_7` 是 `Link_6` 到末端 `Link_7` 的固定连接。
