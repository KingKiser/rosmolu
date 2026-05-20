cmake_minimum_required(VERSION 3.8)
project(hangman_game_cpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(hangman_interfaces REQUIRED)

set(EXECUTABLES
  letter_publisher
  progress_action_client
  progress_action_server
  user_input
  word_service
)

foreach(target ${EXECUTABLES})
  add_executable(${target} src/${target}.cpp)

  ament_target_dependencies(${target} rclcpp rclcpp_action std_msgs hangman_interfaces)

  install(TARGETS
    ${target}
    DESTINATION lib/${PROJECT_NAME}
  )
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
