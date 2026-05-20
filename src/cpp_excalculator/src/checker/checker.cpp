// src/arithmetic/checker.cpp

#include "../include/checker/checker.h"
#include <chrono>
using namespace std::chrono;

Checker::Checker()
: Node("checker")
{
  action_client_ = rclcpp_action::create_client<ArithmeticChecker>(this, "arithmetic_checker");
}

bool Checker::send_goal_total_sum(float goal_sum)  // ← 반드시 이렇게 써야 함
{
  int wait_count = 1;
  while (!action_client_->wait_for_action_server(std::chrono::milliseconds(100)))
  {
    if (wait_count > 3)
    {
      RCLCPP_WARN(this->get_logger(), "Arithmetic action server is not available.");
      return false;
    }
    wait_count++;
  }

  auto goal_msg = ArithmeticChecker::Goal();
  goal_msg.goal_sum = goal_sum;

  auto send_goal_options = rclcpp_action::Client<ArithmeticChecker>::SendGoalOptions();
  send_goal_options.feedback_callback =
    std::bind(&Checker::feedback_callback, this, std::placeholders::_1, std::placeholders::_2);
  send_goal_options.result_callback =
    std::bind(&Checker::result_callback, this, std::placeholders::_1);

  action_client_->async_send_goal(goal_msg, send_goal_options);
  return true;
}


void Checker::feedback_callback(
    GoalHandleChecker::SharedPtr,
    const std::shared_ptr<const ArithmeticChecker::Feedback> feedback)
{
    RCLCPP_INFO(this->get_logger(), "Action feedback:");
    for (const auto &formula : feedback->formula)
    {
        RCLCPP_INFO(this->get_logger(), "  %s", formula.c_str());
    }
}

void Checker::result_callback(const GoalHandleChecker::WrappedResult &result)
{
    switch (result.code)
    {
    case rclcpp_action::ResultCode::SUCCEEDED:
        RCLCPP_INFO(this->get_logger(), "Action succeeded!");
        break;
    case rclcpp_action::ResultCode::ABORTED:
        RCLCPP_WARN(this->get_logger(), "Action aborted.");
        return;
    case rclcpp_action::ResultCode::CANCELED:
        RCLCPP_WARN(this->get_logger(), "Action canceled.");
        return;
    default:
        RCLCPP_WARN(this->get_logger(), "Unknown result code.");
        return;
    }

    RCLCPP_INFO(this->get_logger(), "Action result (all formula):");
    for (const auto &f : result.result->all_formula)
    {
        RCLCPP_INFO(this->get_logger(), "  %s", f.c_str());
    }

    RCLCPP_INFO(this->get_logger(), "Action result (total sum): %f", result.result->total_sum);
}
