#ifndef CPP_EXCALCULATOR__CALCULATOR_HPP_
#define CPP_EXCALCULATOR__CALCULATOR_HPP_

#include "rclcpp/rclcpp.hpp"
#include "ros_study_msgs/msg/arithmetic_argument.hpp"
#include "ros_study_msgs/srv/arithmetic_operator.hpp"
#include "ros_study_msgs/action/arithmetic_checker.hpp"
#include "rclcpp_action/rclcpp_action.hpp"

#include <string>
#include <vector>
#include <memory>

class Calculator : public rclcpp::Node
{
public:
  using ArithmeticChecker = ros_study_msgs::action::ArithmeticChecker;
  using GoalHandleChecker = rclcpp_action::ServerGoalHandle<ArithmeticChecker>;

  Calculator();

private:
  void get_arithmetic_argument(const ros_study_msgs::msg::ArithmeticArgument::SharedPtr msg);
  void get_arithmetic_operator(
    const std::shared_ptr<ros_study_msgs::srv::ArithmeticOperator::Request> request,
    std::shared_ptr<ros_study_msgs::srv::ArithmeticOperator::Response> response);
  float calculate_given_formula(float a, float b, int op);

  rclcpp_action::GoalResponse handle_goal(
    const rclcpp_action::GoalUUID & uuid,
    std::shared_ptr<const ArithmeticChecker::Goal> goal);
  rclcpp_action::CancelResponse handle_cancel(const std::shared_ptr<GoalHandleChecker> goal_handle);
  void execute_checker(const std::shared_ptr<GoalHandleChecker> goal_handle);

  // Member Variables
  float argument_a_, argument_b_;
  int argument_operator_;
  float argument_result_;
  std::string argument_formula_;
  std::vector<std::string> operator_;

  rclcpp::Subscription<ros_study_msgs::msg::ArithmeticArgument>::SharedPtr argument_sub_;
  rclcpp::Service<ros_study_msgs::srv::ArithmeticOperator>::SharedPtr operator_srv_;
  rclcpp_action::Server<ArithmeticChecker>::SharedPtr checker_action_server_;
};

#endif  // CPP_EXCALCULATOR__CALCULATOR_HPP_
