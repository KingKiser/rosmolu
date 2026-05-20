#include <chrono>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

class LetterPublisher : public rclcpp::Node
{

private:

    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
    char current_letter_;

    void publish_letter()
    {
        auto message = std_msgs::msg::String();
        message.data = std::string(1, current_letter_);
        publisher_->publish(message);
        RCLCPP_INFO(this->get_logger(), "Publishing: %s", message.data.c_str());

        current_letter_++;
        if (current_letter_ > 'z') {
            current_letter_ = 'a';
        }
    }

public:
    LetterPublisher()
    : Node("letter_publisher"), current_letter_('a')
    {
        publisher_ = this->create_publisher<std_msgs::msg::String>("letter_topic", 10);
        timer_ = this->create_wall_timer(
            1s, std::bind(&LetterPublisher::publish_letter, this));
    }


};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<LetterPublisher>());
    rclcpp::shutdown();
    return 0;
}
