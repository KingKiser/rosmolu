#include "../include/calculator/calculator.h"

#include <thread>
#include <chrono>

using namespace std::chrono_literals;
using std::placeholders::_1;
using std::placeholders::_2;
using std::placeholders::_3;

Calculator::Calculator()
: Node("calculator"),
  argument_a_(0.0), argument_b_(0.0),
  argument_operator_(0), argument_result_(0.0),
  argument_formula_(""),
  operator_{"+", "-", "*", "/"}
{
  RCLCPP_INFO(this->get_logger(), "Calculator init set start");

  this->declare_parameter("qos_depth", 10);
  int qos_depth = this->get_parameter("qos_depth").as_int();
  RCLCPP_INFO(this->get_logger(), "qos_depth set ok %d", qos_depth);

  auto qos_profile = rclcpp::QoS(rclcpp::QoSInitialization::from_rmw(rmw_qos_profile_default))
                        .keep_last(qos_depth)
                        .reliable()
                        .durability_volatile();

  argument_sub_ = this->create_subscription<ros_study_msgs::msg::ArithmeticArgument>(
    "arithmetic_argument",
    qos_profile,
    std::bind(&Calculator::get_arithmetic_argument, this, _1));
  RCLCPP_INFO(this->get_logger(), "arithmetic_argument_subscriber on");

  operator_srv_ = this->create_service<ros_study_msgs::srv::ArithmeticOperator>(
    "arithmetic_operator",
    std::bind(&Calculator::get_arithmetic_operator, this, _1, _2));
  RCLCPP_INFO(this->get_logger(), "arithmetic_service_server on");

  checker_action_server_ = rclcpp_action::create_server<ArithmeticChecker>(
    this,
    "arithmetic_checker",
    std::bind(&Calculator::handle_goal, this, _1, _2),
    std::bind(&Calculator::handle_cancel, this, _1),
    std::bind(&Calculator::execute_checker, this, _1));
  RCLCPP_INFO(this->get_logger(), "arithmetic_action_server on");
}

void Calculator::get_arithmetic_argument(const ros_study_msgs::msg::ArithmeticArgument::SharedPtr msg)
{
  argument_a_ = msg->argument_a;
  argument_b_ = msg->argument_b;
  RCLCPP_INFO(this->get_logger(), "Timestamp of the message: %d", msg->stamp.sec);
  RCLCPP_INFO(this->get_logger(), "Subscribed argument a: %f", argument_a_);
  RCLCPP_INFO(this->get_logger(), "Subscribed argument b: %f", argument_b_);
}

void Calculator::get_arithmetic_operator(
  const std::shared_ptr<ros_study_msgs::srv::ArithmeticOperator::Request> request,
  std::shared_ptr<ros_study_msgs::srv::ArithmeticOperator::Response> response)
{
  argument_operator_ = request->arithmetic_operator;
  argument_result_ = calculate_given_formula(argument_a_, argument_b_, argument_operator_);
  response->arithmetic_result = argument_result_;
  argument_formula_ = std::to_string(argument_a_) + " " +
                      operator_[argument_operator_ - 1] + " " +
                      std::to_string(argument_b_) + " = " +
                      std::to_string(argument_result_);
  RCLCPP_INFO(this->get_logger(), "%s", argument_formula_.c_str());
}

float Calculator::calculate_given_formula(float a, float b, int op)
{
  switch (op)
  {
    case ros_study_msgs::srv::ArithmeticOperator::Request::PLUS:
      return a + b;
    case ros_study_msgs::srv::ArithmeticOperator::Request::MINUS:
      return a - b;
    case ros_study_msgs::srv::ArithmeticOperator::Request::MULTIPLY:
      return a * b;
    case ros_study_msgs::srv::ArithmeticOperator::Request::DIVISION:
      if (b == 0.0)
      {
        RCLCPP_ERROR(this->get_logger(), "ZeroDivisionError!");
        return 0.0;
      }
      return a / b;
    default:
      RCLCPP_ERROR(this->get_logger(), "Invalid operator!");
      return 0.0;
  }
}

rclcpp_action::GoalResponse Calculator::handle_goal(
  const rclcpp_action::GoalUUID &,
  std::shared_ptr<const ArithmeticChecker::Goal> goal)
{
  RCLCPP_INFO(this->get_logger(), "Received goal request: goal_sum = %f", goal->goal_sum);
  return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
}

rclcpp_action::CancelResponse Calculator::handle_cancel(
  const std::shared_ptr<GoalHandleChecker>)
{
  RCLCPP_INFO(this->get_logger(), "Received request to cancel goal");
  return rclcpp_action::CancelResponse::ACCEPT;
}

void Calculator::execute_checker(const std::shared_ptr<GoalHandleChecker> goal_handle)
{
  RCLCPP_INFO(this->get_logger(), "Executing action checker");

  const auto goal = goal_handle->get_goal();
  auto feedback = std::make_shared<ArithmeticChecker::Feedback>();
  auto result = std::make_shared<ArithmeticChecker::Result>();

  float total_sum = 0.0;
  while (total_sum < goal->goal_sum)
  {
    total_sum += argument_result_;
    feedback->formula.push_back(argument_formula_);
    RCLCPP_INFO(this->get_logger(), "Feedback: %s", argument_formula_.c_str());
    goal_handle->publish_feedback(feedback);
    std::this_thread::sleep_for(1s);
  }

  result->all_formula = feedback->formula;
  result->total_sum = total_sum;
  goal_handle->succeed(result);
}
