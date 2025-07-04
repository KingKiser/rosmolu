#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class MinimalSubscriber : public rclcpp::Node
{

private:
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;

    void topic_callback(const std_msgs::msg::String::SharedPtr msg)
    {
        RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg->data.c_str());
    }

public:
    MinimalSubscriber()
    : Node("minimal_subscriber_cpp")
    {
        subscription_ = this->create_subscription<std_msgs::msg::String>(
            "topic", 10,
            std::bind(&MinimalSubscriber::topic_callback, this, std::placeholders::_1));
            //std::placeholders::_1 함수의 인자 자리 표시를 위해서 _1은 첫번째 인자 
            //서브스크라이버는 꼭 필수
    }

};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MinimalSubscriber>());
    rclcpp::shutdown();
    return 0;
}
