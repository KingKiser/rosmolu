#include "rclcpp/rclcpp.hpp"
#include "ros_study_msgs/srv/my_srv.hpp"

using std::placeholders::_1;
using std::placeholders::_2;

class MyServiceServer : public rclcpp::Node
{
public:
  MyServiceServer() : Node("my_service_server")
  {
    service_ = this->create_service<ros_study_msgs::srv::MySrv>(
      "my_service", std::bind(&MyServiceServer::handle_service, this, _1, _2));
    RCLCPP_INFO(this->get_logger(), "Service server ready");
  }

private:
  void handle_service(
    const std::shared_ptr<ros_study_msgs::srv::MySrv::Request> request,
    std::shared_ptr<ros_study_msgs::srv::MySrv::Response> response)
  {
    RCLCPP_INFO(this->get_logger(), "Received request: %f", request->num);
    response->res = request->num * 2.0f;
  }

  rclcpp::Service<ros_study_msgs::srv::MySrv>::SharedPtr service_;
};

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MyServiceServer>());
  rclcpp::shutdown();
  return 0;
}
