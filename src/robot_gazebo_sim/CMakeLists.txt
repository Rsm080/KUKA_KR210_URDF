cmake_minimum_required(VERSION 3.8)
project(robot_gazebo_sim)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY config launch meshes urdf worlds
  DESTINATION share/${PROJECT_NAME}
)

install(
  PROGRAMS scripts/gazebo_joint_demo
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
