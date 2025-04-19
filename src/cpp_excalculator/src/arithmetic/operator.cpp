#include "rclcpp/rclcpp.hpp"
#include "ros_study_msgs/srv/arithmetic_operator.hpp"

#include <chrono>
#include <cstdlib>
#include <memory>
#include <random>

using namespace std::chrono_literals;
using ArithmeticOperator = ros_study_msgs::srv::ArithmeticOperator;

class Operator : public rclcpp::Node
{
public:
    Operator()
        : Node("operator")
    {
        client_ = this->create_client<ArithmeticOperator>("arithmetic_operator");

        while (!client_->wait_for_service(0.1s))
        {
            RCLCPP_WARN(this->get_logger(), "The arithmetic_operator service not available.");
        }

        // 첫 요청 전송
        send_request();
    }

    void spin_once_and_check()
    {
        if (!future_result_.valid())
            return;

        // 요청 완료되었는지 확인
        auto status = future_result_.wait_for(0s);
        if (status == std::future_status::ready)
        {
            try
            {
                auto response = future_result_.get();
                RCLCPP_INFO(this->get_logger(), "Result: %f", response->arithmetic_result);
            }
            catch (const std::exception &e)
            {
                RCLCPP_WARN(this->get_logger(), "Service call failed: %s", e.what());
            }

            // 다음 호출 대기
            std::string input;
            std::cout << "Press Enter for next service call." << std::endl;
            std::getline(std::cin, input);
            send_request();
        }
    }

private:

rclcpp::Client<ArithmeticOperator>::SharedPtr client_;
rclcpp::Client<ArithmeticOperator>::SharedFuture future_result_;

    void send_request()
    {
        auto request = std::make_shared<ArithmeticOperator::Request>();
        request->arithmetic_operator = get_random_operator();
        future_result_ = client_->async_send_request(request).future;
    }

    int get_random_operator()
    {
        static std::random_device rd;
        static std::mt19937 gen(rd());
        std::uniform_int_distribution<> dis(1, 4);
        return dis(gen);
    }

};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<Operator>();

    try
    {
        while (rclcpp::ok())
        {
            rclcpp::spin_some(node);
            node->spin_once_and_check();
        }
    }
    catch (const std::exception &e)
    {
        RCLCPP_ERROR(node->get_logger(), "Exception: %s", e.what());
    }

    rclcpp::shutdown();
    return 0;
}
