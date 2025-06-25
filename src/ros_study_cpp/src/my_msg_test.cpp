#include "rclcpp/rclcpp.hpp"
#include "ros_study_msgs/msg/my_msg.hpp"

class MyMsgPublisher : public rclcpp::Node
{
public:
    MyMsgPublisher()
    : Node("my_msg_test"), count_(0.0)
    {
        //this 는 MinimalPublisher의 포인터 함수를 호출하기 위해 사용됨
        //없어도 함수 호출에 무관(있든 없든 컴파일 시 동일하게 됨)
        //this가 사용되는 함수는 주로 가상함수임(오버라이딩이 가능하다!)
        publisher_ = this->create_publisher<ros_study_msgs::msg::MyMsg>("MyMsg", 10);
        //create_publisher는 Node의 함수 qos depth = 10 스마트 포인터 스레드간의 통신을 위한거 아님 메모리 반환을 위해 씀
        //rclcpp::QoS qos_profile(10);
        //publisher_ = this->create_publisher<std_msgs::msg::String>("topic", qos_profile);
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(500),
            std::bind(&MyMsgPublisher::timer_callback, this));
            //&MyMsgPublisher::timer_callback 는 MyMsgPublisher클래스의 timer_callback 함수를 가리키는 멤버 함수 포인터
    }

private:
    rclcpp::Publisher<ros_study_msgs::msg::MyMsg>::SharedPtr publisher_; //스마트 포인터 
    rclcpp::TimerBase::SharedPtr timer_;
    float count_;
    
    void timer_callback()
    {
        auto message = ros_study_msgs::msg::MyMsg();
        //message 변수 생성 auto 예약어 쓴 이유 MyMsg에 어떤게 들어갈줄 몰?루
        message.num = count_; //count_ 변수선언
        publisher_->publish(message); //스마트 포인터 퍼블리셔로 해당 메세지 가져옴
        RCLCPP_INFO(this->get_logger(), "Publishing: %f", count_);
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