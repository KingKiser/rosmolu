#include <chrono>
#include <memory>
#include <string>
#include <thread>
#include <iostream>

#include "rclcpp/rclcpp.hpp"
#include "hangman_interfaces/srv/check_letter.hpp"

using namespace std::chrono_literals;
using CheckLetter = hangman_interfaces::srv::CheckLetter;

class UserInput : public rclcpp::Node
{
public:
  UserInput()
  : Node("user_input")
  {
    client_ = this->create_client<CheckLetter>("check_letter");

    while (!client_->wait_for_service(1s)) {
      RCLCPP_INFO(this->get_logger(), "Service not available, waiting...");
    }

    RCLCPP_INFO(this->get_logger(), "Press Enter to check the current letter.");
    std::thread(&UserInput::input_loop, this).detach();
  }

private:
  rclcpp::Client<CheckLetter>::SharedPtr client_;

  void input_loop()
  {
    while (rclcpp::ok()) {
      std::string dummy;
      std::getline(std::cin, dummy);  // 엔터 대기

      auto request = std::make_shared<CheckLetter::Request>();
      auto result_future = client_->async_send_request(request,
        std::bind(&UserInput::handle_response, this, std::placeholders::_1));
    }
  }

  void handle_response(rclcpp::Client<CheckLetter>::SharedFuture future)
  {
    auto response = future.get();
    RCLCPP_INFO(this->get_logger(), "Response message: %s", response->message.c_str());
    RCLCPP_INFO(this->get_logger(), "Word State: %s", response->updated_word_state.c_str());
  }
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<UserInput>();
  rclcpp::spin(node);  // input_thread는 detach 상태로 계속 대기
  rclcpp::shutdown();
  return 0;
}
