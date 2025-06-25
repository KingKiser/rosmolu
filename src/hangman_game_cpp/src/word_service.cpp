#include <chrono>
#include <memory>
#include <string>
#include <vector>
#include <random>
#include <algorithm>
#include <sstream>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "hangman_interfaces/msg/progress.hpp"
#include "hangman_interfaces/srv/check_letter.hpp"

using namespace std::chrono_literals;
using std::placeholders::_1;
using std::placeholders::_2;

class WordService : public rclcpp::Node
{
public:
  WordService()
  : Node("word_service"), attempts_left_(20)
  {
    service_ = this->create_service<hangman_interfaces::srv::CheckLetter>(
      "check_letter",
      std::bind(&WordService::check_letter_callback, this, _1, _2));

    letter_sub_ = this->create_subscription<std_msgs::msg::String>(
      "letter_topic",
      10,
      std::bind(&WordService::letter_callback, this, _1));

    progress_pub_ = this->create_publisher<hangman_interfaces::msg::Progress>("progress", 10);

    this->declare_parameter<std::vector<std::string>>("word_list", {
      "python", "hangman", "robot", "ros", "interface"
    });

    auto word_list = this->get_parameter("word_list").as_string_array();
    RCLCPP_INFO(this->get_logger(), "Word list loaded:");
    for (const auto & word : word_list) {
      RCLCPP_INFO(this->get_logger(), "- %s", word.c_str());
    }

    // 무작위 단어 선택
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dist(0, word_list.size() - 1);
    word_ = word_list[dist(gen)];
    word_state_ = std::string(word_.size(), '_');

    RCLCPP_INFO(this->get_logger(), "Selected word has %zu letters.", word_.size());

    // 초기 progress 발행
    hangman_interfaces::msg::Progress msg;
    msg.current_state = word_state_;
    msg.attempts_left = attempts_left_;
    msg.game_over = false;
    msg.won = false;
    progress_pub_->publish(msg);
  }

private:
  rclcpp::Service<hangman_interfaces::srv::CheckLetter>::SharedPtr service_;
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr letter_sub_;
  rclcpp::Publisher<hangman_interfaces::msg::Progress>::SharedPtr progress_pub_;

  std::string word_;
  std::string word_state_;
  std::string current_letter_;
  int attempts_left_;

  void letter_callback(const std_msgs::msg::String::SharedPtr msg)
  {
    current_letter_ = msg->data;
  }

  void check_letter_callback(
    const std::shared_ptr<hangman_interfaces::srv::CheckLetter::Request> ,
    std::shared_ptr<hangman_interfaces::srv::CheckLetter::Response> response)
  {
    const std::string & letter = current_letter_;

    bool found = false;
    for (size_t i = 0; i < word_.size(); ++i) {
      if (word_[i] == letter[0]) {
        word_state_[i] = letter[0];
        found = true;
      }
    }

    if (found) {
      response->is_correct = true;
      response->message = "Correct!";
    } else {
      response->is_correct = false;
      response->message = "WRONG";
      attempts_left_ -= 1;
    }

    response->updated_word_state = word_state_;

    RCLCPP_INFO(this->get_logger(), "Received letter: %s", letter.c_str());
    RCLCPP_INFO(this->get_logger(), "Current word state: %s", word_state_.c_str());

    hangman_interfaces::msg::Progress progress;
    progress.current_state = word_state_;
    progress.attempts_left = attempts_left_;
    progress.game_over = word_state_.find('_') == std::string::npos || attempts_left_ <= 0;
    progress.won = word_state_.find('_') == std::string::npos;

    progress_pub_->publish(progress);
  }
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<WordService>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}

//ros2 run hangman_game_cpp word_service --ros-args --params-file src/hangman_game_cpp/param/word.yaml