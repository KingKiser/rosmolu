#ifndef CHECKER_HPP_
#define CHECKER_HPP_

#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "ros_study_msgs/action/arithmetic_checker.hpp"

class Checker : public rclcpp::Node
{
public:
  using ArithmeticChecker = ros_study_msgs::action::ArithmeticChecker;
  using GoalHandleChecker = rclcpp_action::ClientGoalHandle<ArithmeticChecker>;

  Checker();

  bool send_goal_total_sum(float goal_sum);  // <-- 이게 public이어야 함

private:
  void feedback_callback(GoalHandleChecker::SharedPtr,
                         const std::shared_ptr<const ArithmeticChecker::Feedback> feedback);

  void result_callback(const GoalHandleChecker::WrappedResult & result);

  rclcpp_action::Client<ArithmeticChecker>::SharedPtr action_client_;
};

#endif  // CHECKER_HPP_
