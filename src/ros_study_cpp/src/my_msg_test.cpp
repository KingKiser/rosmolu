#include "rclcpp/rclcpp.hpp"
#include "ros_study_msgs/msg/my_msg.hpp"

class MyMsgPublisher : public rclcpp::Node
{
public:
    MyMsgPublisher()
    : Node("my_msg_test"), count_(0.0)
    {

        publisher_ = this->create_publisher<ros_study_msgs::msg::MyMsg>("MyMsg", 10);
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(500),
            std::bind(&MyMsgPublisher::timer_callback, this));
    }

private:
    rclcpp::Publisher<ros_study_msgs::msg::MyMsg>::SharedPtr publisher_; //스마트 포인터 
    rclcpp::TimerBase::SharedPtr timer_;
    float count_;
    
    void timer_callback()
    {
        auto message = ros_study_msgs::msg::MyMsg();
        message.num = count_; //count_ 변수선언
        publisher_->publish(message); //스마트 포인터 퍼블리셔로 해당 메세지 가져옴
        RCLCPP_INFO(this->get_logger(), "Publishing: %f", count_); //애가 로그를 찍는 방법 서식지정자를 활용해서 로그를 찍는다
        count_ += 1.0;
    }

};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MyMsgPublisher>());
    rclcpp::shutdown();
    return 0;
}