cmake_minimum_required(VERSION 3.8)
project(ros_study_cpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(ros_study_msgs REQUIRED)
find_package(rclcpp_action REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

set(EXECUTABLES
  my_msg_test
  my_msg_subscriber
  my_service_client
  my_service_server
  my_action_client
  my_action_server
)

foreach(target ${EXECUTABLES})
  add_executable(${target} src/${target}.cpp)
  if (${target} STREQUAL "my_action_client")
    ament_target_dependencies(${target} rclcpp std_msgs ros_study_msgs rclcpp_action)
  elseif (${target} STREQUAL "my_action_server")
    ament_target_dependencies(${target} rclcpp std_msgs ros_study_msgs rclcpp_action)
  else()
    ament_target_dependencies(${target} rclcpp std_msgs ros_study_msgs)
  endif()
  install(TARGETS ${target} DESTINATION lib/${PROJECT_NAME})
endforeach()


if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
