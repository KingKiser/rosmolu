#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "ros_study_msgs/action/my_action.hpp"

class MyActionServer : public rclcpp::Node
{
public:
  using MyAction = ros_study_msgs::action::MyAction;
  using GoalHandleMyAction = rclcpp_action::ServerGoalHandle<MyAction>;

  MyActionServer()
  : Node("my_action_server")
  {
    action_server_ = rclcpp_action::create_server<MyAction>(
      this,
      "my_action",
      std::bind(&MyActionServer::handle_goal, this, std::placeholders::_1, std::placeholders::_2),
      std::bind(&MyActionServer::handle_cancel, this, std::placeholders::_1),
      std::bind(&MyActionServer::handle_accepted, this, std::placeholders::_1));
  }

private:
  rclcpp_action::Server<MyAction>::SharedPtr action_server_;

  rclcpp_action::GoalResponse handle_goal(
    const rclcpp_action::GoalUUID &, std::shared_ptr<const MyAction::Goal> goal)
  {
    RCLCPP_INFO(this->get_logger(), "Received goal: %f", goal->go);
    return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
  }

  rclcpp_action::CancelResponse handle_cancel(
    const std::shared_ptr<GoalHandleMyAction>)
  {
    return rclcpp_action::CancelResponse::ACCEPT;
  }

  void handle_accepted(const std::shared_ptr<GoalHandleMyAction> goal_handle)
  {
    std::thread{std::bind(&MyActionServer::execute, this, goal_handle)}.detach();
  }

  void execute(const std::shared_ptr<GoalHandleMyAction> goal_handle)
  {
    auto feedback = std::make_shared<MyAction::Feedback>();
    auto result = std::make_shared<MyAction::Result>();

    for (int i = 0; i < 5; ++i) {
      feedback->str.push_back("Step " + std::to_string(i));
      goal_handle->publish_feedback(feedback);
      RCLCPP_INFO(this->get_logger(), "Sending feedback: Step %d", i);
      rclcpp::sleep_for(std::chrono::seconds(1));
    }

    result->res = goal_handle->get_goal()->go * 2.0;
    goal_handle->succeed(result);
  }
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MyActionServer>());
  rclcpp::shutdown();
  return 0;
}
