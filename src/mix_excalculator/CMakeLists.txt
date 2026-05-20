cmake_minimum_required(VERSION 3.8)
project(mix_excalculator)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(ros_study_msgs REQUIRED) #ros_study_msgs의 통신 인터페이스 사용
find_package(rclcpp_action REQUIRED)
find_package(ament_cmake_python REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)
ament_python_install_package(${PROJECT_NAME})

include_directories(include 
  mix_excalculator/include/checker
  mix_excalculator/include/calculator
)

set(EXECUTABLES
  argument
  operator
  calculator
  checker
)

foreach(target ${EXECUTABLES})
  if (${target} STREQUAL "calculator")
    set(source_file src/calculator/${target}.cpp)
  elseif (${target} STREQUAL "checker")
    set(source_file src/checker/${target}.cpp)
  else()
    set(source_file src/arithmetic/${target}.cpp)
  endif()

  if (${target} STREQUAL "calculator")
    add_executable(${target} ${source_file} src/calculator/main.cpp)
  elseif (${target} STREQUAL "checker")
    add_executable(${target} ${source_file} src/checker/main.cpp)
  else()
    add_executable(${target} ${source_file})
  endif()
  ament_target_dependencies(${target}
    rclcpp
    std_msgs
    ros_study_msgs
    rclcpp_action
  )
  install(TARGETS ${target} DESTINATION lib/${PROJECT_NAME})
endforeach()


install(PROGRAMS
  mix_excalculator/arithmetic/argument.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME argument_py
)

install(PROGRAMS
  mix_excalculator/arithmetic/operator.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME operator_py
)

install(PROGRAMS
  mix_excalculator/calculator/main.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME calculator_py
)

install(PROGRAMS
  mix_excalculator/checker/main.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME checker_py
)

install(DIRECTORY
  launch
  param
  DESTINATION share/${PROJECT_NAME}/
)

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
