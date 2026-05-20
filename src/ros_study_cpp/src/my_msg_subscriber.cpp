#include "rclcpp/rclcpp.hpp"
#include "ros_study_msgs/msg/my_msg.hpp"

using std::placeholders::_1;

class MyMsgSubscriber : public rclcpp::Node
{
public:
  MyMsgSubscriber()
  : Node("my_msg_subscriber")
  {
    auto qos = rclcpp::QoS(rclcpp::QoSInitialization::from_rmw(rmw_qos_profile_default)); //10
    qos.keep_last(10); //10

    subscription_ = this->create_subscription<ros_study_msgs::msg::MyMsg>(
      "MyMsg", qos, std::bind(&MyMsgSubscriber::topic_callback, this, _1));
  }

private:
  rclcpp::Subscription<ros_study_msgs::msg::MyMsg>::SharedPtr subscription_;
  void topic_callback(const ros_study_msgs::msg::MyMsg::SharedPtr msg)
  {
    RCLCPP_INFO(this->get_logger(), "Received: %f", msg->num);
  }

};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MyMsgSubscriber>());
  rclcpp::shutdown();
  return 0;
}
