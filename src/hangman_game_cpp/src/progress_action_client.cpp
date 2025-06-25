#include <chrono>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "hangman_interfaces/action/game_progress.hpp"

class ProgressActionClient : public rclcpp::Node
{
public:
  using GameProgress = hangman_interfaces::action::GameProgress;
  using GoalHandleGameProgress = rclcpp_action::ClientGoalHandle<GameProgress>;

  ProgressActionClient()
  : Node("progress_action_client")
  {
    this->client_ptr_ = rclcpp_action::create_client<GameProgress>(this, "game_progress");
    send_goal();
  }

private:
  rclcpp_action::Client<GameProgress>::SharedPtr client_ptr_;
  bool result_received_ = false;

  void send_goal()
  {
    RCLCPP_INFO(this->get_logger(), "Action Client: Waiting for action server...");
    if (!this->client_ptr_->wait_for_action_server()) {
      RCLCPP_ERROR(this->get_logger(), "Action server not available after waiting.");
      rclcpp::shutdown();
      return;
    }

    auto goal_msg = GameProgress::Goal();

    RCLCPP_INFO(this->get_logger(), "Action Client: Sending goal request...");
    auto send_goal_options = rclcpp_action::Client<GameProgress>::SendGoalOptions();
    send_goal_options.feedback_callback = std::bind(&ProgressActionClient::feedback_callback, this, std::placeholders::_1, std::placeholders::_2);
    send_goal_options.result_callback = std::bind(&ProgressActionClient::result_callback, this, std::placeholders::_1);

    client_ptr_->async_send_goal(goal_msg, send_goal_options);
  }

  void feedback_callback(
    GoalHandleGameProgress::SharedPtr,
    const std::shared_ptr<const GameProgress::Feedback> feedback)
  {
    if (feedback->game_over) {
      RCLCPP_INFO(this->get_logger(), "Action Client: Game over detected in feedback");
    }
  }

  void result_callback(const GoalHandleGameProgress::WrappedResult & result)
  {
    if (result.code == rclcpp_action::ResultCode::SUCCEEDED) {
      if (result.result->won) {
        RCLCPP_INFO(this->get_logger(), "Action Client: Congratulations! You won!");
      } else {
        RCLCPP_INFO(this->get_logger(), "Action Client: Game Over. You lost.");
      }
    } else {
      RCLCPP_WARN(this->get_logger(), "Action Client: Action did not succeed");
    }
    result_received_ = true;
  }

public:
  bool is_done() const { return result_received_; }
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<ProgressActionClient>();

  rclcpp::Rate loop_rate(10);
  while (rclcpp::ok() && !node->is_done()) {
    rclcpp::spin_some(node);
    loop_rate.sleep();
  }

  rclcpp::shutdown();
  return 0;
}
