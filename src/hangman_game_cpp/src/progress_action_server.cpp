#include <chrono>
#include <memory>
#include <string>
#include <thread>

#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "hangman_interfaces/action/game_progress.hpp"
#include "hangman_interfaces/msg/progress.hpp"

using namespace std::chrono_literals;
using GameProgress = hangman_interfaces::action::GameProgress;
using Progress = hangman_interfaces::msg::Progress;
using GoalHandleGameProgress = rclcpp_action::ServerGoalHandle<GameProgress>;

class ProgressActionServer : public rclcpp::Node
{
public:
  ProgressActionServer()
  : Node("progress_action_server"), current_progress_()
  {
    action_server_ = rclcpp_action::create_server<GameProgress>(
      this,
      "game_progress",
      std::bind(&ProgressActionServer::handle_goal, this, std::placeholders::_1, std::placeholders::_2),
      std::bind(&ProgressActionServer::handle_cancel, this, std::placeholders::_1),
      std::bind(&ProgressActionServer::handle_accepted, this, std::placeholders::_1));

    subscription_ = this->create_subscription<Progress>(
      "progress",
      10,
      std::bind(&ProgressActionServer::progress_callback, this, std::placeholders::_1));

    RCLCPP_INFO(this->get_logger(), "Action Server Initialized");
  }

private:
  rclcpp_action::Server<GameProgress>::SharedPtr action_server_;
  rclcpp::Subscription<Progress>::SharedPtr subscription_;
  Progress current_progress_;

  rclcpp_action::GoalResponse handle_goal(
    const rclcpp_action::GoalUUID &,
    std::shared_ptr<const GameProgress::Goal>)
  {
    RCLCPP_INFO(this->get_logger(), "Action Server: Received goal request");
    return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
  }

  rclcpp_action::CancelResponse handle_cancel(
    const std::shared_ptr<GoalHandleGameProgress>)
  {
    RCLCPP_INFO(this->get_logger(), "Action Server: Received cancel request");
    return rclcpp_action::CancelResponse::REJECT;
  }

  void handle_accepted(const std::shared_ptr<GoalHandleGameProgress> goal_handle)
  {
    std::thread{std::bind(&ProgressActionServer::execute, this, goal_handle)}.detach();
  }

  void progress_callback(const Progress::SharedPtr msg)
  {
    current_progress_ = *msg;
    RCLCPP_INFO(this->get_logger(), "Progress updated: %s", current_progress_.current_state.c_str());
  }

  void execute(const std::shared_ptr<GoalHandleGameProgress> goal_handle)
  {
    auto feedback = std::make_shared<GameProgress::Feedback>();
    rclcpp::Rate loop_rate(1.0);  // 1Hz

    while (rclcpp::ok() && !current_progress_.game_over)
    {
      feedback->game_over = current_progress_.game_over;
      goal_handle->publish_feedback(feedback);
      RCLCPP_INFO(this->get_logger(), "Current State: %s", current_progress_.current_state.c_str());
      RCLCPP_INFO(this->get_logger(), "Attempts Left: %d", current_progress_.attempts_left);

      loop_rate.sleep();
    }

    auto result = std::make_shared<GameProgress::Result>();
    result->game_over = current_progress_.game_over;
    result->won = current_progress_.won;

    if (current_progress_.won) {
      RCLCPP_INFO(this->get_logger(), "Action Server: Congratulations! You won!");
    } else {
      RCLCPP_INFO(this->get_logger(), "Action Server: Game Over. You lost.");
    }

    goal_handle->succeed(result);
    RCLCPP_INFO(this->get_logger(), "Action Server: Goal succeeded");
  }
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<ProgressActionServer>();
  rclcpp::executors::MultiThreadedExecutor executor;
  executor.add_node(node);
  executor.spin();
  rclcpp::shutdown();
  return 0;
}
