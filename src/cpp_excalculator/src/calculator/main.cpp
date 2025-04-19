#include "../include/calculator/calculator.h"
#include "rclcpp/rclcpp.hpp"

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Calculator>());
  rclcpp::shutdown();
  return 0;
}
